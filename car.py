import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
import csv
import shutil

FILE_NAME = "data.csv"
INDEX_FILE = "index.txt"

def initialize_database():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["State number", "Stamp", "Year of release", "Mileage"])
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'w', encoding='utf-8') as file:
            file.write("")

def build_index():
    index = []
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for line_num, row in enumerate(reader, start=2):
            state_number = row[0]
            index.append((state_number, line_num))

    index.sort()

    with open(INDEX_FILE, 'w', encoding='utf-8') as file:
        for state_number, line_num in index:
            file.write(f"{state_number},{line_num}\n")

def binary_search_in_index(file_name, search_value):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        left, right = 0, len(lines) - 1

        while left <= right:
            mid = (left + right) // 2
            line = lines[mid].strip()
            state_number, line_num = line.split(',')

            if search_value == state_number:
                return int(line_num)
            elif search_value < state_number:
                right = mid - 1
            else:
                left = mid + 1

    return None

def search_records(display_area, reset_button):
    search_value = simpledialog.askstring("Поиск", "Введите гос номер для поиска:")
    if not search_value:
        return

    line_num = binary_search_in_index(INDEX_FILE, search_value)

    if line_num is not None:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            for current_line_num, row in enumerate(file, start=1):
                if current_line_num == line_num:
                    display_area.config(state=tk.NORMAL)
                    display_area.delete(1.0, tk.END)
                    display_area.insert(tk.END, row)
                    display_area.config(state=tk.DISABLED)
                    reset_button.config(state=tk.NORMAL)
                    return
        messagebox.showerror("Ошибка", "Запись не найдена в файле данных!")
    else:
        messagebox.showerror("Ошибка", "Запись с таким гос номером не найдена!")

def reset_search(display_area, reset_button):
    display_all_records(display_area)
    reset_button.config(state=tk.DISABLED)

def add_record(number_field, stamp_field, year_field, mil_field, display_area):
    number = number_field.get().strip()
    stamp = stamp_field.get().strip()
    year_rel = year_field.get().strip()
    mil = mil_field.get().strip()

    if not (number and stamp and year_rel and mil):
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    records = []
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                records.append(row)

    left, right = 0, len(records) - 1
    insert_pos = len(records)
    while left <= right:
        mid = (left + right) // 2
        if records[mid][0] < number:
            left = mid + 1
        else:
            right = mid - 1
            insert_pos = mid

    records.insert(insert_pos, [number, stamp, year_rel, mil])

    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if len(records) > 1:
            writer.writerows(records)
        else:
            writer.writerow(["State number", "Stamp", "Year of release", "Mileage"])
            writer.writerows(records[1:])

    build_index()
    messagebox.showinfo("Успех", "Запись добавлена!")
    display_all_records(display_area)

def display_all_records(display_area):
    records = []
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                records.append(', '.join(row))

    display_area.config(state=tk.NORMAL)
    display_area.delete(1.0, tk.END)
    if records:
        display_area.insert(tk.END, "\n".join(records))
    else:
        display_area.insert(tk.END, "База данных пуста.")
    display_area.config(state=tk.DISABLED)

def delete_record(display_area):
    num = simpledialog.askstring("Удаление", "Введите гос номер для удаления:")
    if not num:
        return

    records = []
    deleted = False
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == num:
                deleted = True
            else:
                records.append(row)

    if deleted:
        with open(FILE_NAME, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(records)

        build_index()

        messagebox.showinfo("Успех", "Запись удалена!")
    else:
        messagebox.showerror("Ошибка", "Запись с таким гос номером не найдена!")

    display_all_records(display_area)

def update_record(display_area):
    num = simpledialog.askstring("Редактирование", "Введите гос номер для редактирования:")
    if not num:
        return

    records = []
    updated = False
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == num:
                new_stamp = simpledialog.askstring("Редактирование", "Введите новую марку:")
                new_year = simpledialog.askstring("Редактирование", "Введите новый год выпуска:")
                new_mil = simpledialog.askstring("Редактирование", "Введите новый пробег:")
                row = [num, new_stamp, new_year, new_mil]
                updated = True
            records.append(row)

    if updated:
        with open(FILE_NAME, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(records)

        build_index()

        messagebox.showinfo("Успех", "Запись обновлена!")
    else:
        messagebox.showerror("Ошибка", "Запись с таким гос номер не найдена!")

    display_all_records(display_area)

def create_backup():
    backup_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if backup_file:
        shutil.copy(FILE_NAME, backup_file)
        messagebox.showinfo("Успех", "Резервная копия создана!")

def restore_backup(display_area):
    backup_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if backup_file:
        shutil.copy(backup_file, FILE_NAME)
        messagebox.showinfo("Успех", "База данных восстановлена!")
        build_index()
    display_all_records(display_area)

def setup_gui(root):
    panel = tk.Frame(root)
    panel.pack(fill=tk.X)

    number_field = tk.Entry(panel)
    stamp_field = tk.Entry(panel)
    year_field = tk.Entry(panel)
    mil_field = tk.Entry(panel)

    tk.Label(panel, text="State number").grid(row=0, column=0)
    number_field.grid(row=0, column=1)
    tk.Label(panel, text="Stamp").grid(row=1, column=0)
    stamp_field.grid(row=1, column=1)
    tk.Label(panel, text="Year of release").grid(row=2, column=0)
    year_field.grid(row=2, column=1)
    tk.Label(panel, text="Mileage").grid(row=3, column=0)
    mil_field.grid(row=3, column=1)

    buttons_panel = tk.Frame(root)
    buttons_panel.pack(fill=tk.X)

    display_area = tk.Text(root, state=tk.DISABLED)
    display_area.pack(fill=tk.BOTH, expand=True)

    reset_button = tk.Button(buttons_panel, text="Сбросить результаты поиска", state=tk.DISABLED,
                             command=lambda: reset_search(display_area, reset_button))
    reset_button.grid(row=0, column=6)
    tk.Button(buttons_panel, text="Добавить запись",
              command=lambda: add_record(number_field, stamp_field, year_field, mil_field, display_area)).grid(row=0,
                                                                                                               column=0)
    tk.Button(buttons_panel, text="Поиск", command=lambda: search_records(display_area, reset_button)).grid(row=0,
                                                                                                            column=1)
    tk.Button(buttons_panel, text="Удалить запись", command=lambda: delete_record(display_area)).grid(row=0, column=2)
    tk.Button(buttons_panel, text="Редактировать запись", command=lambda: update_record(display_area)).grid(row=0,
                                                                                                            column=3)
    tk.Button(buttons_panel, text="Создать резервную копию", command=create_backup).grid(row=0, column=4)
    tk.Button(buttons_panel, text="Восстановить из копии", command=lambda: restore_backup(display_area)).grid(row=0,
                                                                                                              column=5)

    display_all_records(display_area)
    return number_field, stamp_field, year_field, mil_field, display_area, reset_button


root = tk.Tk()
root.title("Файловая база данных автомобилей")
initialize_database()
build_index()
setup_gui(root)
root.mainloop()
