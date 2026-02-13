
import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import moviepy.editor as mp

def IsValid():
    if len(sys.argv) != 5:
        print("Invalid number of arguments")
        sys.exit(1)
        n = int(sys.argv[2])
        y = int(sys.argv[3])
        if n <= 10:
            raise ValueError("Number of videos must be > 10")
        if y <= 20:
            raise ValueError("Audio duration must be > 20 seconds")

    
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

    


def trim(seconds):
    

    os.makedirs("trimmed", exist_ok=True)

    for file in os.listdir("audios"):
        if file.endswith(".mp3"):
            audio = AudioSegment.from_mp3("audios/" + file)

            trimmed = audio[:seconds * 1000]

            trimmed.export("trimmed/" + file, format="mp3")

    


def merge(output_file):
    final_audio = AudioSegment.empty()

    for file in sorted(os.listdir("trimmed")):
        if file.endswith(".mp3"):
            audio = AudioSegment.from_mp3("trimmed/" + file)
            final_audio += audio

    final_audio.export(output_file, format="mp3")


def cleanup():
    shutil.rmtree("videos", ignore_errors=True)
    shutil.rmtree("audios", ignore_errors=True)
    shutil.rmtree("trimmed", ignore_errors=True)

def main():

    IsValid()

    singer = sys.argv[1]
    num_videos = int(sys.argv[2])
    seconds = int(sys.argv[3])
    output_file = sys.argv[4]

    
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)
    os.makedirs("trimmed", exist_ok=True)

    audioConversion()
    trim(seconds)
    download(singer, num_videos)
    merge(output_file)
    print("\nSuccess!")
    cleanup()

if __name__ == "__main__":
    main()
