import sys, os

class WikiStore:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
             os.mkdir(self.path)
        
    def get_pages(self):
        return os.listdir(self.path)
    
    def get_page(self, name):
        page_file = self.path + os.sep + name
        if not os.path.exists(page_file):
            raise Exception('The page %s does not exist'%name)
        page = WikiPage(name)
        f = open(page_file, 'r')
        page.body = f.read()
        f.close()        
        return page
    
    def save_page(self, page):
        page_file = self.path + os.sep + page.title
        f = open(page_file, 'w')
        f.write(page.body)
        f.close()
        
        if page.original_title != None and page.original_title != page.title:
            page_file = self.path + os.sep + page.original_title
            os.remove(page_file)
        return
    
    def delete_page(self, name):
        page_file = self.path + os.sep + name
        os.remove(page_file)
        
class WikiPage:
    def __init__(self, original_title=None):
        self._original_title = original_title
        self._title = original_title
        self._body = None
    
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