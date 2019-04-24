# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

from .model import Dentist
from mongoengine import connect
from flask_restful import reqparse

class Doctors(Resource):
    connect(host='mongodb://admin:admin123@ds347665.mlab.com:47665/9322micro1')
    #Get available dentists
    def get(self):
        output = []
        flag = 0
        for t in Dentist.objects:
            if t.availability:
                flag = 1
                content = {}
                content['id'] = t.did
                content['name'] = t.name
                content['location'] = t.location
                content['specialization'] = t.specialization
                content['availability'] = t.availability
                output.append(content)
        print(output)
        if flag == 1:
            return output, 200, None
        else:
            return {"code": 400, "message": "No dentist available"}, 400
