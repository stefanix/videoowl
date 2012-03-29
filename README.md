

Usage
-------
usage: videoowl [-h] [-p FILE_PATTERN] [-f {mp4,webm}]
                [-s {480p,720p,1080p,240p,360p}] [-b {high,normal,low}] [-r]
                [-c] [-d] [-v]
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
  -s {480p,720p,1080p,240p,360p}, --size {480p,720p,1080p,240p,360p}
                        video frame size
  -b {high,normal,low}, --bitrate {high,normal,low}
                        video bitrate adjustment
  -r, --recursive       recursively traverse the subtree
  -c, --commit          do not ask for confirmation before starting the
                        conversion process
  -d, --debug           print out ffmpeg commands instead of executing
  -v, --version         show program's version number and exit