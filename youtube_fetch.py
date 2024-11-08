from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_channel_videos(channel_id, api_key):
    # Initialize a list to hold video details
    videos = []

    # Fetch the playlist ID of the channel's uploads
    playlist_url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}"
    playlist_response = requests.get(playlist_url)

    if playlist_response.status_code == 200:
        playlist_data = playlist_response.json()
        if 'items' in playlist_data and len(playlist_data['items']) > 0:
            uploads_playlist_id = playlist_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Now fetch videos from the uploads playlist
            video_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist_id}&key={api_key}"
            video_response = requests.get(video_url)

            if video_response.status_code == 200:
                video_data = video_response.json()
                
                # Extract video details
                for item in video_data.get('items', []):
                    video_title = item['snippet']['title']
                    video_description = item['snippet']['description']
                    video_url = f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
                    videos.append({
                        'title': video_title,
                        'description': video_description,
                        'url': video_url
                    })
            else:
                print(f"Failed to retrieve videos. Status code: {video_response.status_code}")
        else:
            print("No uploads playlist found for this channel.")
    else:
        print(f"Failed to retrieve playlist. Status code: {playlist_response.status_code}")

    return videos

def save_videos_to_file(videos):
    # Save video details to a file with neat formatting
    with open('youtube_videos.txt', 'w') as f:
        for video in videos:
            f.write(f"Title: {video['title']}\n")
            f.write(f"Description: {video['description']}\n")
            f.write(f"URL: {video['url']}\n")
            f.write("\n" + "-"*50 + "\n\n")  # Separator for readability
    print("Video details saved to youtube_videos.txt")

def main():
    api_key = os.getenv("api_key") 
    channel_id = os.getenv("channel_id")  

    # Fetch videos and save to a file
    videos = get_channel_videos(channel_id, api_key)
    save_videos_to_file(videos)

# Run the main function
if __name__ == "__main__":
    main()
