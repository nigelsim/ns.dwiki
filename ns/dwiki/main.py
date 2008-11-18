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
import gtkhtml2

import os

import ns.dwiki
from ns.dwiki import models, editor
from ns.dwiki.wiki import wiki

class Main:
    def __init__(self):
        gladefile = ns.dwiki.__file__[:-12] + 'dwiki.glade'
        self.wTree = gtk.glade.XML(gladefile)
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('MainWindow')
        self.pagesTree = self.wTree.get_widget('pagesTree')
        self.booksTree = self.wTree.get_widget('booksTree')
        self.setup_store()
        
        self.renderArea = self.wTree.get_widget('renderArea')
        self.doc = gtkhtml2.Document()
        self.doc.connect('link_clicked', self.link_clicked)
        html = gtkhtml2.View()
        html.set_document(self.doc)
        self.renderArea.add(html)

        self.setup_books()
        self.setup_pages()
        self.window.connect("destroy", gtk.main_quit)
        self.visible = True
        self.window.show_all()
        
        self.icon = gtk.StatusIcon()
        self.icon.set_from_stock('gtk-spell-check')
        self.icon.set_visible(True)
        self.icon.connect('activate', self.on_status_icon)
        
        self.refresh_pages()

    def setup_store(self):
        path = os.getenv('HOME') + os.sep + '.dwiki'
        self.library = models.WikiLibrary(path)
        self.library.set_on_change(self.on_change)
        
        self.shelf = models.WikiShelf(self.library, 'Default')
        self.book = models.WikiBook(self.shelf, 'Default')

    def on_change(self):
        self.refresh_pages()
        
    def refresh_pages(self):
        self.pagesStore.clear()
        for page in self.book.get_pages():
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

    def on_newpage_clicked(self, widget):
        editor.Editor(models.WikiPage(self.book))

    def on_pagesTree_cursor_changed(self, widget):
        model, sel = self.pagesTree.get_selection().get_selected()
        if sel != None:
            page_name = model.get_value(sel, 0)
            page = self.book.get_page(page_name)
            self.render_page(page)
            
    def link_clicked(self, document, link):
        link.strip()
        if link.find('/') > 0:
            book = link[0:link.find('/')]
            if self.shelf.has_book(book):
                book = self.shelf.get_book(book)
            else:
                book = WikiBook(self.shelf, book)
            page = link[link.find('/')+1:]
        else:
            book = self.book
            page = link
            
        if book.has_page(page):
            actual_page = book.get_page(page)
            self.render_page(actual_page)
        else:
            actual_page = models.WikiPage(book)
            actual_page.title = page
            editor.Editor(actual_page)
            
            
    def render_page(self, page):
        self.doc.clear()
        self.doc.open_stream('text/html')
        self.doc.write_stream('<html></head><body><h1>%s</h1><hr/>%s</body></html>'%(page.title, wiki.render(page.body)))
        self.doc.close_stream()

    def on_pagesTree_button_press_event(self, widget, event):
        model, sel = self.pagesTree.get_selection().get_selected()
        if sel != None:
            page_name = model.get_value(sel, 0)
            if event.type == gtk.gdk._2BUTTON_PRESS:
                editor.Editor(self.book.get_page(page_name))

    def on_status_icon(self, widget):
        self.visible = not self.visible
        if self.visible:
            self.window.show()
        else:
            self.window.hide()
            

    def on_search_clicked(self, widget):
        pass

    def main(self):
        gtk.main()
