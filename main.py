import subprocess
import os
import shutil
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
from PIL import Image
import io
import tkinter as tk
from tkinter import filedialog
import eyed3
from eyed3.id3.frames import ImageFrame


def set_album_art(mp3_file_path, jpg_file):
   audiofile = eyed3.load(mp3_file_path)
   if (audiofile.tag == None):
       audiofile.initTag()

   audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(jpg_file,'rb').read(), 'image/jpeg')
   audiofile.tag.save()


def extract_album_art(mp3_file, output_folder):
   try:
       # Load the MP3 file
       audio = MP3(mp3_file, ID3=ID3)


       # Check for ID3 tags
       if audio.tags is None:
           print("No ID3 tags found in the file.")
           return


       # Find and save the album art
       for tag in audio.tags.values():
           if isinstance(tag, APIC):
               # Load the album art into a PIL image
               image = Image.open(io.BytesIO(tag.data))


               # Create output file path with .png extension
               output_file = os.path.join(output_folder,
                                          f"{os.path.splitext(os.path.basename(mp3_file))[0]}_cover.png")


               # Save the image as PNG
               image.save(output_file, format='PNG')


               print(f"Album art saved as: {output_file}")
               return output_file


       print("No album art found in the file.")


   except ID3NoHeaderError:
       print("The MP3 file does not have ID3 tags.")
   except Exception as e:
       print(f"An error occurred: {e}")


def get_ffmpeg_path():
   script_dir = os.path.dirname(os.path.abspath(__file__))
   return os.path.join(script_dir, 'ffmpeg\\bin\\ffmpeg.exe')  # For Windows


# Not really a useful function now because of issues with converting an MP3 to AAC with album art meta-data
# causing really big issues. May work further on it but isn't the ethos of the project
def convert_mp3_to_aac(mp3_file, output_folder):
   try:
       ffmpeg_path = get_ffmpeg_path()  # Get the FFmpeg path
       output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(mp3_file))[0]}.m4a")
       command = [ffmpeg_path, "-i", mp3_file, "-map", "0:a", "-c:a", "aac", "-map_metadata", "-1", output_file]
       subprocess.run(command, check=True)
       print(f"Converted {mp3_file} to {output_file}")

   except subprocess.CalledProcessError as e:
       print(f"An error occurred: {e}")
   except Exception as e:
       print(f"An error occurred: {e}")


def resize_art(jpg):
   image = Image.open(jpg)
   new_image = image.resize((250, 250))
   new_image.save('tryagain.png', format='png')


def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path


def copy_album_to_output(album_path, output_album_path):
    if not os.path.exists(output_album_path):
        os.makedirs(output_album_path)  # Create output album folder if it doesn't exist
    shutil.copytree(album_path, output_album_path, dirs_exist_ok=True)  # Copy album folder


def process_songs_in_album(album_path):

    for filename in os.listdir(album_path):
        file_path = os.path.join(album_path, filename)
        if os.path.isfile(file_path):  # Check if it's a file
            print(f"Processing song: {file_path}")
            # Add your song processing logic here


def process_albums_in_folder(albums_folder, output_folder):
    # List all folders in the albums folder
    for album_name in os.listdir(albums_folder):
        album_path = os.path.join(albums_folder, album_name)
        if os.path.isdir(album_path):  # Check if it's a directory
            output_album_path = os.path.join(output_folder, album_name)
            copy_album_to_output(album_path, output_album_path)
            process_songs_in_album(output_album_path)


if __name__ == "__main__":

   selected_folder = select_folder()
   output_folder = selected_folder + 'OUTPUT'
   if not os.path.exists(output_folder):
       os.makedirs(output_folder)
   process_albums_in_folder(selected_folder, output_folder)

'''
   output_folder = 'new_folder'
   mp3_file_path = '03 - Spikes.mp3'  # Replace with your MP3 file path
   jpg = extract_album_art(mp3_file_path, output_folder)
   resize_art(jpg)

   set_album_art(mp3_file_path, 'tryagain.png')
   os.remove('tryagain.png')
   print("test")
'''








