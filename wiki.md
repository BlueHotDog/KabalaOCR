JSON
========
Receipts file convention

receipts/
	[supermarket]/
    processed
  		kabalalang.[supermarket].[id].tiff
  		kabalalang.[supermarket].[id].box
    new
      blah.jpg


cake box -> [convert,box(on the new folder)] -> creates a pair of blah.tiff(in grayscale) and blah.box

create a .gitignore that ignores the .box files in the new directory

      