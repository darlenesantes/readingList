# Package setup script for the reading list CLI 
from setuptools import setup, find_packages

setup(
    name="reading-list-cli",
    version="0.1.0",
    author="Demi Fashemo & Darlene Santes",
    description="A CLI tool for managing a personal reading list with Google Books and GenAI integrations",
    packages=find_packages(),  # Automatically finds the `app/` package
    install_requires=[
        "click",
        "requests",
        "python-dotenv",
        "google-genai",
        "pytest",
        "sqlalchemy",
        "google-auth",
        "google-auth-oauthlib",
        "flake8",
        "black",
    ],
    entry_points={
        "console_scripts": [
            # Exposes `bookclub` as the CLI entrypoint
            "bookclub=app.cli:cli",
        ],
    },
    python_requires=">=3.8",
)
