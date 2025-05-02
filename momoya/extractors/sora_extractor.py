"""
Sora AI image extractor implementation
"""
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

import aiohttp
import aiofiles

from momoya.core.base_extractor import BaseExtractor


class SoraExtractor(BaseExtractor):
    """Extractor for Sora AI-generated images."""
    
    def __init__(self, auth_token: str = "YOUR_AUTH_TOKEN_HERE", download_dir: str = "downloads"):
        """Initialize the Sora Image Extractor.
        
        Args:
            auth_token: Your authentication token for the Sora API.
            download_dir: Directory where downloads will be saved.
        """
        self.auth_token = auth_token
        self.download_dir = download_dir
        self.headers = {
            "authority": "sora.chatgpt.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://sora.chatgpt.com",
            "referer": "https://sora.chatgpt.com/explore",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        
        if self.auth_token == "YOUR_AUTH_TOKEN_HERE":
            print("WARNING: You're using the default auth token placeholder.")
            print("Please update the auth_token with your own authentication token.")
        
        self.headers["Authorization"] = f"Bearer {self.auth_token}"
        
        # Ensure downloads directory exists
        os.makedirs(self.download_dir, exist_ok=True)

    async def fetch_content_data(self, content_id: str, search_similar: bool = True, limit: Optional[int] = None) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """Fetch data about an AI-generated image using its gen_id.
        
        Args:
            content_id: The generation ID (gen_id) to search for
            search_similar: If True, return similar images in addition to the exact match
            limit: Maximum number of similar images to return, None means all available
            
        Returns:
            Data about the requested image(s) or None if not found
        """
        url = "https://sora.chatgpt.com/backend/search"
        
        # Payload for the search request
        payload = {
            "similar_to": [content_id],
            "query": ""
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=payload) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if "data" in data and len(data["data"]) > 0:
                        if search_similar:
                            # Return all images without limit
                            results = []
                            for item in data["data"]:
                                gen = item.get("generation", {})
                                results.append(gen)
                                
                            # Check if there's more data to fetch using pagination
                            has_more = data.get("has_more", False)
                            last_id = data.get("last_id", None)
                            
                            # Continue fetching if there are more results
                            while has_more and last_id:
                                print(f"Fetching more images... (last_id: {last_id})")
                                
                                # Update payload for pagination
                                pagination_payload = {
                                    "similar_to": [content_id],
                                    "query": "",
                                    "after": last_id
                                }
                                
                                async with session.post(url, headers=self.headers, json=pagination_payload) as paginated_response:
                                    paginated_response.raise_for_status()
                                    paginated_data = await paginated_response.json()
                                    
                                    if "data" in paginated_data and len(paginated_data["data"]) > 0:
                                        for item in paginated_data["data"]:
                                            gen = item.get("generation", {})
                                            results.append(gen)
                                        
                                        has_more = paginated_data.get("has_more", False)
                                        last_id = paginated_data.get("last_id", None)
                                    else:
                                        break
                            
                            print(f"Total images found: {len(results)}")
                            return results
                        else:
                            # Return only the exact match or the first result
                            for item in data["data"]:
                                gen = item.get("generation", {})
                                if gen.get("id") == content_id:
                                    return gen
                            
                            # If we didn't find an exact match, return the first result
                            return data["data"][0].get("generation", {})
                    else:
                        print(f"No data found for gen_id: {content_id}")
                        return None
        
        except aiohttp.ClientError as e:
            print(f"Error making request: {e}")
            return None
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
            return None
    
    async def download_content(self, url: str, filename: str) -> bool:
        """Download an image from a URL asynchronously.
        
        Args:
            url: The URL of the image to download
            filename: The filename to save the image as
            
        Returns:
            True if the download was successful, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    
                    filepath = os.path.join(self.download_dir, filename)
                    async with aiofiles.open(filepath, 'wb') as f:
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            await f.write(chunk)
            
            print(f"Downloaded: {filename}")
            return True
        
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            return False
    
    async def save_metadata(self, data: Dict[str, Any], filename: str) -> bool:
        """Save metadata to a JSON file asynchronously.
        
        Args:
            data: The metadata to save
            filename: The filename to save the metadata as
            
        Returns:
            True if the save was successful, False otherwise
        """
        try:
            filepath = os.path.join(self.download_dir, filename)
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, indent=2, ensure_ascii=False))
            
            print(f"Saved metadata: {filename}")
            return True
        
        except Exception as e:
            print(f"Error saving metadata {filename}: {e}")
            return False
    
    async def process_content_batch(self, content_data: List[Dict[str, Any]], save_metadata: bool = True) -> int:
        """Process and download multiple images.
        
        Args:
            content_data: List of image data dictionaries
            save_metadata: Whether to save metadata for each image
            
        Returns:
            Number of successfully downloaded images
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_tasks = []
        metadata_tasks = []
        
        for image in content_data:
            if image and 'url' in image and image['url']:
                image_id = image.get('id', 'unknown')
                # Create download task
                img_filename = f"{image_id}_{timestamp}.png"
                download_tasks.append(self.download_content(image['url'], img_filename))
                
                # Create metadata task if requested
                if save_metadata:
                    meta_filename = f"{image_id}_{timestamp}.json"
                    metadata_tasks.append(self.save_metadata(image, meta_filename))
        
        # Execute all download tasks
        download_results = await asyncio.gather(*download_tasks, return_exceptions=True)
        
        # Execute all metadata tasks if any
        if metadata_tasks:
            metadata_results = await asyncio.gather(*metadata_tasks, return_exceptions=True)
        
        # Count successful downloads
        successful_downloads = sum(1 for result in download_results if result is True)
        
        return successful_downloads
    
    async def run(self, content_id: str, save_metadata: bool = True) -> int:
        """Run the extractor to fetch and download images.
        
        Args:
            content_id: The generation ID to search for
            save_metadata: Whether to save metadata for each image
            
        Returns:
            Number of downloaded images
        """
        print(f"Fetching data for gen_id: {content_id}")
        images_data = await self.fetch_content_data(content_id)
        
        if not images_data:
            print(f"No data found for gen_id: {content_id}")
            return 0
        
        print(f"Found {len(images_data)} images. Downloading...")
        downloaded = await self.process_content_batch(images_data, save_metadata)
        
        print(f"Download complete. Successfully downloaded {downloaded} images.")
        return downloaded