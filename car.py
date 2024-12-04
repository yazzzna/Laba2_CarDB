import sqlite3
from tkinter import *
from tkinter import messagebox

class BD:
    def __init__(self):
        self.conn = sqlite3.connect("car_sharing.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS rentals (
                            id INTEGER PRIMARY KEY, 
                            car_model TEXT, 
                            rental_duration TEXT, 
                            cost TEXT, 
                            user_comment TEXT)''')
        self.cur.execute('''CREATE INDEX IF NOT EXISTS idx_car_model ON rentals (car_model)''')
        self.cur.execute('''CREATE INDEX IF NOT EXISTS idx_cost ON rentals (cost)''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM rentals")
        rows = self.cur.fetchall()
        return rows

    def insert(self, car_model, rental_duration, cost, user_comment):
        self.cur.execute("INSERT INTO rentals (car_model, rental_duration, cost, user_comment) VALUES (?, ?, ?, ?)",
                         (car_model, rental_duration, cost, user_comment))
        self.conn.commit()

    def update(self, id, car_model, rental_duration, cost, user_comment):
        self.cur.execute("UPDATE rentals SET car_model=?, rental_duration=?, cost=?, user_comment=? WHERE id=?",
                         (car_model, rental_duration, cost, user_comment, id))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM rentals WHERE id=?", (id,))
        self.conn.commit()

    def search(self, car_model="", cost=""):
        self.cur.execute("SELECT * FROM rentals WHERE car_model LIKE ? OR cost LIKE ?",
                         (f"%{car_model}%", f"%{cost}%"))
        rows = self.cur.fetchall()
        return rows


bd = BD()

def get_selected_row(event):
    global selected_tuple
    try:
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
    except IndexError:
        selected_tuple = None

def view_command():
    list1.delete(0, END)
    for row in bd.view():
        list1.insert(END, row)

def search_command():
    list1.delete(0, END)
    for row in bd.search(car_model.get(), cost.get()):
        list1.insert(END, row)

def add_command():
    bd.insert(car_model.get(), rental_duration.get(), cost.get(), user_comment.get())
    view_command()

def delete_command():
    global selected_tuple
    if selected_tuple is None:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления!")
    else:
        bd.delete(selected_tuple[0])
        view_command()
        selected_tuple = None

def update_command():
    global selected_tuple
    if selected_tuple is not None:
        bd.update(selected_tuple[0], car_model.get(), rental_duration.get(), cost.get(), user_comment.get())
        view_command()

window = Tk()
window.title("Каршеринг 1.0")

def on_closing():
    if messagebox.askokcancel("", "Закрыть программу?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

l1 = Label(window, text="Модель автомобиля")
l1.grid(row=0, column=0)

l2 = Label(window, text="Длительность аренды (часы)")
l2.grid(row=1, column=0)

l3 = Label(window, text="Стоимость аренды")
l3.grid(row=2, column=0)

l4 = Label(window, text="Комментарий")
l4.grid(row=3, column=0)

car_model = StringVar()
e1 = Entry(window, textvariable=car_model)
e1.grid(row=0, column=1)

rental_duration = StringVar()
e2 = Entry(window, textvariable=rental_duration)
e2.grid(row=1, column=1)

cost = StringVar()
e3 = Entry(window, textvariable=cost)
e3.grid(row=2, column=1)

user_comment = StringVar()
e4 = Entry(window, textvariable=user_comment)
e4.grid(row=3, column=1)

list1 = Listbox(window, height=15, width=65)
list1.grid(row=4, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="Посмотреть все", width=12, command=view_command)
b1.grid(row=2, column=3)

b2 = Button(window, text="Поиск", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Добавить", width=12, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Обновить", width=12, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Удалить", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Закрыть", width=12, command=on_closing)
b6.grid(row=7, column=3)

view_command()

window.mainloop()
