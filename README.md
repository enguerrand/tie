# tie
Tags in exif-data - An image file tagger

## Overview
*tie* stands for "tags in exif-data" because it uses the exif data format to "tie" tags to image files.
The tag information is stored in a user-configurable exif field.
For fast querying purposes a symlinks-based index is maintained automatically when tags are added or removed from files.
When files are renamed or moved externally, *tie* must be told to update its index.
This can be automated using the shellscript "tienotify.sh" in the scripts folder.

## Supported Platforms
*tie* has been written and tested on and for GNU/Linux. I have not tested any other platform.

## Dependencies
- python3
- exiv2
- gtk3
- ncurses

## Installation
Once the above-mentioned dependencies are fulfilled, simply clone this git repo to a directory of your choice.
The file tie.py at the root level is the executable to run.

## Usage
### Command line
Run
```
tie.py help
```
for information on how to run *tie*

### Frontends
#### Interactive Mode
Everything that *tie* can do can be done through the command line with one-liner commands. 
However, for it to be reasonably convenient to use from within graphical tools, *tie* is able to enter an interactive mode to request decisions from the user.

The way that this interactive mode behaves changes with the different available frontends.

*tie* enters the interactive mode whenever needed information was not provided through the command line arguments. 
The most notable use case is when the user runs a command that requires a tag selection but does not specify the wanted tags directly on the command line.
The interactive mode is also used to ask the user for confirmation before wiping present metadata that is incompatible with *tie*.

Thanks to this concept, many typical usecases can be covered with just a few generic command lines. These in turn can be added to filemanagers such as Thunar, Nemo or Xfe.
Gthumb also offers the possibility of adding custom commands.

So e.g. the following commands using the gtk frontend typically make sense as context menu entries for an image file(s) selection:
(Read "$@" as a placeholder for the selected files. In most above-mentioned tools the placeholder for this is %F)
```
/path/to/tie.py tag --frontend gtk --files "$@"
/path/to/tie.py untag --frontend gtk --files "$@"
/path/to/tie.py list --frontend gtk --files "$@"
```
The first two commands will open a gtk dialog that allows the user to select one or more tags which are then added to and removed from the selected files, respectively. 
The third will display all tags present in the selected files.

#### GTK Frontend Keyboard Shortcuts 
The GTK tag choice dialog has the following non-obvious keyboard shortcuts while the input field has focus:

| Shortcut    | Description |
| ----------- | ----------- |
| Enter       | Toggle the tag specified by the current input field content. Creates a new tag if necessary |
| Ctrl-Space  | Auto-complete the current text input |
| Ctrl-Enter  | Accept the current selection and close the dialog |

#### Querying
*tie* has no frontend for viewing query results. The idea is to let *tie* print out the list of files and use this output to open the query results in an image viewer.

I personally use gthumb. The script "scripts/query.sh" can be used to obtain a tags selection from the gtk frontend and run gthumb (or another image viewer) with the obtained selection.

## Additional Information
### Primary Goals / Motivation
Besides wanting to familiarize myself more with python I wrote *tie* to tag image files in a way that (in rough order of priority):
- makes it easy and robust to backup tag data along with the images and sync the tag data over different machines
- does not lock me into the use of a single program (especially not a proprietary one) to browse / view the images and query / manipulate the tag database
- does not require renaming files
- allows for fast querying of the tag database
- is fully scriptable / can be used in unix-style as part of command chains using find / grep / etc...
- has few deployment dependencies / follows the kiss principle

### Technical Concept
Every tagging tool that I've seen so far makes one compromise or another. 

The most notable compromise / limitation I was willing to accept for *tie* was limiting its use to file types supporting the exif file format.
The resulting benefit is that the tag data can be stored in the file, which reliably protects it from getting lost when the file is renamed, modified, copied or otherwise moved around, 
including transfers over the network.

In order to support fast querying an index is needed, but that index does not need to be backed up or synced between computers because it can be rebuilt at any time using 
the tag data present in the files. 
In order to keep the dependency footprint small, I decided to build this index using only symlinks.

The symlinks index is stored in a user-configurable directory where each tag has a subdirectory with symlinks to all tagged files. (Run *tie*'s help action for details)

As a result, one can view all files tagged with a given tag by simply opening this directory in a file manager. 
For more complex queries, *tie* can be used to print a path list which can be used as input to other tools as described above.