#!/usr/bin/python

import os, sys, re, argparse

VERSION = 'v12.03'

presets = {}
presets['same'] = {'s':'same', 'b':{'high':'6000k', 'normal':'4000k', 'low':'2000k'}, 'ab':'128k'}
presets['1080p'] = {'s':'1920x1080', 'b':{'high':'8000k', 'normal':'6000k', 'low':'4000k'}, 'ab':'128k'}
presets['720p'] = {'s':'1280x720', 'b':{'high':'6000k', 'normal':'4000k', 'low':'2000k'}, 'ab':'128k'}
presets['480p'] = {'s':'854x480', 'b':{'high':'3000k', 'normal':'2000k', 'low':'1000k'}, 'ab':'128k'}
presets['360p'] = {'s':'640x360', 'b':{'high':'2000k', 'normal':'1000k', 'low':'500k'}, 'ab':'64k'}
presets['240p'] = {'s':'427x240', 'b':{'high':'1000k', 'normal':'500k', 'low':'300k'}, 'ab':'64k'}

formats = {}
formats['mp4'] = {'vcodec':'libx264', 'acodec':'aac', 'more_options':'-strict experimental -qmin 5 -async 50 -vpre libx264-medium -vpre libx264-baseline'}
formats['webm'] = {'vcodec':'libvpx', 'acodec':'libvorbis', 'more_options':''}

default_file_patterns = [
    '.mp4', '.MP4',
    '.webm', '.WEBM',
    '.mov', '.MOV',    
    '.flv', '.FLV',    
    '.m4v', '.M4V',    
    '.mkv', '.MKV',    
    '.mpeg', '.mpg', '.mpe', '.MPEG', '.MPG', '.MPE',    
    '.ogg', '.OGG',    
    '.wmv', '.WMV',    
    '.asf', '.ASF',    
    '.3gp', '.3GP'
]


def ffmpeg_convert(item_abs, format, frame_size, bitrate):
    ffmpeg = ""
    ffmpeg_presets = ""
    if sys.platform == "darwin":
        ffmpeg = os.path.join(data_root(), 'ffmpeg_osx', 'ffmpeg')
        ffmpeg_presets = os.path.join(data_root(), 'ffmpeg_osx', 'ffmpeg_presets')
    elif sys.platform == "win32":
        ffmpeg = os.path.join(data_root(), 'ffmpeg_win', 'ffmpeg.exe')
        ffmpeg_presets = os.path.join(data_root(), 'ffmpeg_win', 'ffmpeg_presets')
    elif sys.platform == "linux" or sys.platform == "linux2":
        ffmpeg = os.path.join(data_root(), 'ffmpeg_linux', 'ffmpeg')    
        ffmpeg_presets = os.path.join(data_root(), 'ffmpeg_linux', 'ffmpeg_presets')
        
    command = "export FFMPEG_DATADIR=" + ffmpeg_presets + "; "
    command += ffmpeg + " -threads 4 -i " + item_abs + " "
    command += "-vcodec " + formats[format]['vcodec'] + " "
    if frame_size != "same":
        command += "-s " + presets[frame_size]['s'] + " "
    if bitrate in ("high", "normal", "low"):
        command += "-b " + presets[frame_size]['b'][bitrate] + " "
    else:
        command += "-b " + bitrate + " "
    command += "-acodec " + formats[format]['acodec'] + " "
    command += "-ab " + presets[frame_size]['ab'] + " "
    command += "-ar 48000 -ac 2 "
    command += formats[format]['more_options'] + " "
    command += os.path.splitext(os.path.basename(item_abs))[0] + "." + format
    
    if args.debug:
        print command
    else:
        os.system(command)


def data_root():
    """This is to be used with all relative file access.
       _MEIPASS is a special location for data files when creating
       standalone, single file python apps with pyInstaller.
       Standalone is created by calling from 'other' directory:
       python pyinstaller/pyinstaller.py --onefile app.spec
    """
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        # root is one up from this file
        return os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


def filter_filenames(filenames, file_pattern, prefix_directory=""):
    matches = []
    for filename in filenames:
        if bool(re.search(file_pattern, filename)):
            matches.append(os.path.join(prefix_directory, filename))  
    return matches  

    
def match_recursive(directory, file_pattern):
    matches = []
    for directory, dirnames, filenames in os.walk(directory):
        matches += filter_filenames(filenames, file_pattern, directory)
    return matches


### Setup Argument Parser
argparser = argparse.ArgumentParser(description='Convert videos to common formats.', prog='videoowl')
argparser.add_argument('input_directory', metavar='input_directory', nargs='?', default='.',
                    help='input directory of video files to be converted')
argparser.add_argument('-p', '--pattern', dest='file_pattern', default='|'.join(default_file_patterns),
                        help='input file filter, regex-style (e.g: ".mov|.avi")')
argparser.add_argument('-f', '--format', dest='output_format', 
                        choices=['mp4', 'webm'], default='mp4',
                        help='video output format')
argparser.add_argument('-s', '--size', dest='size',
                        choices=presets.keys(), default='same',
                        help='video frame size')
argparser.add_argument('-b', '--bitrate', dest='bitrate',
                        default='normal',
                        help='video bitrate adjustment')
argparser.add_argument('-r', '--recursive', dest='recursive', action='store_true',
                    default=False, help='recursively traverse the subtree')
argparser.add_argument('-c', '--commit', dest='commit', action='store_true',
                    default=False, help='do not ask for confirmation before starting the conversion process')
argparser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    default=False, help='print out ffmpeg commands instead of executing')
argparser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
args = argparser.parse_args()


if args.input_directory:
    if os.path.isdir(args.input_directory):
        print "---[ videoowl ]---"
        print "Input file pattern --> " + args.file_pattern
        matched_files = []
        if args.recursive:
            print "Running recursively stating at --> " + args.input_directory
            matched_files = match_recursive(args.input_directory, args.file_pattern)
        else:
            print "Running non-recursively in --> " + args.input_directory
            filenames = [f for f in os.listdir(args.input_directory) if os.path.isfile(os.path.join(args.input_directory,f))]
            matched_files += filter_filenames(filenames, args.file_pattern, args.input_directory)                 
        print "Outputting to currently working directory --> " + os.getcwd()
        print "Converting the following files to --> " + args.size + " " + args.output_format + " (" + args.bitrate + " bitrate)"
        print "---"
        for mf in matched_files:
            print mf
        if not args.commit:
            ret = raw_input('Do you want to start converting? (y/n)')
            if not ret in 'yY':
                sys.exit()
        for mf in matched_files:
            ffmpeg_convert(mf, args.output_format, args.size, args.bitrate)                
                
    else:
        print "ERROR: invalid directory specified"
    print "------------------"





            
                
