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
    parser.add_argument("gen_id", help="Generation ID to extract")
    parser.add_argument("--output-dir", default="downloads", help="Directory to save downloads")
    parser.add_argument("--no-metadata", action="store_true", help="Don't save metadata")
    args = parser.parse_args()

    # Get authentication token from environment variable
    auth_token = os.environ.get("MOMOYA_SORA_AUTH_TOKEN", "YOUR_AUTH_TOKEN_HERE")
    
    # Initialize the Sora extractor
    sora_extractor = SoraExtractor(
        auth_token=auth_token,
        download_dir=args.output_dir
    )
    
    # Run the extractor
    print(f"Extracting content for gen_id: {args.gen_id}")
    downloaded = await sora_extractor.run(
        args.gen_id, 
        save_metadata=not args.no_metadata
    )
    
    print(f"\nDownload complete! Total files: {downloaded}")
    print(f"Files saved to: {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    asyncio.run(main())