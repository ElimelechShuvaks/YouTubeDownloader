from tempfile import mktemp 
from flask import Flask, after_this_request, request, render_template, send_file
import yt_dlp

app = Flask(__name__)

def download_youtube_video(url, output_path): 
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'nocheckcertificate': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


#עם כניסה לעומק
# def get_video_list(channel_url):
#     options = {
#         'extract_flat': False,  # מאפשר כניסה לעומק עבור קטגוריות
#         'quiet': True,
#         'skip_download': True,
#         'nocheckcertificate': True
#     }
#     with yt_dlp.YoutubeDL(options) as ydl:
#         info = ydl.extract_info(channel_url, download=False)
    
#     video_list = []
#     for entry in info.get('entries', []):
#         # בדיקה אם יש תת-ערכים בקטגוריה הנוכחית
#         if entry.get('_type') == 'playlist':
#             # כניסה לרשימת הסרטונים בקטגוריה
#             for video in entry.get('entries', []):
#                 if video.get('id'):  # ודא שהסרטון מכיל מזהה
#                     video_list.append({
#                         'title': video.get('title'),
#                         'url': f"https://www.youtube.com/watch?v={video.get('id')}",
#                         'upload_date': video.get('upload_date')
#                     })
#         elif entry.get('_type') == 'video':  # אם זה סרטון בודד
#             video_list.append({
#                 'title': entry.get('title'),
#                 'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
#                 'upload_date': entry.get('upload_date')
#             })
    
#     return video_list

#בלי כניסה לעומק
def get_video_list(channel_url):
    options = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
        'nocheckcertificate': True
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    
    video_list = [
        {
            'title': video.get('title', 'Unknown title'),  # הוספת ערך ברירת מחדל
            'url': f"https://www.youtube.com/watch?v={video.get('id', '#')}",
            'upload_date': video.get('upload_date', 'Unknown date')
        }
        for video in info.get('entries', []) if video  # בדיקה ש- video אינו None
    ]
    return video_list


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    output_file = mktemp(suffix=".mp4")
    download_youtube_video(video_url, output_file)
    return send_file(output_file, as_attachment=True, download_name="downloaded_video.mp4")

@app.route('/channel_videos', methods=['POST'])
def channel_videos():
    channel_url = request.form['channel_url']
    videos = get_video_list(channel_url)
    return render_template('video_list.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
