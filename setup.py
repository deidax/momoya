from setuptools import setup, find_packages

setup(
    name="momoya",
    version="1.0.0",
    description="A package for extracting AI-generated images and videos from various platforms",
    author="deidax",
    author_email="deidaxtech@gmail.com",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "aiofiles>=0.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)