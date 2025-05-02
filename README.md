# Momoya

A Python package for extracting AI-generated images and videos from various platforms.

## Features

- Extract AI-generated content from different platforms
- Download images and videos with associated metadata
- Concurrent downloads using asynchronous I/O
- Clean architecture for easy extensibility
- Command-line interface for easy usage

## Currently Supported Platforms

- **Sora AI**: Extracts images and metadata using gen_id

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/momoya.git
cd momoya

# Install the package
pip install -e .
```

## Usage

### Command Line Interface

The package provides a command-line interface for easy usage:

```bash
# Set your authentication token (recommended)
export MOMOYA_SORA_AUTH_TOKEN="your_auth_token_here"

# Extract content from Sora
python -m momoya.cli sora gen_01jt5veqacf4tsvcwa76kb908m

# Save to a specific directory
python -m momoya.cli sora gen_01jt5veqacf4tsvcwa76kb908m --output-dir my_downloads

# Skip saving metadata
python -m momoya.cli sora gen_01jt5veqacf4tsvcwa76kb908m --no-metadata
```

### Python API

You can also use the package in your Python code:

```python
import asyncio
from momoya.extractors.sora_extractor import SoraExtractor

async def download_sora_content():
    # Initialize the extractor
    extractor = SoraExtractor(
        auth_token="your_auth_token_here",
        download_dir="downloads"
    )
    
    # Download content
    gen_id = "gen_01jt5veqacf4tsvcwa76kb908m"
    downloaded = await extractor.run(gen_id, save_metadata=True)
    
    print(f"Downloaded {downloaded} items")

# Run the async function
asyncio.run(download_sora_content())
```

## Adding New Extractors

The package is designed to be easily extensible with new extractors for different AI platforms:

1. Create a new extractor class in the `momoya/extractors` directory
2. Implement the `BaseExtractor` interface
3. Add the new extractor to the CLI in `momoya/cli.py`

## Authentication

Most AI platforms require authentication to access their APIs. For security, you should avoid hardcoding authentication tokens in your code. Instead, you can:

1. Pass the token as an argument to the extractor
2. Set it as an environment variable
3. Use a secure credentials manager

## License

MIT