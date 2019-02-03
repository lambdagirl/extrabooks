from isbnlib import meta
from isbnlib.registry import bibformatters,PROVIDERS
from isbnlib._desc import goo_desc
from isbnlib._cover import cover
# now you can use the service
def get_isbn_data(isbn):
    bibtex = bibformatters['bibtex']
    print(bibtex(meta(isbn)))
    print(meta(isbn)['Title'])
    print(cover(isbn)['thumbnail'])
    print(goo_desc(isbn))
