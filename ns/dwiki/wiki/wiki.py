from ns.dwiki.wiki import creole, creole2html

def render(text):
    document = creole.Parser(unicode(text)).parse()
    print (creole2html.HtmlEmitter(document).emit().encode('utf-8', 'ignore'))
    