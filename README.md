# Compressing Media
______

Aplikasi ini bertujuan untuk melakukan kompresi berbagai jenis file media, dengan tujuan mengurangi ukuran file sambil mempertahankan kualitas yang dapat diterima. Baik itu gambar, video, maupun file audio, teknik kompresi yang efisien sangat penting untuk mengoptimalkan ruang penyimpanan dan meningkatkan kecepatan transfer.

## Fitur-fitur :
______

1. ***Kompresi Gambar:*** Alat dan skrip untuk mengurangi ukuran gambar tanpa mengorbankan kualitas secara signifikan.
2. ***Kompresi Video:*** Teknik untuk mengompresi file video agar lebih cocok untuk streaming atau penyimpanan.
3. ***Kompresi Audio:*** Metode untuk mengurangi ukuran file rekaman audio sambil mempertahankan kualitas suara.
4. ***Pemrosesan Batch:*** Skrip untuk mengotomatisasi proses kompresi untuk beberapa file secara simultan.
5. ***Kontrol Kualitas:*** Panduan dan konfigurasi untuk menyeimbangkan antara pengurangan ukuran file dan mempertahankan kualitas media yang dapat diterima.

### Cara Menjalankan
______

1. Clone Repository terlebih dahulu :
```markdown
git clone https://github.com/kempess/Compressing-Media.git
```
2. buka file :
```markdown
cd Compressing-Media
```
3. Install Python dependecies :
```markdown
 python -m venv venv    
.\venv\Scripts\activate   
```  
4. Instal Flask:
Pastikan Flask diinstal dengan benar dalam environment virtual Anda. Jalankan perintah berikut untuk menginstal Flask:
```markdown
pip install Flask
```
5. Instal pydub:
Pastikan pydub terinstal dengan benar:
```markdown
pip install pydub
```
6. install requirements
```markdown
pip install -r requirements.txt
```
7. Install ffmpeg :
Instal ffmpeg:
pydub memerlukan ffmpeg atau libav untuk memproses file audio. Anda perlu menginstal salah satu dari mereka dan memastikan mereka berada dalam sistem PATH Anda. Anda dapat mendownload ffmpeg dari situs resmi [ffmpeg](https://ffmpeg.org/download.html) dan mengikuti instruksi instalasi untuk OS Anda.

Setelah menginstal ffmpeg, pastikan ffmpeg dapat diakses dari command line:
```markdown
ffmpeg -version
```
8. Jika dependencies python telah usang, update ke :
```markdown
python.exe -m pip install --upgrade pip
```
9. Jalankan Aplikasi :
``` markdown
python script.py
```

#### Penjelasan Detail
______
Kode di atas merupakan sebuah aplikasi web berbasis Flask yang memungkinkan pengguna untuk mengunggah dan mengompres file gambar, audio, dan video. Aplikasi ini menggunakan beberapa pustaka eksternal untuk kompresi file, yaitu:

1. **PIL (Python Imaging Library)** untuk kompresi gambar.
2. **pydub** untuk kompresi audio.
3. **moviepy** untuk kompresi video.



Berikut adalah penjelasan tentang algoritma dan teknik kompresi yang digunakan:
______

##### 1. Kompresi Gambar
PIL digunakan untuk membuka dan menyimpan gambar dengan kualitas yang ditentukan oleh pengguna. Algoritma kompresi yang digunakan oleh PIL tergantung pada format gambar, misalnya:
- **JPEG** menggunakan kompresi lossy dengan algoritma Discrete Cosine Transform (DCT).
- **PNG** menggunakan kompresi lossless dengan algoritma DEFLATE.

Dalam kode:
```markdown
original_image.save(compressed_image_path, quality=image_quality)
```
`image_quality` adalah parameter yang dikontrol pengguna untuk mengatur tingkat kompresi. Nilai yang lebih rendah berarti kompresi lebih tinggi (dan kualitas lebih rendah).

##### 2. Kompresi Audio
Pydub digunakan untuk mengonversi dan mengompres file audio. Algoritma kompresi yang digunakan adalah:
- **MP3** menggunakan kompresi lossy dengan algoritma Modified Discrete Cosine Transform (MDCT).

Dalam kode:
```markdown
original_audio.export(compressed_audio_path, format='mp3', bitrate=f"{audio_bitrate}k")
```
`audio_bitrate` mengatur bitrate audio dalam kbps. Bitrate lebih rendah berarti kompresi lebih tinggi (dan kualitas lebih rendah).

##### 3. Kompresi Video
Moviepy digunakan untuk membuka dan menyimpan video dengan kualitas yang ditentukan oleh pengguna. Algoritma kompresi yang digunakan oleh moviepy, melalui codec `libx264`, adalah:
- **H.264** (atau AVC) yang menggunakan kompresi lossy dengan berbagai teknik seperti Intra-frame dan Inter-frame compression.

Dalam kode:
```markdown
original_video.write_videofile(compressed_video_path, codec='libx264', audio_codec='aac', bitrate=f"{video_bitrate}k")
```
`video_bitrate` mengatur bitrate video dalam kbps. Bitrate lebih rendah berarti kompresi lebih tinggi (dan kualitas lebih rendah).

##### Ringkasan
______
- **Gambar**: Kompresi dilakukan dengan PIL menggunakan DCT untuk JPEG atau DEFLATE untuk PNG.
- **Audio**: Kompresi dilakukan dengan pydub menggunakan MDCT untuk MP3.
- **Video**: Kompresi dilakukan dengan moviepy menggunakan H.264.

Setiap kompresi menggunakan parameter kualitas atau bitrate yang ditentukan oleh pengguna, yang menentukan tingkat kompresi dan kualitas output.
