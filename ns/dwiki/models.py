import sys, os

# Library
#  |- Shelf
#      |- Book
#          |- Page

class WikiLibrary:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
             os.mkdir(self.path)
        
    def get_shelves(self):
        return os.listdir(self.path)
    
    def get_shelf(self, name):
        page_file = self.path + os.sep + name
        if not os.path.exists(page_file):
            raise Exception('The shelf %s does not exist'%name)
        shelf = WikiShelf(self, name)
        return shelf
    
    def delete_shelf(self, name):
        page_file = self.path + os.sep + name
        os.rmdir(page_file)

class WikiShelf:
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
        book = WikiBook(self, name)
        return book
    
    def has_book(self, name):
        return name in self.get_books()
    
    def delete_book(self, name):
        page_file = self.path + os.sep + name
        os.rmdir(page_file)
        

class WikiBook:
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
        page = WikiPage(self, name)
        f = open(page_file, 'r')
        page.body = f.read()
        f.close()        
        return page
    
    def has_page(self, name):
        return name in self.get_pages()
    
    def delete_page(self, name):
        page_file = self.path + os.sep + name
        os.remove(page_file)
        
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
