# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.doctors import Doctors
from .api.doctors_doctorsName import DoctorsDoctorsname


routes = [
    dict(resource=Doctors, urls=['/doctors'], endpoint='doctors'),
    dict(resource=DoctorsDoctorsname, urls=['/doctors/<doctorsName>'], endpoint='doctors_doctorsName'),
]