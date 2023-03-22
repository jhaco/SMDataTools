## SMDataTools
###### Stepmania Data Tools compiles the [Stepmania File Parser](https://github.com/jhaco/SMFile_Parser) and [Stepmania File Writer](https://github.com/jhaco/SMFile_Writer) scripts into one. Refer to either scripts' README for more information.

`python smdatatools.py [--parsetxt "txt_dir (opt)"] [--parsesm "sm_dir (opt)"] [--writetxt "txt_dir (opt)"] [--writesm "sm_dir (opt)"]`

#### Notes: 

- Added DataHandler class to store note data. Each handler will represent data from one .sm or .txt file.
- Multiple CLI options can be used at once, allowing the tool to run them all. Each option will always run in a specific order.
- Input and output directories should be specified in config.ini file for each script.
- Config settings can be overridden by providing a directory with any CLI option.
- If a CLI option is used without providing a directory, the tool will use the value specified in config.ini.

---

<details close>
  <summary>Changelog</summary>
        
  Sorted by most recent:
  
  - added ability to override config options through the command line
  - refactored code to decouple large code blocks into smaller distinct components, improving modularity
  - logged console output to file, reducing avg runtime by 15%: from 20s to 17s for ~200 files
  - added error message for unpaired .sm/sound files; added count for successfully processed files
  - fixed error message; ensured note data matches the 4-note dance-singles mode, not 8-note dance-doubles
  - added configuration file to reduce tedium in specifying input/output folders
  
</details>
