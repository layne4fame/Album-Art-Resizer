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
                    img_file.write(tag.data)

                print(f"Album art saved as: {output_file}")
                return

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
        command = [ffmpeg_path, "-i", mp3_file, "-c:a", "aac", output_file]
        subprocess.run(command, check=True)
        print(f"Converted {mp3_file} to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    mp3_file = '11 Foreign.mp3'
    output_folder = 'new_folder'
    print(os.path.abspath(mp3_file))
    convert_mp3_to_aac(mp3_file, output_folder)
    extract_album_art(mp3_file, output_folder)




