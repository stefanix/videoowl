
Videoowl is a video converter that can take almost any video file and transcode it to mp4 or webm. The supported output frame resolutions are 240p, 360p, 480p, 720p, 1080p (all 1.77:1) or 'same' which simply takes the resolution of the input file.

Input files are selected by providing a directory and a regex pattern. Optionally videoowl also traverses (option -r) all sub-directores and picks files based on the regex pattern. By default it picks most video formats.

Output files are currently written into the directory from which videoowl is called.

### Examples

- `videoowl`
  - converts all video files in the current directory to 480p mp4
- `videoowl -s 720p -f webm -b high`
  - converts all videos in the current directory to 720p webm (at higher than normal quality)
- `videoowl -r -p ".avi|.mov" videos/`
  - converts recursively videos in the videos/ directory that contain ".avi" or ".mov" in the file name (also defaults to 480p mp4)


Installation
------------

From the [downloads section](https://github.com/stefanix/videoowl/downloads) get the OSX installer and run it. VideoOwl will be installed as one file here: /usr/local/bin/videoowl. This is part of the search path which means videoowl can be executed from anywhere in the Terminal.

To uninstall simply delete /usr/local/bin/videoowl.



Usage
-------

<pre>
usage: videoowl [-h] [-p FILE_PATTERN] [-f {mp4,webm}]
                [-s {480p,360p,720p,same,240p,1080p}] [-b BITRATE] [-r] [-c]
                [-d] [-v]
                [input_directory]

Convert videos to common formats.

positional arguments:
  input_directory       input directory of video files to be converted

optional arguments:
  -h, --help            show this help message and exit
  -p FILE_PATTERN, --pattern FILE_PATTERN
                        input file filter, regex-style (e.g: ".mov|.avi")
  -f {mp4,webm}, --format {mp4,webm}
                        video output format
  -s {480p,360p,720p,same,240p,1080p}, --size {480p,360p,720p,same,240p,1080p}
                        video frame size
  -b BITRATE, --bitrate BITRATE
                        video bitrate adjustment
  -r, --recursive       recursively traverse the subtree
  -c, --commit          do not ask for confirmation before starting the
                        conversion process
  -d, --debug           print out ffmpeg commands instead of executing
  -v, --version         show program's version number and exit  
</pre>



License
--------

Videoowl is released under the GPL v3 and  the bundled ffmpeg is LGPL v2.1.