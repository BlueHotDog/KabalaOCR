#!/usr/bin/python
# -*- coding: utf-8 -*-

# pyTesseractTrainer is editor for tesseract-ocr box files.
# pyTesseractTrainer is successor of tesseractTrainer.py
#
# More information about project can be found on project page:
# http://pytesseracttrainer.googlecode.com
#
# pyTesseractTrainer.py
# Copyright 2010 Zdenko Podobný <zdenop at gmail.com>
# http://pytesseracttrainer.googlecode.com
# http://sk-spell.sk.cx
#
# tesseractBoxEditor.py
# Modified version for work with djvused
# Modified by Mihail Radu Solcan
# Last modification: 2008-12-28
#
# tesseractTrainer.py
# Copyright 2007 Catalin Francu <cata at francu.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.#}}}
"""
pyTesseractTrainer is editor for tesseract-ocr box files.
pyTesseractTrainer is successor of tesseractTrainer.py
"""
import pygtk
pygtk.require('2.0')
import gtk
import pango
import sys
import os
import shutil
import codecs
from time import clock, sleep
from datetime import datetime

# parameters
VERSION = '1.03'
REVISION = '50'
SAVE_FORMAT = 3  # tesseract v3 box format
BASE_FONT = 'Sans'
DEBUG_SPEED = 0
VERBOSE = 0  # if 1, than print additional information to standrard output

MENU = \
    '''<ui>
  <menubar name="MenuBar">
    <menu action="File">
      <menuitem action="Open"/>
      <menuitem action="MergeText"/>
      <menuitem action="Save"/>
      <menuitem action="Quit"/>
    </menu>
    <menu action="Edit">
      <menuitem action="Copy"/>
      <menuitem action="djvMap"/>
      <menuitem action="htmMap"/>
      <separator/>
      <menuitem action="Split"/>
      <menuitem action="JoinWithNext"/>
      <menuitem action="Delete"/>
    </menu>
    <menu action="Help">
      <menuitem action="About"/>
      <menuitem action="AboutMergeText"/>
      <menuitem action="Shortcuts"/>
    </menu>
  </menubar>
</ui>'''

ATTR_BOLD = 0
ATTR_ITALIC = 1
ATTR_UNDERLINE = 2

DIR_LEFT = 0
DIR_RIGHT = 1
DIR_TOP = 2
DIR_BOTTOM = 3
DIR_RUP = 4
DIR_LDOWN = 5


class Symbol:
    '''class symbol '''
    text = ''
    left = 0
    right = 0
    top = 0
    rightup = 0
    bottom = 0
    leftdown = 0
    page = 0
    bold = False
    italic = False
    underline = False
    spaceBefore = False
    entry = None
    handlers = []


    def setEntryFont(self):
        font = BASE_FONT
        if self.bold:
            font += ' bold'

        # endif

        if self.italic:
            font += ' italic'

        # endif

        self.entry.modify_font(pango.FontDescription(font))

        if self.underline:
            self.entry.set_width_chars(len(unicode(self.text)) + 1)
            self.entry.set_text("'" + self.text)
        else:
            self.entry.set_width_chars(len(unicode(self.text)))
            self.entry.set_text(self.text)

        # endif
    # enddef


    def clone(self):
        s = Symbol()
        s.text = self.text
        s.left = self.left
        s.right = self.right
        s.top = self.top
        s.bottom = self.bottom
        s.page = self.page
        s.rightup = self.rightup
        s.leftdown = self.leftdown
        s.bold = self.bold
        s.italic = self.italic
        s.underline = self.underline
        s.spaceBefore = self.spaceBefore
        s.entry = self.entry
        s.handlers = self.handlers
        return s

    # enddef


    def deleteLabelBefore(self):
        e = self.entry
        box = e.get_parent()
        pos = box.child_get_property(e, 'position')
        label = box.get_children()[pos - 1]
        label.destroy()

    # enddef


    def __str__(self):
        return 'Text [%s] L%d R%d T%d B%d P%d LD%d RU%d' % (self.text,
                self.left, self.right, self.top, self.bottom, self.page,
                self.leftdown,  self.rightup)

    # enddef
# endclass

def safe_backup(path, keep_original=True):
    """
    Rename a file or directory safely without overwriting an existing 
    backup of the same name.
    http://www.5dollarwhitebox.org/drupal/node/91
    """
    count = -1
    new_path = None
    while True:
        if os.path.exists(path):
            if count == -1:
                new_path = "%s.bak" % (path)
            else:
                new_path = "%s.bak.%s" % (path, count)
            if os.path.exists(new_path):
                count += 1
                continue
            else:
                if keep_original:
                    if os.path.isfile(path):
                        shutil.copy(path, new_path)
                    elif os.path.isdir(path):
                        shutil.copytree(path, new_path)
                else:
                    shutil.move(path, new_path)
                break
        else:
            break
    return new_path

def find_format(boxname):
    ''''find format of box file'''
    expected_format = 0  # expected number of items
    wrong_row = ""  # here will be list of wrong rows
    wrong_fl = False  # even first line is wrong 
                      # so we can not use it for expected format
    row = 1

    fbn = open(boxname,'r') 
    for line in fbn:
        nmbr_items = len(line.split())
        if row == 1 and (nmbr_items == 5 or nmbr_items == 6):
            expected_format = nmbr_items
        elif row == 1 and (nmbr_items != 5 or nmbr_items != 6):
            wrong_fl = True
        if nmbr_items != expected_format:
            wrong_row = wrong_row + str(row) + ", "
        row += 1
    fbn.close()

    if wrong_row == "":  # file is ok - it has only one format
        if expected_format == 5:
            if VERBOSE > 0:
                print datetime.now(), 'Find tesseract 2 box file.'
            return 2
        if expected_format == 6:
            if VERBOSE > 0:
                print datetime.now(), 'Find tesseract 3 box file.'
            return 3
    else:  # there lines with different formats!!!
        message = "Wrong format of '%s'." % boxname
        if wrong_fl:
            message =  message + " Even first line is not correct!"
        else:
            message =  message + " Please check these rows: '%s'." \
                % wrong_row[:-2]

        dialog = gtk.MessageDialog(parent=None,
                buttons=gtk.BUTTONS_CLOSE,
                flags=gtk.DIALOG_DESTROY_WITH_PARENT,
                type=gtk.MESSAGE_WARNING, message_format=message)
        dialog.set_title('Error in box file!')
        dialog.run()
        dialog.destroy()
        return -1 # wrong format of box file


def loadBoxData(boxname, height):
    '''Returns a list of lines. Each line contains a list of symbols
    FIELD_* constants.'''

    open_format = find_format(boxname)

    if open_format == -1:
        return -1 # wrong format of box file

    fbn = codecs.open(boxname, 'r', 'utf-8')
    if VERBOSE > 0:
        print datetime.now(), 'File %s is opened.' % boxname
    result = []
    symbolLine = []
    prevRight = -1
    page = 0

    for line in fbn:
        if open_format == 3:
            (text, left, bottom, right, top, page) = line.split()
        elif open_format == 2:
            (text, left, bottom, right, top) = line.split()

        s = Symbol()

        # if there is more than 1 symbols in text, check for:
        # bold, italic, underline

        if len(text) > 1:
            if '@' in text[:1]:
                s.bold = True
                text = text.replace('@', '', 1)

            # endif

            if '$' in text[:1]:
                s.italic = True
                text = text.replace('$', '', 1)

            # endif

            if "'" in text[:1]:
                s.underline = True
                text = text.replace("'", '', 1)

            # endif
        # endif

        s.text = text
        s.left = int(left)
        s.right = int(right)
        # initial values for y coords as in tesseract
        s.rightup = int(top)
        s.leftdown = int(bottom)
        # end initial values        
        s.top = height - s.rightup
        s.bottom = height - s.leftdown
        s.page = int(page)

        s.spaceBefore = s.left >= prevRight + 6 and prevRight != -1

        if s.left < prevRight - 10:
            result.append(symbolLine)
            symbolLine = []

        # endif

        symbolLine.append(s)
        prevRight = s.right

    # endfor

    result.append(symbolLine)
    fbn.close()
    return result

# enddef


def ensureVisible(adjustment, start, size):
    '''
    Ensures that the adjustment is set to include the range of size "size"
    starting at "start"
    '''
    # Compute the visible range
    visLo = adjustment.value
    visHi = adjustment.value + adjustment.page_size
    if start <= visLo or start + size >= visHi:
        desired = start - (adjustment.page_size - size) / 2
        if desired < 0:
            desired = 0
        elif desired + adjustment.page_size >= adjustment.upper:
            desired = adjustment.upper - adjustment.page_size

        # endif

        adjustment.set_value(desired)

    # endif
# enddef



def countBlackPixels(pixels, x):
    '''Counts all the black pixels in column x'''

    numPixels = 0
    for row in pixels:
        if isBlack(row[x]):
            numPixels += 1

      # endif
    # endfor

    return numPixels

# enddef



def isBlack(pixel):
    return pixel[0][0] + pixel[1][0] + pixel[2][0] < 128 * 3

# enddef


class MainWindow:

    pixbuf = None
    selectedRow = None
    selectedColumn = None
    buttonUpdateInProgress = None
    boxes = None


    def reconnectEntries(self, rowIndex):
        row = self.boxes[rowIndex]
        for col in range(0, len(row)):
            e = row[col].entry
            for handler in row[col].handlers:
                e.disconnect(handler)

            # endfor

            row[col].handlers = [e.connect('focus-in-event',
                                 self.onEntryFocus, rowIndex, col),
                                 e.connect('changed',
                                 self.onEntryChanged, rowIndex, col),
                                 e.connect('key-press-event',
                                 self.onEntryKeyPress, rowIndex, col)]

        # endfor
    # enddef


    def errorDialog(self, labelText, parent):
        dialog = gtk.Dialog('Error', parent, gtk.DIALOG_NO_SEPARATOR
                            | gtk.DIALOG_MODAL, (gtk.STOCK_OK,
                            gtk.RESPONSE_OK))
        label = gtk.Label(labelText)
        dialog.vbox.pack_start(label, True, True, 0)
        label.show()
        dialog.run()
        dialog.destroy()

    # enddef


    def makeGtkEntry( self, symbol, row, col):
        if VERBOSE > 1:
            print datetime.now(), \
            u"symbol: '', row: '%s', col: '%s', page: '%s'" \
                % (row, col, symbol.page)
        symbol.entry = gtk.Entry()
        symbol.handlers = [symbol.entry.connect('focus-in-event',
                           self.onEntryFocus, row, col),
                           symbol.entry.connect('changed',
                           self.onEntryChanged, row, col),
                           symbol.entry.connect('key-press-event',
                           self.onEntryKeyPress, row, col)]

    # enddef


    def invalidateImage(self):
        '''refresh image'''
        (width, height) = self.drawingArea.window.get_size()
        self.drawingArea.window.invalidate_rect((0, 0, width, height),
                False)

    # enddef


    def onCheckButtonToggled(self, widget, attr):
        '''Set atribut to symbol'''
        if self.buttonUpdateInProgress or self.selectedRow == None:
            return

        # endif

        value = widget.get_active()
        symbol = self.boxes[self.selectedRow][self.selectedColumn]
        if attr == ATTR_BOLD:
            symbol.bold = value
        elif attr == ATTR_ITALIC:
            symbol.italic = value
        elif attr == ATTR_UNDERLINE:
            symbol.underline = value

        # endif

        symbol.setEntryFont()

        # The underline attribute does not apply to the entire word

        if attr == ATTR_UNDERLINE:
            return

        # endif

        row = self.boxes[self.selectedRow]
        i = self.selectedColumn - 1
        while i >= 0 and not row[i + 1].spaceBefore:
            if attr == ATTR_BOLD:
                row[i].bold = value
            elif attr == ATTR_ITALIC:
                row[i].italic = value

            # endif

            row[i].setEntryFont()
            i -= 1

        # endwhile

        i = self.selectedColumn + 1
        while i < len(row) and not row[i].spaceBefore:
            if attr == ATTR_BOLD:
                row[i].bold = value
            elif attr == ATTR_ITALIC:
                row[i].italic = value

            # endif

            row[i].setEntryFont()
            i += 1

        # endwhile
    # enddef


    def onEntryFocus(self, entry, ignored, row, column):
        self.selectedRow = row
        self.selectedColumn = column

        # Force the image to refresh

        self.invalidateImage()

        # Bring the rectangle into view if necessary

        s = self.boxes[row][column]
        width = s.right - s.left
        height = s.bottom - s.top
        ensureVisible(self.scrolledWindow.get_hadjustment(), s.left,
                      width)
        ensureVisible(self.scrolledWindow.get_vadjustment(), s.top,
                      height)
        # ensureVisible(self.textScroll.get_hadjustment(), s.left,
                      # width)
        # ensureVisible(self.textScroll.get_vadjustment(), s.top,
                      # height)

        # Activate the formatting checkboxes and set their values

        self.setSymbolControlSensitivity(True)
        self.buttonUpdateInProgress = True
        self.boldButton.set_active(s.bold)
        self.italicButton.set_active(s.italic)
        self.underlineButton.set_active(s.underline)

        # Set adjustments/limits on all spin buttons
        i_height = self.pixbuf.get_height()
        i_width = self.pixbuf.get_width()
        self.spinLeft.set_adjustment(gtk.Adjustment(0, 0, s.right, 1, 10))
        self.spinRight.set_adjustment(gtk.Adjustment(0, s.left, i_width, 1, 10))
        self.spinTop.set_adjustment(gtk.Adjustment(0, 0, s.bottom, 1, 10))
        self.spinRUp.set_adjustment(gtk.Adjustment(0, s.leftdown, i_height,
                                                   1, 10))
        self.spinBottom.set_adjustment(gtk.Adjustment(0, s.top, i_height,
                                                      1, 10))
        self.spinLDown.set_adjustment(gtk.Adjustment(0, 0, s.rightup, 1, 10))

        # Update the spin buttons
        self.spinLeft.set_value(s.left)
        self.spinRight.set_value(s.right)
        self.spinTop.set_value(s.top)
        self.spinRUp.set_value(s.rightup)
        self.spinBottom.set_value(s.bottom)
        self.spinLDown.set_value(s.leftdown)

        self.buttonUpdateInProgress = None

    # enddef


    def onEntryChanged(self, entry, row, col):
        symbol = self.boxes[row][col]
        symbol.text = entry.get_text()
        symbol.underline = symbol.text.startswith("'")
        entry.set_width_chars(len(unicode(symbol.text)))
        while symbol.text.startswith("'"):
            symbol.text = symbol.text[1:]

        # endwhile

        self.buttonUpdateInProgress = True
        self.underlineButton.set_active(symbol.underline)
        self.buttonUpdateInProgress = None

    # enddef

    # Intercept ctrl-arrow and ctrl-shift-arrow


    def onEntryKeyPress(self, entry, event, row, col):
        if not event.state & gtk.gdk.CONTROL_MASK:
            return False

        # endif

        shift = event.state & gtk.gdk.SHIFT_MASK
        s = self.boxes[row][col]
        if event.keyval == 65361:  # Left arrow
            self.buttonUpdateInProgress = True
            if shift:
                s.left += 1
            else:
                s.left -= 1
            self.spinLeft.set_value(s.left)
            self.buttonUpdateInProgress = None
            self.invalidateImage()
            return True
        elif event.keyval == 65362:  # Up arrow
            self.buttonUpdateInProgress = True
            if shift:
                s.top += 1
                s.rightup -= 1
            else:
                s.top -= 1
                s.rightup += 1
            self.spinTop.set_value(s.top)
            self.spinRUp.set_value(s.rightup)
            self.spinTop.set_value(s.top)
            self.buttonUpdateInProgress = None
            self.invalidateImage()
            return True
        elif event.keyval == 65363:  # Right arrow

            self.buttonUpdateInProgress = True
            if shift:
                s.right -= 1
            else:
                s.right += 1
            self.spinRight.set_value(s.right)
            self.buttonUpdateInProgress = None
            self.invalidateImage()
            return True
        elif event.keyval == 65364:  # Down arrow
            self.buttonUpdateInProgress = True
            if shift:
                s.bottom -= 1
                s.leftdown += 1
            else:
                s.bottom += 1
                s.leftdown -= 1
            self.spinBottom.set_value(s.bottom)
            self.spinLDown.set_value(s.leftdown)
            self.buttonUpdateInProgress = None
            self.invalidateImage()
            return True

        # endif

        return False

    # enddef


    def onSpinButtonChanged(self, button, dir):
        if self.buttonUpdateInProgress or self.selectedRow == None:
            return

        # endif

        value = int(button.get_value())
        s = self.boxes[self.selectedRow][self.selectedColumn]
        prevValue = (s.left, s.right, s.top, s.bottom, s.rightup, \
                     s.leftdown)[dir]
        i_height = self.pixbuf.get_height()
        i_width = self.pixbuf.get_width()

        if dir == DIR_LEFT:
            s.left = value
            self.spinRight.set_adjustment(gtk.Adjustment(s.right, s.left,
                                                         i_width, 1, 10))
        elif dir == DIR_RIGHT:
            s.right = value
            self.spinLeft.set_adjustment(gtk.Adjustment(s.left, 0, 
                                                        s.right, 1, 10))
        elif dir == DIR_TOP:
            s.top = value
            s.rightup = s.rightup + prevValue - value
            self.spinRUp.set_value(s.rightup)
            self.spinBottom.set_adjustment(gtk.Adjustment(s.bottom, s.top,
                                                          i_height, 1, 10))
            self.spinLDown.set_adjustment(gtk.Adjustment(s.leftdown, 0,
                                                         s.rightup, 1, 10))
        elif dir == DIR_BOTTOM:
            s.bottom = value
            s.leftdown = s.leftdown + prevValue - value
            self.spinLDown.set_value(s.leftdown)
            self.spinTop.set_adjustment(gtk.Adjustment(s.top, 0,
                                                       s.bottom, 1, 10))
            self.spinRUp.set_adjustment(gtk.Adjustment(s.rightup, s.leftdown,
                                                       i_height, 1, 10))
        elif dir == DIR_RUP:
            s.rightup = value
            s.top = s.top + prevValue - value
            self.spinTop.set_value(s.top)
            self.spinBottom.set_adjustment(gtk.Adjustment(s.bottom, s.top,
                                                          i_height, 1, 10))
            self.spinLDown.set_adjustment(gtk.Adjustment(s.leftdown, 0,
                                                         s.rightup, 1, 10))
        elif dir == DIR_LDOWN:
            s.leftdown = value
            s.bottom = s.bottom + prevValue - value
            self.spinBottom.set_value(s.bottom)
            self.spinTop.set_adjustment(gtk.Adjustment(s.top, 0,
                                                       s.bottom, 1, 10))
            self.spinRUp.set_adjustment(gtk.Adjustment(s.rightup, s.leftdown,
                                                       i_height, 1, 10))
        # endif
        self.invalidateImage()

    # enddef


    def populateTextVBox(self):
        ''' Creates text entries from the boxes'''

        # first we need to remove old symbols
        # in case this is not first open file
        self.textVBox.foreach(lambda widget: \
                              self.textVBox.remove(widget))

        row = 0
        for line in self.boxes:
            col = 0
            hbox = gtk.HBox()
            self.textVBox.pack_start(hbox)
            hbox.show()
            for s in line:
                if s.spaceBefore:
                    label = gtk.Label('   ')
                    hbox.pack_start(label, False, False, 0)
                    label.show()

                # endif

                self.makeGtkEntry(s, row, col)
                hbox.pack_start(s.entry, expand=False, fill=False, padding=0)
                # following entry properties must be used after hbox.pack_start
                # otherwise RTL chars will receives offset
                # print 'scroll-offset:', s.entry.get_property('scroll-offset')
                s.entry.set_text(s.text)
                s.entry.set_width_chars(len(unicode(s.text)))
                s.setEntryFont()
                s.entry.show()
                col += 1

            # endfor

            row += 1

        # endfor
    # enddef

    #
    def redrawArea(self, drawingArea, event):
        '''redraw area of selected symbol + add rectangle'''
        if self.selectedRow != None:
            gc = drawingArea.get_style().fg_gc[gtk.STATE_NORMAL]
            color = gtk.gdk.color_parse('red')
            drawingArea.modify_fg(gtk.STATE_NORMAL, color)  # color of rectangle
            if self.pixbuf:
                drawingArea.window.draw_pixbuf(gc, self.pixbuf, 0, 0, 0, 0)

            # endif

            s = self.boxes[self.selectedRow][self.selectedColumn]
            width = s.right - s.left
            height = s.bottom - s.top
            drawingArea.window.draw_rectangle(gc,
                False, s.left, s.top, width, height)

        # endif
    # enddef


    def filecheck(self, imageName):
        '''
        Make sure that the image, box files exists
        find box file format
        '''
        try:
            fc = open(imageName, 'r')
            fc.close()
        except IOError:
            self.errorDialog('Cannot find the %s file' % imageName,
                             self.window)
            return False

        boxname = imageName.rsplit('.', 1)[0] + '.box'
        try:
            fb = open(boxname, 'r')
            fb.close()
        except IOError:
            self.errorDialog('Cannot find the %s file' % boxname,
                             self.window)
            return False
        return True


    def loadImageAndBoxes(self, imageName, fileChooser):
        (name, extension) = imageName.rsplit('.', 1)
        boxname = name + '.box'

        file_ok = self.filecheck(imageName)
        if file_ok == False:
            return False

        self.pixbuf = gtk.gdk.pixbuf_new_from_file(imageName)
        height = self.pixbuf.get_height()
        self.boxes = loadBoxData(boxname, height)
        if self.boxes == -1:  # wrong format of box file
            self.pixbuf = ""  # clear area
            self.selectedRow = None
            self.textVBox.foreach(lambda widget: \
                              self.textVBox.remove(widget))
            return False
        self.loadedBoxFile = boxname
        self.window.set_title('pyTesseractTrainer - %s: %s' % \
                (VERSION, boxname))

        if VERBOSE > 0:
            print datetime.now(), 'File %s is opened.' % imageName

        if VERBOSE > 0:
            print datetime.now(), 'Displaying image...'
        self.drawingArea.set_size_request(self.pixbuf.get_width(),
                height)
        if VERBOSE > 0:
            print datetime.now(), 'Displaying symbols...'
        self.populateTextVBox()

        self.setImageControlSensitivity(True)
        self.selectedRow = 0
        self.selectedColumn = 0
        self.boxes[0][0].entry.grab_focus()
        if VERBOSE > 0:
            print datetime.now(), \
                'Function loadImageAndBoxes is finished.'
        return True

    # enddef


    def mergeTextFile(self, fileName, fileChooser):
        row = 0
        col = 0
        try:
            ft = open(fileName, 'r')
            for line in ft:
                line = unicode(line)
                for char in line:
                    if not char.isspace():
                        if row < len(self.boxes):
                            self.boxes[row][col].text = char
                            self.boxes[row][col].setEntryFont()
                            col += 1
                            if col == len(self.boxes[row]):
                                col = 0
                                row += 1

                            # endif
                        # endif
                    # endif
                # endfor
            # endfor

            ft.close()
        except IOError:
            self.errorDialog('File ' + fileName + ' does not exist',
                             fileChooser)

        # endtry
    # enddef


    def doFileOpen(self, action):
        chooser = gtk.FileChooserDialog('Open Image', self.window,
                gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL,
                gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        filter = gtk.FileFilter()
        filter.set_name('TIFF files')
        filter.add_pattern('*.tif')
        filter.add_pattern('*.tiff')
        chooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name('Image files')
        filter.add_pattern('*.jpg')
        filter.add_pattern('*.jpeg')
        filter.add_pattern('*.png')
        filter.add_pattern('*.bmp')
        filter.add_pattern('*.tif')
        filter.add_pattern('*.tiff')
        chooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name('All files')
        filter.add_pattern('*')
        chooser.add_filter(filter)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            fileName = chooser.get_filename()
            self.loadImageAndBoxes(fileName, chooser)

        # endif

        chooser.destroy()

    # enddef


    def doFileMergeText(self, action):
        chooser = gtk.FileChooserDialog('Merge Text File', self.window,
                gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL,
                gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        filter = gtk.FileFilter()
        filter.set_name('All files')
        filter.add_pattern('*')
        chooser.add_filter(filter)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            fileName = chooser.get_filename()
            self.mergeTextFile(fileName, chooser)

        # endif

        chooser.destroy()

    # enddef


    def doFileSave(self, action):
        if self.boxes == None:
            self.errorDialog('Nothing to save', self.window)
            return

        # endif

        height = self.pixbuf.get_height()

        path = self.loadedBoxFile
        bak_path = safe_backup(path)
        if VERBOSE > 0:
            if bak_path:
                print '%s safely backed up as %s' % (path, bak_path)
            else:
                print '%s does not exist, nothing to backup' % path

        save_f = open(self.loadedBoxFile, 'w')
        for row in self.boxes:
            for s in row:
                text = s.text
                if s.underline:
                    text = "'" + text

                # endif

                if s.italic:
                    text = '$' + text

                # endif

                if s.bold:
                    text = '@' + text

                # endif

                if  SAVE_FORMAT == 2:
                    save_f.write('%s %d %d %d %d\n' % (text, s.left, height
                            - s.bottom, s.right, height - s.top))
                else:
                    save_f.write('%s %d %d %d %d %d\n' % (text, s.left, height
                            - s.bottom, s.right, height - s.top, s.page))

            # endfor
        # endfor

        save_f.close()
    # enddef


    def doHelpAbout(self, action):
        dialog = gtk.Dialog('About pyTesseractTrainer', self.window,
                            gtk.DIALOG_NO_SEPARATOR | gtk.DIALOG_MODAL,
                            (gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_size_request(450, 250)
        label = gtk.Label(
            'pyTesseractTrainer version %s\n'
            'website: pytesseracttrainer.googlecode.com\n'
            '\n'
            'Copyright 2010 Zdenko Podobný <zdenop at gmail.com>\n'
            'Copyright 2008 Mihail Radu Solcan (djvused and image maps)\n'
            'Copyright 2007 Cătălin Frâncu <cata at francu.com>\n'
            '\n'
            'This program is free software: you can redistribute it and/or '
            'modify it under the terms of the GNU General Public License v3'
            % (VERSION))
        label.set_line_wrap(True)
        dialog.vbox.pack_start(label, True, True, 0)
        label.show()
        dialog.run()
        dialog.destroy()

    # enddef

    def doHelpAboutMerge(self, action):
        dialog = gtk.Dialog('About Merge Text...', self.window,
                            gtk.DIALOG_NO_SEPARATOR | gtk.DIALOG_MODAL,
                            (gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_size_request(450, 250)

        font = pango.FontDescription('Arial Bold 12')
        label = gtk.Label('Function: Merge Text\n')
        label.modify_font(font)
        label.show()
        dialog.vbox.pack_start(label, False, False)

        label = gtk.Label(
        'This function takes text form external file and put it to '
        'currrent boxes. Number of boxes should fit tu number of '
        'symbols in file. If they did not match, you should '
        'split/join/delete symbols&boxs before running "Merge Text...".\n'
        '\n'
        'This is usefull if you have correct text from training image '
        'in external file.')
        label.set_line_wrap(True)
        label.show()
        dialog.vbox.pack_end(label, False, False)
        dialog.run()
        dialog.destroy()

    # enddef


    def doHelpShortcuts(self, action):
        dialog = gtk.Dialog('Keyboard shortcuts', self.window,
                            gtk.DIALOG_NO_SEPARATOR | gtk.DIALOG_MODAL,
                            (gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_size_request(450, 250)
        label = gtk.Label(
            'Keyboard shortcuts\n'
            '\n'
            'Ctrl-B: mark entire word as bold\n'
            'Ctrl-I: mark entire word as italic\n'
            'Ctrl-U: mark current symbol as underline\n'
            'Ctrl-arrow: grow box up, down, left or right\n'
            'Ctrl-Shift-arrow: shrink box up, down, left or right\n'
            'Ctrl-1: merge current symbol&box with next symbol\n'
            'Ctrl-2: split current symbol&box vertically\n'
            'Ctrl-C: copy coordinates (djvu txt style)\n'
            'Ctrl-A: copy coordinates (djvu ant style)\n'
            'Ctrl-M: copy coordinates (html image map style)\n'
            'Ctrl-D: delete current symbol&box\n')
        label.set_line_wrap(True)
        dialog.vbox.pack_start(label, True, True, 0)
        label.show()
        dialog.run()
        dialog.destroy()

    # enddef


    def doEditCopy(self, action):
        this = self.boxes[self.selectedRow][self.selectedColumn]
        coords = '%s %s %s %s' % (this.left, this.leftdown, this.right, \
                                  this.rightup)
        clipboard = gtk.clipboard_get("CLIPBOARD")
        clipboard.set_text(coords, len=-1)
    #enddef


    def doEditdjvMap(self, action):
        this = self.boxes[self.selectedRow][self.selectedColumn]
        area_width = this.right - this.left
        area_height = this.rightup - this.leftdown
        coords = '%s %s %s %s' % \
                (this.left, this.leftdown, area_width, area_height)
        clipboard = gtk.clipboard_get("CLIPBOARD")
        clipboard.set_text(coords, len=-1)
    #enddef


    def doEdithtmMap(self, action):
        this = self.boxes[self.selectedRow][self.selectedColumn]
        coords = '%s,%s,%s,%s' % (this.left, this.top, this.right, this.bottom)
        clipboard = gtk.clipboard_get("CLIPBOARD")
        clipboard.set_text(coords, len=-1)
    #enddef


    def findSplitPoint(self, symbol):
        '''Looks 5 pixels to the left and right of the median divider'''

        subpixbuf = self.pixbuf.subpixbuf(symbol.left, symbol.top,
                symbol.right - symbol.left, symbol.bottom - symbol.top)

        # get_pixels_array work only with PyGTK with support of Numeric

        try:
            pixels = subpixbuf.get_pixels_array()

            height = len(pixels)
            width = len(pixels[0])
            bestX = -1
            bestNumPixels = 1000000

            for x in range(width // 2 - 5, width // 2 + 6):
                numPixels = countBlackPixels(pixels, x)

                # print x, numPixels

                if numPixels < bestNumPixels:
                    bestX = x
                    bestNumPixels = numPixels
        except:

                # endif
            # endfor
                 # workaround for missing support in PyGTK

            error = 'It looks like your PyGTK has no support for ' \
                + "Numeric!\nCommand 'split' will not work best way."

            # self.errorDialog(error, self.window)

            if VERBOSE > 0:
                print error
            bestX = subpixbuf.get_width() / 2

        return bestX + symbol.left

    # enddef


    def doEditSplit(self, action):
        '''Split box/symbol'''
        if self.selectedRow == None:
            self.errorDialog('Click into a cell first.', self.window)
            return

        # endif

        row = self.boxes[self.selectedRow]
        this = row[self.selectedColumn]
        clone = this.clone()
        this.right = self.findSplitPoint(this)
        clone.left = this.right
        clone.spaceBefore = False
        clone.text = '*'
        self.makeGtkEntry(clone, self.selectedRow, self.selectedColumn
                          + 1)
        clone.setEntryFont()
        hbox = this.entry.get_parent()
        hbox.pack_start(clone.entry, False, False, 0)

        # To reorder the child, use col + 1 and add all the word breaks
        pos = self.selectedColumn + 1
        for s in row[0:self.selectedColumn + 1]:
            if s.spaceBefore:
                pos += 1

            # endif
        # endfor

        hbox.reorder_child(clone.entry, pos)
        clone.entry.show()
        row.insert(self.selectedColumn + 1, clone)
        self.reconnectEntries(self.selectedRow)

        self.invalidateImage()
        self.buttonUpdateInProgress = True
        self.spinLeft.set_value(this.left)
        self.spinRight.set_value(this.right)
        self.spinTop.set_value(this.top)
        self.spinRUp.set_value(this.rightup)
        self.spinBottom.set_value(this.bottom)
        self.spinLDown.set_value(this.leftdown)
        self.buttonUpdateInProgress = None

    # enddef


    def doEditJoin(self, action):
        '''Join box/symbol with next box/symbol'''
        if self.selectedRow == None:
            self.errorDialog('Click into a cell first.', self.window)
            return

        # endif

        if self.selectedColumn + 1 == len(self.boxes[self.selectedRow]):
            self.errorDialog('There is no next symbol on this line!',
                             self.window)
            return

        # endif

        this = self.boxes[self.selectedRow][self.selectedColumn]
        next = self.boxes[self.selectedRow][self.selectedColumn + 1]
        this.text += next.text
        this.left = min(this.left, next.left)
        this.right = max(this.right, next.right)
        this.top = min(this.top, next.top)
        this.bottom = max(this.bottom, next.bottom)
        this.setEntryFont()
        next.entry.destroy()
        del self.boxes[self.selectedRow][self.selectedColumn + 1]
        self.reconnectEntries(self.selectedRow)
        self.invalidateImage()

        self.buttonUpdateInProgress = True
        self.spinLeft.set_value(this.left)
        self.spinRight.set_value(this.right)
        self.spinTop.set_value(this.top)
        self.spinRUp.set_value(this.rightup)
        self.spinBottom.set_value(this.bottom)
        self.spinLDown.set_value(this.leftdown)
        self.buttonUpdateInProgress = None

    # enddef


    def doEditDelete(self, action):
        '''Delete box/symbol'''
        if self.selectedRow == None:
            self.errorDialog('Click into a cell first.', self.window)
            return

        # endif

        row = self.boxes[self.selectedRow]
        this = row[self.selectedColumn]
        if self.selectedColumn + 1 < len(row):
            next = row[self.selectedColumn + 1]
        else:
            next = None

        # endif

        if this.spaceBefore:
            if next != None and not next.spaceBefore:
                next.spaceBefore = True
            else:

                # delete the label before this symbol

                this.deleteLabelBefore()

            # endif
        # endif

        this.entry.destroy()
        del row[self.selectedColumn]
        self.reconnectEntries(self.selectedRow)

        # Find the next cell to focus

        if self.selectedColumn >= len(row):
            self.selectedRow += 1
            self.selectedColumn = 0

        # endif

        if self.selectedRow >= len(self.boxes):
            self.selectedRow = len(self.boxes) - 1
            self.selectedColumn = len(self.boxes[self.selectedRow]) - 1

        # endif

        self.boxes[self.selectedRow][self.selectedColumn].entry.grab_focus()

    # enddef


    def setImageControlSensitivity(self, bool):
        '''If image is not open menu actions will be blocked'''
        self.actionGroup.get_action('MergeText').set_sensitive(bool)
        self.actionGroup.get_action('Save').set_sensitive(bool)

    # enddef


    def setSymbolControlSensitivity(self, bool):
        '''If symbols are not loaded actions will be blocked'''
        self.buttonBox.set_sensitive(bool)
        self.actionGroup.get_action('Edit').set_sensitive(bool)

    # enddef


    def makeMenu(self):
        uiManager = gtk.UIManager()
        self.accelGroup = uiManager.get_accel_group()
        self.window.add_accel_group(self.accelGroup)
        self.actionGroup = gtk.ActionGroup('UIManagerExample')
        self.actionGroup.add_actions(
            [('Open', gtk.STOCK_OPEN, '_Open Image...', None, None,
              self.doFileOpen),
             ('MergeText', None, '_Merge Text...', '<Control>3', None,
              self.doFileMergeText),
             ('Save', gtk.STOCK_SAVE, '_Save Box Info', None, None,
              self.doFileSave),
             ('Quit', gtk.STOCK_QUIT, None, None, None,
              lambda w: gtk.main_quit()),
             ('File', None, '_File'),
             ('Edit', None, '_Edit'),
             ('Copy', None, 'Copy _tesseract coords', '<Control>T', None,
              self.doEditCopy),
             ('djvMap', None, 'Copy _djvMap coords', '<Control>A', None,
              self.doEditdjvMap),
             ('htmMap', None, 'Copy _htmMap coords', '<Control>M', None,
              self.doEdithtmMap),
             ('Split', None, '_Split Symbol&Box', '<Control>2', None,
              self.doEditSplit),
             ('JoinWithNext', None, '_Join with Next Symbol&Box',
              '<Control>1', None, self.doEditJoin),
             ('Delete', None, '_Delete Symbol&Box', '<Control>D',
              None, self.doEditDelete),
             ('Help', None, '_Help'),
             ('About', None, '_About', None, None, self.doHelpAbout),
             ('AboutMergeText', None, 'About Merge Text', None, None,
                self.doHelpAboutMerge),
             ('Shortcuts', None, '_Keyboard shotcuts', None, None,
              self.doHelpShortcuts),
             ])
        uiManager.insert_action_group(self.actionGroup, 0)
        uiManager.add_ui_from_string(MENU)
        return uiManager.get_widget('/MenuBar')
    #enddef

    # enddef


    def __init__(self):
        if VERBOSE > 0:
            print 'Platform:', sys.platform

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.set_title('pyTesseractTrainer - Tesseract Box '
                              + 'Editor version %s'
                              % (VERSION))        
        self.window.set_size_request(900, 600)

        vbox = gtk.VBox(False, 2)
        self.window.add(vbox)
        vbox.show()

        menuBar = self.makeMenu()
        vbox.pack_start(menuBar, False)

        self.scrolledWindow = gtk.ScrolledWindow()
        self.scrolledWindow.set_policy(gtk.POLICY_AUTOMATIC,
                gtk.POLICY_AUTOMATIC)
        vbox.pack_start(self.scrolledWindow, True, True, 2)
        self.scrolledWindow.show()

        self.drawingArea = gtk.DrawingArea()
        self.drawingArea.connect('expose-event', self.redrawArea)
        self.scrolledWindow.add_with_viewport(self.drawingArea)
        self.drawingArea.show()

        self.textScroll = gtk.ScrolledWindow()
        self.textScroll.set_policy(gtk.POLICY_AUTOMATIC,
                                   gtk.POLICY_AUTOMATIC)
        vbox.pack_start(self.textScroll, True, True, 2)
        self.textScroll.show()

        self.textVBox = gtk.VBox()
        self.textScroll.add_with_viewport(self.textVBox)
        self.textVBox.show()

        self.buttonBox = gtk.HBox(False, 0)
        vbox.pack_start(self.buttonBox, False, False, 2)
        self.buttonBox.show()

        b = gtk.CheckButton('_Bold', True)
        self.buttonBox.pack_start(b, False, False, 10)
        b.connect('toggled', self.onCheckButtonToggled, ATTR_BOLD)
        b.add_accelerator('activate', self.accelGroup, ord('B'),
                          gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        b.show()
        self.boldButton = b

        b = gtk.CheckButton('_Italic', True)
        self.buttonBox.pack_start(b, False, False, 10)
        b.connect('toggled', self.onCheckButtonToggled, ATTR_ITALIC)
        b.add_accelerator('activate', self.accelGroup, ord('I'),
                          gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        b.show()
        self.italicButton = b

        b = gtk.CheckButton('_Underline', True)
        self.buttonBox.pack_start(b, False, False, 10)
        b.connect('toggled', self.onCheckButtonToggled, ATTR_UNDERLINE)
        b.add_accelerator('activate', self.accelGroup, ord('U'),
                          gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        b.show()
        self.underlineButton = b

        self.spinBottom = gtk.SpinButton()
        self.spinBottom.set_wrap(True)
        self.spinBottom.connect("value_changed", self.onSpinButtonChanged,
                                DIR_BOTTOM)
        self.buttonBox.pack_end(self.spinBottom, False, False, 0)
        self.spinBottom.show()
        l = gtk.Label(' Bottom:')
        self.buttonBox.pack_end(l, False, False, 0)
        l.show()

        self.spinTop = gtk.SpinButton()
        self.spinTop.connect('value_changed', self.onSpinButtonChanged,
                             DIR_TOP)
        self.buttonBox.pack_end(self.spinTop, False, False, 0)
        self.spinTop.show()
        l = gtk.Label(' Top:')
        self.buttonBox.pack_end(l, False, False, 0)
        l.show()

        self.spinRUp = gtk.SpinButton()
        self.spinRUp.connect("value_changed", self.onSpinButtonChanged,
                             DIR_RUP)
        self.buttonBox.pack_end(self.spinRUp, False, False, 0)
        self.spinRUp.show()
        lru = gtk.Label(' r-up:')
        self.buttonBox.pack_end(lru, False, False, 0)
        lru.show()

        self.spinRight = gtk.SpinButton()
        self.spinRight.connect('value_changed', self.onSpinButtonChanged,
                               DIR_RIGHT)
        self.buttonBox.pack_end(self.spinRight, False, False, 0)
        self.spinRight.show()
        l = gtk.Label(' Right:')
        self.buttonBox.pack_end(l, False, False, 0)
        l.show()

        self.spinLDown = gtk.SpinButton()
        self.spinLDown.connect('value_changed', self.onSpinButtonChanged,
                               DIR_LDOWN)
        self.buttonBox.pack_end(self.spinLDown, False, False, 0)
        self.spinLDown.show()
        lld = gtk.Label(' l-down:')
        self.buttonBox.pack_end(lld, False, False, 0)
        lld.show()

        self.spinLeft = gtk.SpinButton()
        self.spinLeft.connect('value_changed', self.onSpinButtonChanged,
                              DIR_LEFT)
        self.buttonBox.pack_end(self.spinLeft, False, False, 0)
        self.spinLeft.show()
        l = gtk.Label('Left:')
        self.buttonBox.pack_end(l, False, False, 0)
        l.show()

        self.setImageControlSensitivity(False)
        self.setSymbolControlSensitivity(False)
        self.window.show_all() #.show()

        if len(sys.argv) >= 2 and sys.argv[1] != "":
            argfilename = sys.argv[1]
            self.loadImageAndBoxes(argfilename, self.window)
        else:
            argfilename = None
        self.isPaused = False

    # enddef
# endClass



def main():
    '''main'''
    gtk.main()
    return 0

# enddef

if __name__ == '__main__':
    MainWindow()
    main()
