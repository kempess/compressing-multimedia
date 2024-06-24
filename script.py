from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'wav'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_size(size):
    units = ['B', 'KB', 'MB', 'GB']
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/image')
def index_image():
    return render_template('image.html')

@app.route('/audio')
def index_audio():
    return render_template('audio.html')

@app.route('/video')
def index_video():
    return render_template('video.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/compress-image', methods=['POST'])
def post_endpoint_image():
    if 'image' not in request.files:
        return redirect(url_for('index_image'))
    
    image_file = request.files['image']
    if image_file.filename == '':
        return redirect(url_for('index'))

    image_quality = request.form['quality']
    if not image_quality:
        image_quality = 50
    else:
        image_quality = int(image_quality)

    if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        compressed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + filename)

        original_image = Image.open(original_image_path)
        original_size = os.path.getsize(original_image_path)

        original_image.save(compressed_image_path, quality=image_quality)
        compressed_size = os.path.getsize(compressed_image_path)

        compression_ratio = (1 - (compressed_size / original_size)) * 100
        compression_ratio = f"{compression_ratio:.2f}"

        original_size_formatted = format_size(original_size)
        compressed_size_formatted = format_size(compressed_size)

        return render_template('image.html',
                               original_image=url_for('uploaded_file', filename=filename),
                               compressed_image=url_for('uploaded_file', filename='compressed_' + filename),
                               original_size=original_size_formatted,
                               compressed_size=compressed_size_formatted,
                               compression_ratio=compression_ratio)
    else:
        return redirect(url_for('index_image'))

@app.route('/compress-audio', methods=['POST'])
def post_endpoint_audio():
    if 'audio' not in request.files:
        return redirect(url_for('index_audio'))
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return redirect(url_for('index'))

    audio_quality = request.form['quality']
    if not audio_quality:
        audio_quality = 128  # default 128 kbps
    else:
        audio_quality = int(audio_quality)

    if audio_file and allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
        filename = secure_filename(audio_file.filename)
        audio_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        original_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        compressed_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + filename)

        original_audio = AudioSegment.from_file(original_audio_path)
        original_size = os.path.getsize(original_audio_path)

        # Convert quality from percentage to kbps
        audio_bitrate = int((audio_quality / 100) * 320)

        # Export compressed audio to MP3 format
        original_audio.export(compressed_audio_path, format='mp3', bitrate=f"{audio_bitrate}k")
        compressed_size = os.path.getsize(compressed_audio_path)

        compression_ratio = (1 - (compressed_size / original_size)) * 100
        compression_ratio = f"{compression_ratio:.2f}"

        original_size_formatted = format_size(original_size)
        compressed_size_formatted = format_size(compressed_size)

        return render_template('audio.html',
                               original_audio=url_for('uploaded_file', filename=filename),
                               compressed_audio=url_for('uploaded_file', filename='compressed_' + filename),
                               original_size=original_size_formatted,
                               compressed_size=compressed_size_formatted,
                               compression_ratio=compression_ratio)
    else:
        return redirect(url_for('index_audio'))

@app.route('/compress-video', methods=['POST'])
def post_endpoint_video():
    if 'video' not in request.files:
        return redirect(url_for('index_video'))
    
    video_file = request.files['video']
    if video_file.filename == '':
        return redirect(url_for('index'))

    video_quality = request.form['quality']
    if not video_quality:
        video_quality = 50  # default 50% quality
    else:
        video_quality = int(video_quality)

    if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
        filename = secure_filename(video_file.filename)
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        compressed_video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + filename)

        original_video = VideoFileClip(original_video_path)
        original_size = os.path.getsize(original_video_path)

        # Convert quality from percentage to bitrate
        video_bitrate = int((video_quality / 100) * 1000)

        # Export compressed video to MP4 format
        original_video.write_videofile(compressed_video_path, codec='libx264', audio_codec='aac', bitrate=f"{video_bitrate}k")
        compressed_size = os.path.getsize(compressed_video_path)

        compression_ratio = (1 - (compressed_size / original_size)) * 100
        compression_ratio = f"{compression_ratio:.2f}"

        original_size_formatted = format_size(original_size)
        compressed_size_formatted = format_size(compressed_size)

        return render_template('video.html',
                               original_video=url_for('uploaded_file', filename=filename),
                               compressed_video=url_for('uploaded_file', filename='compressed_' + filename),
                               original_size=original_size_formatted,
                               compressed_size=compressed_size_formatted,
                               compression_ratio=compression_ratio)
    else:
        return redirect(url_for('index_video'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
