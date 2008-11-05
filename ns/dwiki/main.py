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

import os

import ns.dwiki
from ns.dwiki import models 

class Main:
    def __init__(self):
        gladefile = ns.dwiki.__file__[:-12] + 'dwiki.glade'
        self.wTree = gtk.glade.XML(gladefile)
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('MainWindow')
        self.pagesTree = self.wTree.get_widget('notesTree')
        self.booksTree = self.wTree.get_widget('booksTree')
        
        self.setup_store()

        self.setup_books()
        self.setup_pages()
        self.window.connect("destroy", gtk.main_quit)
        self.window.show()
        self.refresh_pages()

    def setup_store(self):
        path = os.getenv('HOME') + os.sep + '.dwiki'
        self.store = models.WikiStore(path)
        
    def refresh_pages(self):
        self.pagesStore.clear()
        for page in self.store.get_pages():
            self.pagesStore.append([page])

    def setup_books(self):
        self.booksStore = gtk.ListStore(str)
        self.booksTree.set_model(self.booksStore)
        col = gtk.TreeViewColumn('Books')
        col.pack_start(gtk.CellRendererText())
        self.booksTree.append_column(col)

        cell = gtk.CellRendererText()
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 0)

    def setup_pages(self):
        self.pagesStore = gtk.ListStore(str)
        self.pagesTree.set_model(self.pagesStore)
        col = gtk.TreeViewColumn('Pages')
        self.pagesTree.append_column(col)

        cell = gtk.CellRendererText()
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 0)

    def on_search_clicked(self, widget):
        self.notesStore.append(['t'])

    def main(self):
        gtk.main()
