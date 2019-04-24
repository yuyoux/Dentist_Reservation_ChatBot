from mongoengine import IntField, Document, EmbeddedDocument,ListField, BooleanField,EmbeddedDocumentField, StringField


class Timeslot(EmbeddedDocument):
    time = StringField(required=True, max_length=500)
    status = StringField(required=True, max_length=500)

    def __init__(self, time, status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = time
        self.status = status


class Timeslots(Document):
    did = IntField(required=True)
    timeslist=ListField(EmbeddedDocumentField(Timeslot))

    def __init__(self, did, timeslist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.did = did
        self.timeslist = timeslist
