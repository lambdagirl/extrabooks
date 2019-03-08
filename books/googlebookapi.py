import json
import requests

def get_book_by_isbn(isbn):
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+isbn)


    json_data = json.loads(response.text)
    book_info = json_data["items"][0]["volumeInfo"]

    title = book_info["title"]
    authors = book_info["authors"]
    published_date = book_info["publishedDate"]
    categories = book_info["categories"][0]
    if "description" in book_info:
        description = book_info["description"]
    else:
        description = json_data["items"][0]["searchInfo"]["textSnippet"]

    if "imageLinks" in book_info:
        thumbnail = book_info["imageLinks"]["thumbnail"]
        smallThumbnail = book_info["imageLinks"]["smallThumbnail"]
    else:
        thumbnail = "https://s.gr-assets.com/assets/nophoto/book/50x75-a91bf249278a81aabab721ef782c4a74.png"
        smallThumbnail = "https://s.gr-assets.com/assets/nophoto/book/50x75-a91bf249278a81aabab721ef782c4a74.png"

    book_object = {
                "title"           : title,
                "thumbnail"       : thumbnail,
                "smallThumbnail" : smallThumbnail,
                "description"     : description,
                "published_date": published_date,
                "authors"          : authors,
                "categories"        :categories,
                    }
    return book_object
