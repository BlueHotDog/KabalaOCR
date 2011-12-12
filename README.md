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
* Before proceeding to the next step, make sure you have the following packages:
    * `sudo apt-get install autoconf automake libtool`
    * `sudo apt-get install libpng12-dev`
    * `sudo apt-get install libjpeg62-dev`
    * `sudo apt-get install libtiff4-dev`
    * `sudo apt-get install zlib1g-dev`
    * `sudo apt-get install libleptonica-dev`
* Compile tesseract:
    * `./autogen.sh`
    * `./configure`
    **NOTE:** In case you will get an error about leptonica, you will have to do the following:
        * `sudo apt-get remove libleptonica-dev`
        * `wget http://www.leptonica.com/source/leptonica-1.68.tar.gz`
        * After installing leptonica, try running `./configure` for tesseract again.
    * `make`
    * `sudo make install`
    * `sudo ldconfig`

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
