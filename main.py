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
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]

def update_list(entity_list):
    listbox.delete(0, END)
    for idx, ent in enumerate(entity_list):
        listbox.insert(idx, f"{idx + 1}. {ent.name}")

def add_entity():
    name = entry_name.get()
    location = entry_location.get()
    desc = entry_desc.get()

    if var_choice.get() == 1:
        mines.append(Entity(name, location, desc))
        update_list(mines)
    elif var_choice.get() == 2:
        employees.append(Entity(name, location, desc))
        update_list(employees)
    elif var_choice.get() == 3:
        clients.append(Entity(name, location, desc))
        update_list(clients)

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_desc.delete(0, END)

def remove_entity():
    i = listbox.index(ACTIVE)
    if var_choice.get() == 1 and i < len(mines):
        mines[i].marker.delete()
        mines.pop(i)
        update_list(mines)
    elif var_choice.get() == 2 and i < len(employees):
        employees[i].marker.delete()
        employees.pop(i)
        update_list(employees)
    elif var_choice.get() == 3 and i < len(clients):
        clients[i].marker.delete()
        clients.pop(i)
        update_list(clients)

def show_details():
    i = listbox.index(ACTIVE)
    if var_choice.get() == 1 and i < len(mines):
        ent = mines[i]
    elif var_choice.get() == 2 and i < len(employees):
        ent = employees[i]
    elif var_choice.get() == 3 and i < len(clients):
        ent = clients[i]
    else:
        return

    label_name_val.config(text=ent.name)
    label_location_val.config(text=ent.location)
    label_desc_val.config(text=ent.description)
    map_widget.set_position(ent.coordinates[0], ent.coordinates[1])
    map_widget.set_zoom(14)

def edit_entity():
    i = listbox.index(ACTIVE)
    if var_choice.get() == 1 and i < len(mines):
        ent = mines[i]
    elif var_choice.get() == 2 and i < len(employees):
        ent = employees[i]
    elif var_choice.get() == 3 and i < len(clients):
        ent = clients[i]
    else:
        return

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_desc.delete(0, END)
    entry_name.insert(0, ent.name)
    entry_location.insert(0, ent.location)
    entry_desc.insert(0, ent.description)
    button_add.config(text="Zapisz", command=lambda: update_entity(i))

def update_entity(i):
    name = entry_name.get()
    location = entry_location.get()
    desc = entry_desc.get()

    if var_choice.get() == 1 and i < len(mines):
        entity = mines[i]
    elif var_choice.get() == 2 and i < len(employees):
        entity = employees[i]
    elif var_choice.get() == 3 and i < len(clients):
        entity = clients[i]
    else:
        return

    entity.name = name
    entity.location = location
    entity.description = desc
    entity.marker.delete()
    entity.coordinates = entity.get_coordinates()
    entity.marker = map_widget.set_marker(entity.coordinates[0], entity.coordinates[1], text=entity.name)
    update_list(mines if var_choice.get() == 1 else employees if var_choice.get() == 2 else clients)
    button_add.config(text="Dodaj", command=add_entity)
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_desc.delete(0, END)