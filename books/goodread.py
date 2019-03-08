import xml.etree.ElementTree as ET
import requests
import re

def get_rating_by_isbn(isbn):
    key = "1emC5V4L1aQXNtWBo7SpKw"
    response = requests.get('https://www.goodreads.com/book/isbn/'+isbn+'?key='+key)

    root = ET.fromstring(response.content)

    for book in root.findall('book'):
        title            = book.find('title').text
        isbn             = book.find('isbn').text
        image_url        = book.find('image_url').text
        small_image_url  = book.find('small_image_url').text
        description      = book.find('description').text
        publication_year = book.find('publication_year').text
        publisher        = book.find('publisher').text
        average_rating   =book.find('average_rating').text
        ratings_count    = book.find('ratings_count').text
        author    = book.find('authors').find('author').find('name').text
    book_object = {
			"title"           : title,
			"isbn10"          : isbn,
			"image_url"       : image_url,
            "small_image_url" : small_image_url,
			"publisher"       : publisher,
			"description"     : description,
            "publication_year": publication_year,
            "average_rating"  : average_rating,
            "ratings_count"   : ratings_count,
			"author"          : author,
				}
    print(book_object)

    return(book_object)