from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_user_info():
    user_id = os.getenv("user_id")  
    access_token = os.getenv("access_token")  

    
    url = f"https://graph.facebook.com/v21.0/{user_id}?fields=id,username,media{{comments{{id,text,like_count}},caption,id}}&access_token={access_token}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        with open('user_info.txt', 'w', encoding='utf-8') as f:
            f.write("User Information:\n\n")
            f.write(f"- User ID: {data['id']}\n")
            f.write(f"- Username: {data.get('username', 'N/A')}\n\n")
            
            if 'media' in data:
                media = data['media']['data']
                f.write("Reels/Posts:\n\n")
                for post in media:
                    f.write(f"**Post ID:** {post['id']}\n")
                    caption = post.get('caption', 'No caption')
                    f.write(f"**Caption:**\n{caption}\n\n")
                    f.write(f"**Comments Count:** {len(post.get('comments', {}).get('data', []))}\n")
                    
                    # Check if there are comments and print them
                    if 'comments' in post:
                        comments = post['comments']['data']
                        if comments:
                            f.write("**Comments:**\n")
                            for comment in comments:
                                f.write(f"- Comment: {comment['text']} (Likes: {comment.get('like_count', 0)})\n")
                        else:
                            f.write("- No comments available.\n")
                    f.write("\n")  # Add a newline for better separation
            else:
                f.write("No media found.\n")
    else:
        print("Failed to fetch user info:", response.status_code, response.text)

get_user_info()
