import streamlit as st
import os
import shutil
import zipfile
import re
import smtplib
from email.message import EmailMessage

from yt_dlp import YoutubeDL
from pydub import AudioSegment
import moviepy.editor as mp

from dotenv import load_dotenv
import os

load_dotenv()



def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


def download(singer, n):
    query = f"ytsearch{n}:{singer} songs"

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])


def audioConversion():

    os.makedirs("audios", exist_ok=True)

    for file in os.listdir("videos"):
        if file.endswith(".mp4"):
            video_path = "videos/" + file
            audio_name = file.replace(".mp4", ".mp3")
            audio_path = "audios/" + audio_name

            video = mp.VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, logger=None)
            video.close()


def trim_audio(seconds):
    os.makedirs("trimmed", exist_ok=True)

    for file in os.listdir("audios"):
        if file.endswith(".mp3"):
            audio = AudioSegment.from_mp3("audios/" + file)

            trimmed = audio[:seconds * 1000]

            trimmed.export("trimmed/" + file, format="mp3")


def create_zip(zip_name):
    with zipfile.ZipFile(zip_name, "w") as zipf:

        for file in os.listdir("trimmed"):
            zipf.write(
                "trimmed/" + file,
                arcname=file
            )


def send_email(receiver, zip_file):

    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender or not password:
        raise Exception("Email credentials not found in .env file")

    msg = EmailMessage()

    msg["Subject"] = "Mashup Audio Result"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content("Your mashup audio files are attached.")

    with open(zip_file, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(zip_file)

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="zip",
        filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def cleanup():
    folders = ["videos", "audios", "trimmed"]

    for f in folders:
        shutil.rmtree(f, ignore_errors=True)


st.set_page_config(page_title="Mashup Service")

st.title("Mashup Generator Web Service")

st.markdown("Generate mashup audio and receive via email")

# Input Form
with st.form("mashup_form"):

    singer = st.text_input("Singer Name")

    videos = st.number_input(
        "Number of Videos ( > 10 )",
        min_value=11,
        step=1
    )

    duration = st.number_input(
        "Duration (seconds > 20 )",
        min_value=21,
        step=1
    )

    email = st.text_input("Email ID")

    submit = st.form_submit_button("Submit")


if submit:

    if not singer:
        st.error("Enter singer name")

    elif not is_valid_email(email):
        st.error("Invalid email format")

    else:

        try:
            st.info("⏳ Processing... Please wait")

            os.makedirs("videos", exist_ok=True)

            # Run pipeline
            download(singer, int(videos))
            audioConversion()
            trim_audio(int(duration))

            zip_name = "mashup_result.zip"
            create_zip(zip_name)

            send_email(email, zip_name)

            cleanup()

            st.success("File sent to your email successfully!")

        except Exception as e:
            st.error(f"Error: {e}")
