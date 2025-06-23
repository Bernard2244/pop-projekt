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

root = Tk()
root.geometry("1200x800")
root.title("Mine/Employee/Client Manager")

frame_list = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)

frame_list.grid(row=0, column=0)
frame_form.grid(row=0, column=1)
frame_details.grid(row=1, column=0, columnspan=2)
frame_map.grid(row=2, column=0, columnspan=2)

var_choice = IntVar()
Radiobutton(frame_list, text="Kopalnie", variable=var_choice, value=1, command=lambda: update_list(mines)).grid(row=0, column=0)
Radiobutton(frame_list, text="Pracownicy", variable=var_choice, value=2, command=lambda: update_list(employees)).grid(row=0, column=1)
Radiobutton(frame_list, text="Klienci", variable=var_choice, value=3, command=lambda: update_list(clients)).grid(row=0, column=2)

listbox = Listbox(frame_list, width=60, height=15)
listbox.grid(row=1, column=0, columnspan=3)
Button(frame_list, text="Pokaż", command=show_details).grid(row=2, column=0)
Button(frame_list, text="Usuń", command=remove_entity).grid(row=2, column=1)
Button(frame_list, text="Edytuj", command=edit_entity).grid(row=2, column=2)

Label(frame_form, text="Nazwa:").grid(row=0, column=0)
Label(frame_form, text="Lokalizacja:").grid(row=1, column=0)
Label(frame_form, text="Opis:").grid(row=2, column=0)

entry_name = Entry(frame_form)
entry_name.grid(row=0, column=1)
entry_location = Entry(frame_form)
entry_location.grid(row=1, column=1)
entry_desc = Entry(frame_form)
entry_desc.grid(row=2, column=1)

button_add = Button(frame_form, text="Dodaj", command=add_entity)
button_add.grid(row=3, column=0, columnspan=2)

Label(frame_details, text="Nazwa:").grid(row=0, column=0)
label_name_val = Label(frame_details, text="...")
label_name_val.grid(row=0, column=1)
Label(frame_details, text="Lokalizacja:").grid(row=0, column=2)
label_location_val = Label(frame_details, text="...")
label_location_val.grid(row=0, column=3)
Label(frame_details, text="Opis:").grid(row=0, column=4)
label_desc_val = Label(frame_details, text="...")
label_desc_val.grid(row=0, column=5)

map_widget = tkintermapview.TkinterMapView(frame_map, width=1200, height=500, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=2)

root.mainloop()
