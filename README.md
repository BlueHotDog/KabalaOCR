KabalaOCR
==============

An attempt to create an Tesseract langauge file for SuperMarket receipts :)

Interface & Commands
------------------------
The workflow is divided into two phases, the first one is manual and the second we automate:
*
	* Create an image of your receipt
	* Convert the image to a b&w tif file
	* Save the image under the receipts directory in its proper place
*
	* Generate a box file by running: node create_box_file.js tif_file_name
    * Fix the boxing results
	* Run: coffee runner_command.coffee [reciepts dir path]
