# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

from .model import Dentist
from mongoengine import connect
from flask_restful import reqparse

class DoctorsDoctorsname(Resource):
    connect(host='mongodb://admin:admin123@ds347665.mlab.com:47665/9322micro1')
    #Get dentist information
    def get(self, doctorsName):
        for t in Dentist.objects:
            content={}
            if t.name == doctorsName:
                content['id'] = t.did
                content['name'] = t.name
                content['location'] = t.location
                content['specialization'] = t.specialization
                content['availability'] = t.availability
                return content, 200, None
        return {"code": 404, "message": "Check name again"}, 404