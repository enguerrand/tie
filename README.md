# tie
Tags in exif-data - An image file tagger

## Overview
tie stands for tags in exif-data because it uses the exif data format to "tie" tags to image files.
The tag information is stored in a user-configurable exif field so that it does not get lost when tagged files are moved or modified.
For fast querying purposes an symlinks-based index is maintained automatically.

## Supported Platforms
tie has been written and tested on and for GNU/Linux. I have not tested any other platform.

## Dependencies
-python3
-exiv2
-gtk3
-ncurses

## Installation
Once the above-mentioned dependencies are fulfilled, simply clone this git repo to a directory of your choice.
The file tie.py at the root level is the executable to run.

## Usage
### Command line
Type
```
tie.py help
```
for information on how to run tie

### Graphical User Interface
tie does not have a standalone graphical user interface. It is meant to be integrated with existing tools.
I use it with file managers that allow me to add custom commands to the context menu.

As described in the help output, tie can be run without specifying tags, in which case the specified frontend will interactively ask the user for input.

So e.g. the following commands typically make sense as context menu entries for an image file(s) selection:
```
/path/to/tie.py tag -F gtk -f "$@"
/path/to/tie.py untag -F gtk -f "$@"
/path/to/tie.py list -F gtk -f "$@"
```
The above commands are all useful for tag data manipulation. In order for the querying feature to become useful, the query results must be viewable in a thumbnail overview. 
To achieve this, tie's querying output can be used to open an image viewer that accepts a file list as command line arguments.
I personally use gthumb. A sample script can be found in the "scripts" folder.
