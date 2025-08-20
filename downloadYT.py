import yt_dlp
from pathlib import Path

'''
Functions to download YouTube videos and check for existing local files.
Usage: check_local_file(url, directory)
'''

def check_id_of_url(url):
    """    
    Check the id of a YouTube video URL.
    """
    # Download options
    ydl_opts = {
        "quiet": False,  # Show progress in console
        "skip_download": True,  # Ensure the video is downloaded
    }
    id = ""
    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        id = info.get('id', None)
        print(f"Video title: {info.get('title', 'Unknown Title')}")
        print(f"URL: {info.get('webpage_url', 'Unknown URL')}")
        print(f"ID: {id}")

    return id

def check_local_file(url, directory):
    """
    Search if a local .mp4 file exists in the given directory, and compare IDs"""
    
    directory = Path(directory)
    if not directory.is_dir():
        print(f"The path '{directory}' is not a valid directory.")
        return None
    
    id = check_id_of_url(url)
    
    # Search for .mp4 files in the directory
    mp4_files = list(directory.glob('*.mp4'))
    if not mp4_files:
        print(f"No .mp4 files found in the directory '{directory}'.")
        return download_video(url, directory, id)
    
    # Compare name of file with video ID
    for file in mp4_files:
        if id in file.name:
            print(f"Found matching file: {file.name}")
            return file
    
    # If nomatching file found, download the video
    return download_video(url, directory, id)
        
def download_video(url, directory, id):
    """
    Download the video from the given URL to the specified directory.
    """
    output_path = directory / f"{id}.mp4"
    
    # Download options
    ydl_opts = {
        "format": "any",  # Download the best available quality
        "outtmpl": str(output_path),  # Output filename pattern
        "quiet": False,  # Show progress in console
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print(f"Video downloaded to {directory.resolve()}")
    
    return directory / f"{id}.mp4"