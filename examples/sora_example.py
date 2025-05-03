#!/usr/bin/env python3
"""
Example usage of the Momoya package
"""
import os
import asyncio
import argparse
from momoya.extractors.sora_extractor import SoraExtractor


async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Momoya example script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--gen-id", help="Generation ID to extract")
    group.add_argument("--query", help="Text query to search for content")
    
    parser.add_argument("--output-dir", default="downloads", help="Directory to save downloads")
    parser.add_argument("--no-metadata", action="store_true", help="Don't save metadata")
    parser.add_argument("--limit", type=int, help="Maximum number of results to download")
    parser.add_argument("--no-similar", action="store_true", help="Don't fetch similar content")
    args = parser.parse_args()

    # Get authentication token from environment variable
    auth_token = os.environ.get("MOMOYA_SORA_AUTH_TOKEN", "YOUR_AUTH_TOKEN_HERE")
    
    # Initialize the Sora extractor
    sora_extractor = SoraExtractor(
        auth_token=auth_token,
        download_dir=args.output_dir
    )
    
    # Run the extractor based on search type
    if args.gen_id:
        print(f"Extracting content for gen_id: {args.gen_id}")
        search_term = args.gen_id
        search_type = "content_id"
    else:
        print(f"Searching for content with query: {args.query}")
        search_term = args.query
        search_type = "query"
    
    downloaded = await sora_extractor.run(
        content_id=args.gen_id if args.gen_id else None,
        query=args.query if args.query else None,
        save_metadata=not args.no_metadata,
        search_similar=not args.no_similar,
        limit=args.limit
    )
    
    print(f"\nDownload complete! Total files: {downloaded}")
    print(f"Files saved to: {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    asyncio.run(main())