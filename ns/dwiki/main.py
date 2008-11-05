##############################################################################
#
# Copyright (c) 2008 Nigel Sim and Contributors.
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

import ns.dwiki

class Main:
    def __init__(self):
        gladefile = ns.dwiki.__file__[:-12] + 'dwiki.glade'
        self.wTree = gtk.glade.XML(gladefile)
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('MainWindow')
        self.notesTree = self.wTree.get_widget('notesTree')
        self.booksTree = self.wTree.get_widget('booksTree')

        self.setup_books()
        self.setup_notes()
        #self.inputFile = self.wTree.get_widget('inputFile')
        #self.outputFile = self.wTree.get_widget('outputFile')
        self.window.connect("destroy", gtk.main_quit)
        #self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()

    def setup_books(self):
        self.booksStore = gtk.ListStore(str)
        self.booksStore.append(['test1'])
        self.booksTree.set_model(self.booksStore)
        col = gtk.TreeViewColumn('Books')
        col.pack_start(gtk.CellRendererText())
        self.booksTree.append_column(col)

        cell = gtk.CellRendererText()
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 0)

    def setup_notes(self):
        self.notesStore = gtk.ListStore(str)
        self.notesStore.append(['test1'])
        self.notesStore.append(['test1'])
        self.notesTree.set_model(self.notesStore)
        col = gtk.TreeViewColumn('Notes')
        self.notesTree.append_column(col)

        cell = gtk.CellRendererText()
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 0)

    def on_search_clicked(self, widget):
        self.notesStore.append(['t'])

    def main(self):
        gtk.main()
