from setuptools import find_packages, setup

__version__ = "0.0.0"

setup(
    name="libgencli",
    version=__version__,
    author="notjawad",
    author_email="chaptrhouse@gmail.com",
    description="A command-line interface for searching and downloading books from Library Genesis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/notjawad/libgencli",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "questionary",
        "tqdm",
        "beautifulsoup4",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "libgen=libgencli.cli:search_books",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
