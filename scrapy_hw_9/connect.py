import json

import certifi
from mongoengine import *

class Author(Document):
    fullname = StringField(required=True)
    date_born = StringField(required=True)
    born_location = StringField(required=True)
    bio = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

def connect_mongodb():
    uri = "mongodb+srv://osandreyman:1111@firstcluster.g6svumr.mongodb.net/hw_9_web?retryWrites=true&w=majority"

    connect('hw_9_web', host=uri, tlsCAFile=certifi.where(), ssl=True)

    with open('authors.json') as f:
        authors = json.load(f)

    with open('quotes.json') as f:
        quotes = json.load(f)

    for author in authors:
        Author(**author).save()

    for quote in quotes:
        author_fullname = quote['author']
        author = Author.objects(fullname=author_fullname).first()

        if author:
            quote['author'] = author
            Quote(**quote).save()
        else:
            print(f"Author '{author_fullname}' not found in the database. Quote not saved.")


if __name__ == '__main__':
    connect_mongodb()

