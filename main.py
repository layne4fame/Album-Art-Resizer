import subprocess
import os
import shutil
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
import io
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import eyed3
from eyed3.id3.frames import ImageFrame
from PIL import Image
from mutagen.flac import FLAC, Picture
from pydub import AudioSegment
from mutagen.m4a import *
import ffmpeg


class FolderSettings:

    def __init__(self):
        self.output_folder = ''
        self.input_folder = ''

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        output_folder_text.set(self.output_folder)
        return

    def select_input_folder(self):
        self.input_folder = filedialog.askdirectory()
        input_folder_text.set(self.input_folder)
        return

    def run_conversion(self):
        self.input_folder = input_folder_text.get()
        self.output_folder = output_folder_text.get()

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        process_albums_in_folder(self.input_folder, self.output_folder)


def set_album_art(mp3_file_path, jpg_file):
    audiofile = eyed3.load(mp3_file_path)
    if (audiofile.tag == None):
        audiofile.initTag()

    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(jpg_file,'rb').read(), 'image/jpeg')
    audiofile.tag.save()


def extract_album_art(mp3_file, output_folder):
    try:

       audio = MP3(mp3_file, ID3=ID3)
       if audio.tags is None:
            print("No ID3 tags found in the file.")
            return

       if audio.tags.version == eyed3.id3.ID3_V2_2:
           audio.tags.version = eyed3.id3.ID3_V2_3
           print("so far")
           audio.save()
           print("success?")

       for tag in audio.tags.values():
            if isinstance(tag, APIC):

                im = Image.open(io.BytesIO(tag.data))
                output_file = os.path.join(output_folder,
                               f"{os.path.splitext(os.path.basename(mp3_file))[0]}_cover.png")
                im.save(output_file, format='PNG')
                print(f"Album art saved as: {output_file}")
                return output_file

        #print("No album art found in the file.")

    except ID3NoHeaderError:
       print("The MP3 file does not have ID3 tags.")
    except Exception as e:
       print(f"An error occurred: {e}")


def get_ffmpeg_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'ffmpeg\\bin\\ffmpeg.exe')  # For Windows


def resize_art(jpg, album_path):
    print(jpg)
    image = Image.open(jpg)
    new_image = image.resize((250, 250))
    filename = 'current.png'
    file_path = os.path.join(album_path, filename)
    new_image.save(file_path, format='png')
    print("why isn't ths working")
    return file_path


def extract_album_art_flac(flac_path, output_folder):
    flac = FLAC(flac_path)
    pics = flac.pictures
    output_file = os.path.join(output_folder,
                               f"{os.path.splitext(os.path.basename(flac_path))[0]}_cover.png")
    for p in pics:
        if p.type == 3:  # front cover
            with open(output_file, "wb") as f:
                f.write(p.data)
                return output_file

    return "Error: no image found for " + flac_path


def set_album_art_flac(flac_file, image_file):
    """Sets the album art for a FLAC file."""

    # Load the FLAC file
    try:
        audio = FLAC(flac_file)
    except FileNotFoundError:
        print(f"Error: The file {flac_file} was not found.")
        return
    except ID3NoHeaderError:
        print(f"Error: The file {flac_file} is not a valid FLAC file.")
        return

    # Read the image file
    try:
        with open(image_file, 'rb') as f:
            image_data = f.read()
    except FileNotFoundError:
        print(f"Error: The image file {image_file} was not found.")
        return
    except Exception as e:
        print(f"Error reading image file: {e}")
        return

    # Create the Picture object
    picture = Picture()
    picture.data = image_data
    picture.mime = 'image/png'  # Change this if the image is not JPEG
    picture.desc = 'front cover'

    # Add the picture to the audio file
    audio.add_picture(picture)

    # Save changes to the FLAC file
    try:
        audio.save()
        print(f"Successfully set album art for {flac_file}.")
    except Exception as e:
        print(f"Error saving album art: {e}")

def copy_album_to_output(album_path, output_album_path):
    if not os.path.exists(output_album_path):
        os.makedirs(output_album_path)  # Create output album folder if it doesn't exist
        shutil.copytree(album_path, output_album_path, dirs_exist_ok=True)  # Copy album folder


def process_songs_in_album(album_path):

    for filename in os.listdir(album_path):
        file_path = os.path.join(album_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.mp3'):  # Check if it's a file
            print(file_path)
            print(album_path)
            jpg = extract_album_art(file_path, album_path)
            print(jpg)
            resized_jpg = resize_art(jpg, album_path)
            set_album_art(file_path, resized_jpg)
            os.remove(jpg)
            os.remove(resized_jpg)
        elif os.path.isfile(file_path) and filename.lower().endswith('.flac'):
            jpg = extract_album_art_flac(file_path, album_path)
            resized_jpg = resize_art(jpg, album_path)
            set_album_art_flac(file_path, resized_jpg)
            os.remove(jpg)
            os.remove(resized_jpg)


def process_albums_in_folder(albums_folder, output_folder):
        # List all folders in the albums folder
    for album_name in os.listdir(albums_folder):
        album_path = os.path.join(albums_folder, album_name)
        if os.path.isdir(album_path):  # Check if it's a directory
            output_album_path = os.path.join(output_folder, album_name)
            copy_album_to_output(album_path, output_album_path)
            process_songs_in_album(output_album_path)


def attach_image_to_audio_m4a(input_audio, input_image, output_audio):
    command = [
        'ffmpeg',
        '-i', input_audio,
        '-i', input_image,
        '-c', 'copy',
        '-disposition:v', 'attached_pic',
        output_audio
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully created {output_audio} with album art.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def convert_to_aac(input_file):
    sound = AudioSegment.from_file(input_file)
    sound.export("output-file.m4a", format="adts", bitrate="256k")


if __name__ == "__main__":

   #attach_image_to_audio("C:\\Users\\jackl\\Music\\correctedandresized\\Discovery\\01 One More Time.m4a", "C:\\Users\\jackl\\PycharmProjects\\AAC File Manager\\OUTPUT\\current.png", "output1.m4a")
   convert_to_aac("C:\\Users\\jackl\\Music\\Death Grips  - Bottomless Pit (320kbps mp3)\\02 - Hot Head.mp3")
   f = FolderSettings()
   root = Tk()
   root.title("MP3 Album Art Resizer")
   root.iconbitmap('MP3.ico')

   input_folder_text = tk.StringVar()
   output_folder_text = tk.StringVar()

   frm = tk.Frame(root, height=100, borderwidth=100, padx=10, pady=10)
   frm.grid()
   tk.Button(frm, text="Select Input Folder", command=f.select_input_folder).grid(column=0, row=1, sticky='W', padx=(5,10))
   tk.Button(frm, text="Select Output Folder", command=f.select_output_folder).grid(column=0, row=2, sticky='W', pady=(6, 0))
   tk.Button(frm, text="Convert Files", command=f.run_conversion).grid(column=0, row=3, pady=(6, 0))

   tk.Entry(frm, textvariable=input_folder_text, width=50).grid(column=1, row=1, columnspan=1)
   tk.Entry(frm, textvariable=output_folder_text, width=50).grid(column=1, row=2, columnspan=1, pady=(6, 0))

   root.mainloop()