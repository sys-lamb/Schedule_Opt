#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:41:15 2020

@author: alexlamb
"""

class Employee:

    name = None
    email = None
    hourly_rate = 0
    availability = []
    shifts = []
       
    def __init__(self, name, email, hourly_rate):
        self.name = name 
        self.email = email
        self.hourly_rate = hourly_rate
    
    def add_shift(self, shift):
        self.shifts.append(shift)
        
    def remove_shift(self, shift):
        self.shifts.remove(shift)
        
    def set_availability(self, availability):
        self.availability = availability

class Shift:
    
    day_of_week = None
    start_hour = None
    end_hour = None
    duration = None
    employees = []

    def __init__(self, day_of_week, start_hour, end_hour):
        self.day_of_week = day_of_week
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.duration = self.end_hour - self.start_hour

    def add_employee(self, employee):
        self.employees.append(employee)
        
    def remove_employee(self, employee):
        self.employees.remove(employee)
        
class LaborHour:

    day_of_week = None
    hour_number = None
    labor_need = 0
    labor_coverage = 0
    labor_diff = 0
    shifts = []
       
    def __init__(self, day_of_week, hour_number, labor_need):
        self.day_of_week = day_of_week 
        self.hour_number = hour_number
        self.labor_need = labor_need
        
    def update_labor_coverage(self, change):
        self.labor_coverage += change
        self.labor_diff = self.labor_coverage - self.labor_need

    def add_shift(self, shift):
        self.shifts.append(shift)
        self.labor_coverage += 1
        self.labor_diff = self.labor_coverage - self.labor_need
        
    def remove_shift(self, shift):
        self.shifts.remove(shift)
        self.labor_coverage -= 1
        self.labor_diff = self.labor_coverage - self.labor_need
               
        
        
        
        
        
        
        
        
