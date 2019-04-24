from mongoengine import IntField, Document, EmbeddedDocument,ListField, BooleanField,EmbeddedDocumentField, StringField

class Dentist(Document):
    did = IntField(required=True)
    name = StringField(required=True)
    location = StringField(required=True)
    specialization = StringField(required=True)
    availability = BooleanField(required=True,default=True)

    def __init__(self, did, name,location, specialization, availability,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.did = did
        self.name = name
        self.location = location
        self.specialization = specialization
        self.availability = availability
