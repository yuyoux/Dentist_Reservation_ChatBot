# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

from .model import Timeslots
from mongoengine import connect
from flask_restful import reqparse

class TimeslotsId(Resource):
    connect(host='mongodb://admin:admin123@ds151612.mlab.com:51612/9322micro2')
    # Get available timeslots for each dentist
    def get(self, id):
        for t in Timeslots.objects:
            if t.did == id:
                return t.timeslist, 200, None
        return {"code": 404, "message": "Id not found"}, 404

    # Reserve timeslot
    def put(self, id):
        print(g.args)
        parser = reqparse.RequestParser()
        parser.add_argument('timeslot', type=str, required=True, help='timeslot input error')
        args = parser.parse_args()
        timeslot = args.get("timeslot")
        flag = 0
        for t in Timeslots.objects:
            for re in t.timeslist:
                if re.time == timeslot and re.status == "available":
                    re.status = "reserved"
                    t.save()
                    flag = 1
                    tmp = re
        if flag == 1:
            return tmp, 200, None
        else:
            return {"code": 400, "message": "Not Booked"}, 400

    # Cancelling appointment
    def delete(self, id):
        print(g.args)
        parser = reqparse.RequestParser()
        parser.add_argument('timeslot', type=str, required=True, help='timeslot input error')
        args = parser.parse_args()
        timeslot = args.get("timeslot")
        flag = 0
        for t in Timeslots.objects:
            for re in t.timeslist:
                if re.time == timeslot and re.status == "reserved":
                    re.status = "available"
                    t.save()
                    flag = 1
                    tmp = re
        if flag == 1:
            return tmp, 200, None
        else:
            return {"code": 400, "message": "Not Canceled"}, 400