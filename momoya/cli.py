#!/usr/bin/env python3
"""
Command-line interface for Momoya image/video extractors
"""
import os
import sys
import argparse
import asyncio
from typing import List, Dict, Any, Optional

from momoya.extractors.sora_extractor import SoraExtractor
# Import other extractors as they are added


async def extract_sora_content(gen_id: str, auth_token: str, download_dir: str, save_metadata: bool) -> int:
    """Extract Sora AI-generated content using the Sora extractor.
    
    Args:
        gen_id: The generation ID to extract
        auth_token: Authentication token for the API
        download_dir: Directory to save downloads
        save_metadata: Whether to save metadata
    
    Returns:
        Number of downloaded items
    """
    extractor = SoraExtractor(auth_token=auth_token, download_dir=download_dir)
    return await extractor.run(gen_id, save_metadata=save_metadata)


async def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Momoya - AI-generated content extractor")
    
    # Platform subparsers
    subparsers = parser.add_subparsers(dest="platform", help="AI platform to extract from")
    
    # Sora extractor arguments
    sora_parser = subparsers.add_parser("sora", help="Extract content from Sora AI")
    sora_parser.add_argument("gen_id", help="Generation ID to extract")
    sora_parser.add_argument("--auth-token", help="Authentication token for Sora API")
    sora_parser.add_argument("--no-metadata", action="store_true", help="Don't save metadata")
    sora_parser.add_argument("--output-dir", default="downloads", help="Directory to save downloads")
    
    # Add parsers for other platforms here
    
    # Global arguments
    parser.add_argument("--version", action="store_true", help="Show version information")
    
    args = parser.parse_args()
    
    if args.version:
        from momoya import __version__
        print(f"Momoya v{__version__}")
        return
    
    if not args.platform:
        parser.print_help()
        return
    
    if args.platform == "sora":
        # Get auth token from argument, environment variable, or prompt
        auth_token = args.auth_token
        if not auth_token:
            auth_token = os.environ.get("MOMOYA_SORA_AUTH_TOKEN")
        
        if not auth_token:
            print("Please provide an authentication token for Sora API.")
            print("You can provide it using the --auth-token argument or")
            print("by setting the MOMOYA_SORA_AUTH_TOKEN environment variable.")
            return
        
        # Run the extractor
        downloaded = await extract_sora_content(
            args.gen_id,
            auth_token,
            args.output_dir,
            not args.no_metadata
        )
        
        print(f"\nTotal downloaded: {downloaded} files")
        print(f"Files saved to: {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    asyncio.run(main())