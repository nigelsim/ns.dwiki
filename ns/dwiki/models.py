import sys, os

# Library
#  |- Shelf
#      |- Book
#          |- Page

class WikiLibrary:
    def __init__(self, path):
        self.path = path
        self._on_change = None
        if not os.path.exists(self.path):
             os.mkdir(self.path)
    def on_change(self):
        if self._on_change:
            self._on_change()

    def set_on_change(self, func):
        self._on_change = func

    def get_shelves(self):
        return os.listdir(self.path)

    def get_shelf(self, name):
        shelf_dir = self.path + os.sep + name
        if not os.path.exists(shelf_dir):
            raise Exception('The shelf %s does not exist'%name)
        if os.path.exists('%s/.git'%shelf_dir):
            shelf = GitWikiShelf(self, name)
        else:
            shelf = WikiShelf(self, name)
        return shelf

    def delete_shelf(self, name):
        page_file = self.path + os.sep + name
        os.rmdir(page_file)
        self.on_change()

class WikiPage:
    def __init__(self, book, original_title=None):
        self._book = book
        self._original_title = original_title
        self._title = original_title
        self._body = None

    def save(self):
        f = open(self.path, 'w')
        f.write(self.body)
        f.close()

        if self.original_title != None and self.original_title != self.title:
            page_file = self._book.path + os.sep + self.original_title
            os.remove(page_file)
        self._original_title = self.title

        self._book.on_change()
        return

    @apply
    def path():
        def get(self):
            return self._book.path + os.sep + self.title
        return property(get)

    @apply
    def title():
        def get(self):
            return self._title
        def set(self,value):
            self._title = value
        return property(get, set)

    @apply
    def body():
        def get(self):
            return self._body
        def set(self,value):
            self._body = value
        return property(get, set)

    @apply
    def original_title():
        def get(self):
            return self._original_title
        return property(get)

class WikiBook:
    page_factory = WikiPage
    def __init__(self, shelf, name):
        self._shelf = shelf
        self._name = name
        if not os.path.exists(self.path):
             os.mkdir(self.path)

    @apply
    def path():
        def get(self):
            return self._shelf.path + os.sep + self._name
        return property(get)

    @apply
    def name():
        def get(self):
            return self._name
        def set(self,value):
            # TODO rename dir
            self._name = value
        return property(get, set)


    def get_pages(self):
        return os.listdir(self.path)

    def get_page(self, name):
        page_file = self.path + os.sep + name
        if not os.path.exists(page_file):
            raise Exception('The page %s does not exist'%name)
        page = self.page_factory(self, name)
        f = open(page_file, 'r')
        page.body = f.read()
        f.close()
        return page

    def has_page(self, name):
        return name in self.get_pages()

    def delete_page(self, name):
        page_file = self.path + os.sep + name
        os.remove(page_file)
        self.on_change()

    def on_change(self):
        self._shelf.on_change()

    def new_page(self):
        return WikiPage(self)

    def push(self):
        pass

    def pull(self):
        pass

    def config(self):
        pass


class WikiShelf:
    book_factory = WikiBook
    def __init__(self, library, name):
        self._library = library
        self._name = name

        if not os.path.exists(self.path):
             os.mkdir(self.path)

    @apply
    def path():
        def get(self):
            return self._library.path + os.sep + self._name
        return property(get)

    @apply
    def name():
        def get(self):
            return self._name
        def set(self,value):
            # TODO rename dir
            self._name = value
        return property(get, set)

    def get_books(self):
        return os.listdir(self.path)

    def get_book(self, name):
        book_dir = self.path + os.sep + name
        if not os.path.exists(book_dir):
            raise Exception('The book %s does not exist'%name)
        book = self.book_factory(self, name)
        return book

    def has_book(self, name):
        return name in self.get_books()

    def delete_book(self, name):
        page_file = self.path + os.sep + name
        os.rmdir(page_file)
        self.on_change()

    def on_change(self):
        self._library.on_change()

from subprocess import Popen

def run(command, path):
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    if not os.path.isdir(path):
        raise Exception('This is not a path: %s'%path)

    Popen(command, shell=True, cwd=path)


class GitWikiPage(WikiPage):
    def save(self):
        has_moved = self.original_title != None and self.original_title != self.title
        if has_moved:
            f = open(self.original_title, 'w')
        else:
            f = open(self.path, 'w')

        f.write(self.body)
        f.close()

        if has_moved:
            run('git mv "%s" "%s" ; git commit -m "Changing"'%(self.original_title, self.path), self.path)
        else:
            run('git add "%s" ; git commit -m "Changing"'%(self.path), self.path)


        self._original_title = self.title

class GitWikiBook(WikiBook):
    page_factory = GitWikiPage
    def __init__(self, shelf, name):
        self._shelf = shelf
        self._name = name
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            run('git add "%s" ; git commit -m "Creating new book"'%self.path, self.path)

    def new_page(self):
        return GitWikiPage(self)

    def push(self):
        run('git push', self.path)

    def pull(self):
        run('git pull', self.path)

    def config(self):
        run('git-gui', self.path)


class GitWikiShelf(WikiShelf):
    book_factory = GitWikiBook

    def get_books(self):
        return [book for book in os.listdir(self.path) if book != '.git']


