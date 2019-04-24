# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import requests
import json


def getAllDentists():
    res = requests.get('http://0.0.0.0:5002/v1/doctors')
    if res.status_code == 200:
        jsonres = res.json()
        dentistList = []
        for i in jsonres:
            j = i['name']
            dentistList.append(j)
        return dentistList

def getDentistInfo(contact):
    res = requests.get('http://0.0.0.0:5002/v1/doctors/{}'.format(contact))
    if res.status_code == 200:
        jsonres = res.json()
        location = jsonres['location']
        name = jsonres['name']
        specialization = jsonres['specialization']
        reslist = []
        reslist.append(name)
        reslist.append(location)
        reslist.append(specialization)
        return reslist
    else:
        reslist = []
        return reslist

def getAvailableTimeslots(contact):
    res1 = requests.get('http://0.0.0.0:5002/v1/doctors')
    if res1.status_code == 200:
        jsonres1 = res1.json()
        id_flag = 0
        for i in jsonres1:
            if i['name'] == contact:
                id_flag = 1
        if id_flag == 1:
            dentistID = i['id']
        else:
            dentistID = 0
    res2 = requests.get('http://0.0.0.0:5001/v2/timeslots/{}'.format(dentistID))
    if res2.status_code == 200:
        jsonres2 = res2.json()
        timeslotlist = []
        for j in jsonres2:
            if j['status'] == "available":
                timeslotlist.append(j['time'])
        return timeslotlist
    else:
        timeslotlist = []
        return timeslotlist

def reserveTimeslot(contact, datetime):
    res1 = requests.get('http://0.0.0.0:5002/v1/doctors')
    if res1.status_code == 200:
        jsonres1 = res1.json()
        id_flag = 0
        for i in jsonres1:
            if i['name'] == contact:
                id_flag = 1
        if id_flag == 1:
            dentistID = i['id']
        else:
            dentistID = 0
    res2 = requests.put('http://0.0.0.0:5001/v2/timeslots/{}?timeslot={}'.format(dentistID, datetime))
    if res2.status_code == 200:
        jsonres2 = res2.json()
        reservationinfo = []
        reservationinfo.append(jsonres2['time'])
        return reservationinfo
    else:
        reservationinfo = []
        res3 = requests.get('http://0.0.0.0:5001/v2/timeslots/{}'.format(dentistID))
        if res3.status_code == 200:
            jsonres3 = res3.json()
            counter = 0
            error_flag = 1
            for j in jsonres3:
                if j['time'] == datetime:
                    error_flag = 0
            if error_flag == 1:
                return reservationinfo
            for j in jsonres3:
                if j['status'] == "available" and counter < 3:
                    reservationinfo.append(j['time'])
                    counter += 1
            return reservationinfo

def cancelTimeslot(contact, datetime):
    res1 = requests.get('http://0.0.0.0:5002/v1/doctors')
    if res1.status_code == 200:
        jsonres1 = res1.json()
        id_flag = 0
        for i in jsonres1:
            if i['name'] == contact:
                id_flag = 1
        if id_flag == 1:
            dentistID = i['id']
        else:
            dentistID = 0
    res2 = requests.delete('http://0.0.0.0:5001/v2/timeslots/{}?timeslot={}'.format(dentistID, datetime))
    if res2.status_code == 200:
        jsonres2 = res2.json()
        cancelinfo = []
        cancelinfo.append(jsonres2['time'])
        return cancelinfo
    else:
        cancelinfo = []
        return cancelinfo


class DentistresevationExpression(Resource):
    def get(self, expression):
        result = requests.get('https://api.wit.ai/message?v=20190402&q={}'.format(expression),
                              headers={'Authorization': 'Bearer 3IRRVNR25O3YNWXTDJUTDH7QKFTSI5QN'})
        jsonResult = result.json()
        if jsonResult['entities']['intent'][0]['value'] == 'GetAvailableDentists':
            dentistlist = getAllDentists()
            if len(dentistlist) > 0:
                reply = ""
                for i in dentistlist:
                    reply = reply+"{}, ".format(i)
                reply = reply[:-1].rstrip(',')
                return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}
            else:
                reply="No doctor available."
                return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}

        elif jsonResult['entities']['intent'][0]['value'] == 'GetDentistInfo':
            contact = jsonResult['entities']['contact'][0]['value']
            dentistInfo = getDentistInfo(contact)
            if len(dentistInfo) > 0:
                reply = "{} is located in {}, specialised in {}.".format(dentistInfo[0], dentistInfo[1], dentistInfo[2])
            else:
                reply = "Please input correct doctor name (e.g. Dr.Lily)."
            return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}

        elif jsonResult['entities']['intent'][0]['value'] == 'GetAvailableTimeslots':
            contact = jsonResult['entities']['contact'][0]['value']
            timeslotlist = getAvailableTimeslots(contact)
            if len(timeslotlist) > 0:
                reply = ""
                for t in timeslotlist:
                    reply = reply + "{}, ".format(t)
                reply = reply[:-1].rstrip(',')
                return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}
            else:
                reply = "Sorry, this doctor currently has no timeslots available, or " \
                        "please check the name of the doctor (e.g. Dr.Feng). "
                return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}

        elif jsonResult['entities']['intent'][0]['value'] == 'ReserveTimeslot':
            print(jsonResult['entities'])
            contact = jsonResult['entities']['contact'][0]['value']
            datetime = jsonResult['entities']['time'][0]['value']
            reservationinfo = reserveTimeslot(contact, datetime)
            print(reservationinfo)
            if len(reservationinfo) == 1:
                reply = "Successful! Booked at {}, with {}.".format(reservationinfo[0], contact)
            elif len(reservationinfo) > 1:
                reply = "This Timeslot is already booked, please check other timeslots, such as {}, " \
                        "{}, and {}.".format(reservationinfo[0],reservationinfo[1],reservationinfo[2])
            else:
                reply = "Please check input again (e.g. reserve Dr.Feng at Monday 9:00 - 10:00 am)."
            return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}

        elif jsonResult['entities']['intent'][0]['value'] == 'CancelTimeslot':
            print(jsonResult['entities'])
            contact = jsonResult['entities']['contact'][0]['value']
            datetime = jsonResult['entities']['time'][0]['value']
            cancelinfo = cancelTimeslot(contact, datetime)
            print(cancelinfo)
            if len(cancelinfo) == 1:
                reply = "Already canceled the reservation at {} with {}.".format(cancelinfo[0], contact)
            else:
                reply = "Haven't booked yet, please check your input information."
            return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}

        elif jsonResult['entities']['intent'][0]['value'] == 'GreetingsThanks':
            if 'greetings' in jsonResult['entities']:
                reply = "Hello, nice to meet you:) How can I help you today?"
                return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}
            elif 'thanks' in jsonResult['entities']:
                reply = "You're welcome!"
                return {"response": reply}, 200, {'Access-Control-Allow-Origin': '*'}

