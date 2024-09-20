from mutagen.mp4 import MP4
from mutagen.mp4 import MP4Cover
from PIL import Image
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.id3 import APIC
import ffmpeg
import subprocess
import os


from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
from PIL import Image
import io


import eyed3
from eyed3.id3.frames import ImageFrame




def set_album_art(mp3_file_path, jpg_file):
   audiofile = eyed3.load(mp3_file_path)
   if (audiofile.tag == None):
       audiofile.initTag()


   audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(jpg_file,'rb').read(), 'image/jpeg')


   audiofile.tag.save()


'''
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
               # Create output file path
               output_file = os.path.join(output_folder,
                                          f"{os.path.splitext(os.path.basename(mp3_file))[0]}_cover.{tag.mime.split('/')[1]}")


               # Write the album art to a file
               with open(output_file, 'wb') as img_file:
                   image = Image.open(io.BytesIO(tag.data))
                   img_file.write(tag.data)


               print(f"Album art saved as: {output_file}")
               return output_file


       print("No album art found in the file.")


   except ID3NoHeaderError:
       print("The MP3 file does not have ID3 tags.")
   except Exception as e:
       print(f"An error occurred: {e}")
'''




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
   # Adjust path based on the current script location
   script_dir = os.path.dirname(os.path.abspath(__file__))
   return os.path.join(script_dir, 'ffmpeg\\bin\\ffmpeg.exe')  # For Windows




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
   print("test test")




if __name__ == "__main__":
   output_folder = 'new_folder'
   mp3_file_path = '03 - Spikes.mp3'  # Replace with your MP3 file path
   jpg = extract_album_art(mp3_file_path, output_folder)
   resize_art(jpg)


   set_album_art(mp3_file_path, 'tryagain.png')
   os.remove('tryagain.png')
   print("test")









