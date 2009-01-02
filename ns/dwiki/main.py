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
        gladefile = ns.dwiki.__file__[:-12] + os.sep + 'dwiki.glade'
        self.wTree = gtk.glade.XML(gladefile)
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('MainWindow')
        self.pagesTree = self.wTree.get_widget('pagesTree')
        self.booksTree = self.wTree.get_widget('booksTree')
        self.setup_store()

        self.renderArea = self.wTree.get_widget('renderArea')
        self.doc = gtkhtml2.Document()
        self.doc.connect('link_clicked', self.link_clicked)
        self.html = gtkhtml2.View()
        self.html.set_document(self.doc)
        self.renderArea.add(self.html)

        self.setup_books()
        self.setup_pages()
        self.window.connect("destroy", gtk.main_quit)
        self.visible = True
        self.window.show_all()

        self.icon = gtk.StatusIcon()
        self.icon.set_from_stock('gtk-spell-check')
        self.icon.set_visible(True)
        self.icon.connect('activate', self.on_status_icon)

        self.refresh_books()
        self.refresh_pages()

    def setup_store(self):
        path = os.getenv('HOME') + os.sep + '.dwiki'
        self.library = models.WikiLibrary(path)
        self.library.set_on_change(self.on_change)
        if len(self.library.get_shelves()) == 0:
            self.shelf = models.WikiShelf(self.library, 'Default')
            self.book = models.WikiBook(self.shelf, 'Default')
        else:
            self.shelf = self.library.get_shelf(self.library.get_shelves()[0])
            self.book = self.shelf.get_book(self.shelf.get_books()[0])

    def on_change(self):
        self.refresh_books()
        self.refresh_pages()

    def refresh_books(self):
        self.booksStore.clear()
        path = None
        for shelf in self.library.get_shelves():
            shelf_iter = self.booksStore.append(None, [shelf])
            shelf = self.library.get_shelf(shelf)
            for book in shelf.get_books():
                book_iter = self.booksStore.append(shelf_iter, [book])
                if book == self.book.name and shelf.name == self.shelf.name:
                    path = self.booksStore.get_path(book_iter)

        if path != None:
            self.booksTree.expand_to_path(path)#(self.shelf.name, self.book.name))
            self.booksTree.get_selection().select_path(path)


    def refresh_pages(self):
        path = None
        self.pagesStore.clear()
        for page in self.book.get_pages():
            page_iter = self.pagesStore.append([page])
            if self.page != None and page == self.page.title:
                path = self.pagesStore.get_path(page_iter)

        if path != None:
            self.pagesTree.expand_to_path(path)#(self.shelf.name, self.book.name))
            self.pagesTree.get_selection().select_path(path)

    def setup_books(self):
        self.booksStore = gtk.TreeStore(str)
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
        self.page = None

    def on_newpage_clicked(self, widget):
        if self.book != None:
            editor.Editor(models.WikiPage(self.book))

    def on_push_clicked(self, widget):
        if self.book != None:
            self.book.push()

    def on_pull_clicked(self, widget):
        if self.book != None:
            self.book.pull()

    def on_preferences_clicked(self, widget):
        if self.book != None:
            self.book.config()

    def on_booksTree_cursor_changed(self, widget):
        model, sel = self.booksTree.get_selection().get_selected()
        if sel != None:
            parent_iter = self.booksStore.iter_parent(sel)
            if parent_iter != None:
                shelf_name = model.get_value(parent_iter, 0)
                book_name = model.get_value(sel, 0)
                self.shelf = self.library.get_shelf(shelf_name)
                self.book = self.shelf.get_book(book_name)
                self.refresh_pages()


    def on_pagesTree_cursor_changed(self, widget):
        model, sel = self.pagesTree.get_selection().get_selected()
        if sel != None:
            page_name = model.get_value(sel, 0)
            self.page = self.book.get_page(page_name)
            self.render_page(self.page)

    def link_clicked(self, document, link):
        link.strip()
        if link.find('/') > 0:
            book = link[0:link.find('/')]
            if self.shelf.has_book(book):
                book = self.shelf.get_book(book)
            else:
                book = models.WikiBook(self.shelf, book)
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

    def on_MainWindow_key_press_event(self, widget, event):
        if 'GDK_CONTROL_MASK' in event.state.value_names and event.keyval == 99:
            selection = gtkhtml2.html_selection_get_text(self.html)
            if selection != None:
                cb = self.html.get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)
                cb.set_text(selection)

    def on_search_clicked(self, widget):
        pass

    def main(self):
        gtk.main()
