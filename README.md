Stepmania Data Tools is a Python library that rewrites functionality from [Stepmania File Parser](https://github.com/jhaco/SMFile_Parser) and [Stepmania File Writer](https://github.com/jhaco/SMFile_Writer) projects into one tool for extracting and converting note and timing data. Used with cpuguy96's [StepCOVNet](https://github.com/cpuguy96/StepCOVNet).

## Usage

### Command Line Tool

This library offers a command-line tool interface. All flags are optional, but at least one is needed to run the tool.

```bash
python smdatatools.py --parsetxt --parsesm --writetxt --writesm
```

Directories specified in either 'config.ini' or through the command-line must exist as the tool will not generate one on its own.

By default, the tool will use directories specified within `config.ini`. Users will have the option to override these by appending a directory to its corresponding flag in the command-line:

##### Example 1:

```bash
python smdatatools.py --parsetxt <input-txt-dir>
```

##### Example 2: overriding multiple flags

```bash
python smdatatools.py --parsesm <input-sm-dir> --writetxt <output-txt-dir>
```

##### Example 3: overriding all but one flag

```bash
python smdatatools.py --parsesm <input-sm-dir> --writetxt <output-txt-dir> --writesm
```

`-ps` `--parsesm` Parses .sm files for note data

`-ws` `--writesm` Writes converted data to playable .sm files

`-pt` `--parsetxt` Parses .txt files for note data

`-wt` `--writetxt` Writes raw data to .txt files

`-c` `--copyaudio` Copies audio files for successfully parsed data to a directory

### Options Overview

#### Parsing SM Files for Data using `--parsesm`

A Stepmania simfile, or .sm file, contains note data necessary to play its corresponding song in [Stepmania](https://www.stepmania.com). Simfiles are always paired with a .ogg or .mp3 file, and usually found zipped with a collection of other songs. More information on acquiring songs can be found [here](https://www.reddit.com/r/Stepmania/comments/5jfwvh/looking_for_more_song_packs_your_moderator/).

When using this tool to parse a directory for .sm files, users can drop the entire unzipped song pack and it will automatically collect all the .sm files available for parsing.

The resultant data from parsing will contain a series of notes and their actual timings in seconds, calculated from their positions, BPM, and offset.

Note: Currently, the tool only supports parsing songs with static BPMs, so not all .sm files will be considered for data extraction.

#### Writing Data to SM Files using `--writesm`

Writing to an .sm file allows users to created playable simfiles from parsed data. 

Note: Due to no easy way to extrapolate the original offset from just note timings and positions, a parsed .sm file with offset may come out differently from a .sm file written by this tool, despite using the same data.

#### Writing Data to TXT Files using `--writetxt`

This tool allows users to write the data parsed from .sm files to .txt for later use.

The .txt file generated by this tool will contain the song name, bpm, and at least one difficulty with a series of notes and timings for each. This can then be used to train models focused on note placements and timings for songs, or parsed again to convert to a playable .sm file.

#### Parsing TXT Files for Data using `--parsetxt`

When using this tool to parse .txt files, users will need to make sure to include the title, bpm, its difficulty levels and their note and note timings.

Once parsed, the resultant data can be rewritten to other .txt files, or converted and written as playable .sm files.

#### Copying Audio for Data using `--copyaudio`

When using this command, the tool will copy the existing audio files for all parsed data into one directory. 

Like the other commands, users can override config defaults by adding their own directory after this command.
