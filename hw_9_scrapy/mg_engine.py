import certifi
from mongoengine import *


uri = "mongodb+srv://osandreyman:1111@firstcluster.g6svumr.mongodb.net/hw_9_web?retryWrites=true&w=majority"
connection = connect(host=uri,  tlsCAFile=certifi.where(), ssl=True)



class Author(Document):

    fullname = StringField(max_length=100)
    born_date = StringField(max_length=100)
    # born_date = DateTimeField()
    born_location = StringField(max_length=1200)
    description = StringField()


class Quote(Document):

    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=100))
    quote = StringField(max_length=1200, required=True)

    meta = {'allow_inheritance': True}
