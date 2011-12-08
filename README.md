KabalaOCR
==============

Tesseract langauge file for SuperMarket receipts :)

Setup a Tesseract environment
-----------------------------

**Ubuntu**

You will have to build the latest version of tesseract from source (version 3), since the
aptitude repositories hold an old version (v2.04).

* Download tesseract-3.01.tar.gz from http://code.google.com/p/tesseract-ocr/downloads/list
* Unpack it. (`tar -zvxf tesseract-3.01.tar.gz`)
* Compile tesseract:
    * `./autogen.sh` **NOTE**: Make sure you have libtoolize & GNU autotools installed.
    * `./configure`
    * `make`
    * `sudo make install`

**Mac OSX**

Oddly enough, homebrew hosts a newer version of tesseract (v3.0), which is good enough for us.

`brew install tesseract`


Interface & Commands
------------------------
The workflow is divided into two phases, the first one is manual and the second we automate:

* Phase 1
    * Create an image of your receipt
    * Convert the image to a b&w tif file
    * Save the image under the receipts directory in its proper place

* Phase 2
    * Generate a box file by running: `node create_box_file.js tif_file_name`
    * Fix the boxing results
    * Run: `coffee runner_command.coffee [reciepts dir path]`
