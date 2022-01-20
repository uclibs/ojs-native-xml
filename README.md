# OJS NativeXML Conversion Script


## Usage

On the command line:

`$ python3 convert.py [input_filename.csv]`

## Input File

csv file format, comma-delimited, utf8 encoding

## Interactive user input
Script prompts user to input these data points at run-time.

* "Please input issue title and press enter: " 
> Optional.

* "Please input volume number and press enter: "
> Required; must be integer

* "Please input issue number and press enter: "
> Required; must be integer.

* "Please input issue year and press enter: "
> Required; Format YYYY

* "Please type output file name and press enter: "
> Required; XML format; Enter full path to output file e.g. `/tmp/outputfile.xml`

* "Please type full file path for galleys and press enter: "
> Required; PDF galley path/location e.g. `/tmp/Files`

## Fields

* authors
> Required; Format author name as` "last_name, first_name"`. Group multiple authors in one column and seperate with semicolon.

* keywords
> Optional; Group keywords in single column and seperate with commas.

* title
> Required.

* abstract
> Optional.

* copyright
> Optional.

* galley
> Name of file for upload, include name with extension e.g. "article_example1.pdf"

* section
> Required; Use abbreviation codes e.g. "ART" for Article section.


## Wrinkles

* File mimetypes are hard-coded as "application/pdf". Other types will require source code change
* Section definitions are hard-coded in the script, change in the source code.
