from tkinter import *
import tkintermapview

mines = []
employees = []
clients = []

class Entity:
    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description