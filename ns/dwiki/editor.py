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

class Editor:
    def __init__(self, page):
        gladefile = ns.dwiki.__file__[:-12] + 'dwiki.glade'
        self.wTree = gtk.glade.XML(gladefile)
        self.wTree.signal_autoconnect(self)
        self.window = self.wTree.get_widget('EditorWindow')
        self.editor = self.wTree.get_widget('editor')
        self.title = self.wTree.get_widget('title')

        self.editor.get_buffer().set_text(page.body or '')
        self.title.set_text(page.title or 'Untitled')

        try:
            import gtkspell
            gtkspell.Spell(self.editor)
        except:
            pass

        self.page = page

        self.window.show()

    def on_save_clicked(self, widget):
        buf = self.editor.get_buffer()
        self.page.body = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
        self.page.title = self.title.get_text()
        self.page.save()

