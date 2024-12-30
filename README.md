# Album Art Resizer

**Album Art Resizer** is a simple, open-source application designed to resize album art for music files. Currently, it supports **MP3** and **FLAC** formats.

## Purpose

This application was created as a free, straightforward solution for resizing album art in bulk to:

- Reduce overall file sizes.
- Improve compatibility with low-powered portable music devices with limited storage.
- Optimize performance for devices like iPods by reducing metadata size, minimizing playback skipping and stalling.

## Features

- Batch resizing of album art for MP3 and FLAC files.
- Allows users to specify input and output folders for processing.
- Resized files are stored in the specified output folder.

## Current Limitations

- MP3 to AAC conversions are not fully supported as metadata is not properly transferred. 

## Usage

1. Navigate to the `/dist` folder to find the executable.
2. Run the application.
3. Select an input folder containing MP3 or FLAC files.
4. Select an output folder where resized files will be saved.
5. Start the resizing process.

## Future Enhancements

- Support for MP3 to AAC conversions with proper metadata transfer.
- Additional format support and advanced customization options.
