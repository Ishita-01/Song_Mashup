# Mashup Generator Web Application


## Mashup Audio Generation Web Service using Python and Streamlit

---

## 📖 Description

This project is a web-based application that generates a mashup of audio clips from YouTube videos of a given singer. The user provides input such as singer name, number of videos, duration of each clip, and email ID. The system downloads videos, extracts audio, trims them, creates a ZIP file, and sends the result to the user via email.

The application is built using Python and Streamlit.

---

## 🎯 Objectives

- To search and download YouTube videos automatically.
- To convert video files into audio format.
- To trim audio clips to a fixed duration.
- To merge and package audio files.
- To send output files through email.
- To provide a user-friendly web interface.

---

## 🛠️ Technologies Used

- Python 3
- Streamlit
- yt-dlp
- MoviePy
- PyDub
- FFmpeg
- SMTP (Email Service)
- python-dotenv

---


---

## ⚙️ Methodology

The application follows the following steps:

### 1. User Input
The user enters:
- Singer Name
- Number of Videos (N > 10)
- Duration in Seconds (Y > 20)
- Email ID

### 2. Validation
- Checks if all fields are filled.
- Validates email format.
- Ensures N > 10 and Y > 20.

### 3. Video Download
- Uses yt-dlp to search and download YouTube videos based on singer name.
- Downloads top N videos.

### 4. Audio Extraction
- Uses MoviePy to extract audio from video files.
- Converts MP4 files to MP3 format.

### 5. Audio Trimming
- Uses PyDub to trim each audio file.
- Keeps only first Y seconds.

### 6. ZIP File Creation
- All trimmed audio files are compressed into a ZIP file.

### 7. Email Sending
- Uses SMTP with Gmail server.
- Credentials are stored in `.env` file.
- ZIP file is sent to user's email.

### 8. Cleanup
- Temporary folders are deleted after completion.

---

## 🧩 Input Details

| Parameter | Description | Condition |
|-----------|-------------|-----------|
| Singer Name | Name of singer | Required |
| Number of Videos | Videos to download | Must be > 10 |
| Duration | Trim duration (seconds) | Must be > 20 |
| Email | User email ID | Valid format |

---

## 📤 Output

- A ZIP file containing trimmed audio clips.
- File is sent to the provided email address.
- Success message displayed on web interface.

---

## Project Screenshots
<img width="1911" height="1016" alt="image" src="https://github.com/user-attachments/assets/66148d2f-72fd-4d28-a18d-40b36ef87a67" />


---

## 🚀 Features

- Web-based Interface
- Automatic YouTube Search
- Audio Processing
- Email Delivery
- Secure Credentials Storage
- Automatic Cleanup

---

## ⚠️ Limitations

- Requires stable internet connection.
- YouTube may block downloads.
- Large files may fail in email.
- Processing time depends on number of videos.

---

## 📚 Applications

- Music Mashup Creation
- Audio Sampling
- Learning Multimedia Processing
- Web-based Automation

---


## ✅ Conclusion

This project demonstrates the integration of web technologies, multimedia processing, and automation using Python. It provides a complete solution for generating mashup audio files and delivering them to users via email through a simple web interface.




