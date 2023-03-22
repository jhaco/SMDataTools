Stepmania Data Tools is a Python library that rewrites functionality from [Stepmania File Parser](https://github.com/jhaco/SMFile_Parser) and [Stepmania File Writer](https://github.com/jhaco/SMFile_Writer) projects into one tool for extracting and converting note and timing data.

## Usage

### Command Line Tool

This library offers a command-line tool interface. All flags are optional, but at least one is needed to run the tool.

```bash
python smdatatools.py --parsetxt --parsesm --writetxt --writesm
```

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

### Options Overview

#### Parsing SM Files for Data using `--parsesm`

#### Writing Data to SM Files using `--writesm`

#### Parsing TXT Files for Data using `--parsetxt`

#### Writing Data to TXT Files using `--writetxt`
