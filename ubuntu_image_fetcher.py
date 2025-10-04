import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extract the filename from URL or generate a unique one if missing."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        # Generate a unique filename using hash
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    return filename

def download_image(url, directory="Fetched_Images"):
    """Fetches an image from the given URL and saves it."""
    try:
        # Ensure directory exists
        os.makedirs(directory, exist_ok=True)

        # Fetch the image
        headers = {"User-Agent": "Ubuntu-Image-Fetcher/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad status

        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(directory, filename)

        # Prevent duplicates
        if os.path.exists(filepath):
            print(f"✓ Image already exists: {filename}")
            return filepath

        # Save the image in binary mode
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for URL {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for URL {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Please enter image URLs (comma-separated for multiple): ")
    urls_list = [url.strip() for url in urls.split(",") if url.strip()]

    for url in urls_list:
        download_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
