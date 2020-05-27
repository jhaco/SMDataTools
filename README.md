## SMDataTools
###### Stepmania Data Tools compiles the [Stepmania File Parser](https://github.com/jhaco/SMFile_Parser) and [Stepmania File Writer](https://github.com/jhaco/SMFile_Writer) scripts into one. Refer to either scripts' README for more information.

`python stepmania_data_tools.py [collect/write]`

#### Notes: 

- Input and output directories must be specified in config.ini file for each script.

###### SMParser is redefined as "collect" in Stepmania Data Tools.

---

<details close>
  <summary>Changelog</summary>
        
  Sorted by most recent:
  
  - logged console output to file, reducing avg runtime by 15%: from 20s to 17s for ~200 files
  - added error message for unpaired .sm/sound files; added count for successfully processed files
  - fixed error message; ensured note data matches the 4-note dance-singles mode, not 8-note dance-doubles
  - added configuration file to reduce tedium in specifying input/output folders
  
</details>
