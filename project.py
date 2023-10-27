import tkinter as tk
from tkinter import ttk
import sqlite3


class EmployeeDatabase:
    def __init__(self, db_name='employees.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS employees 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            last_name TEXT, 
                            first_name TEXT,
                            phone TEXT, 
                            email TEXT, 
                            salary REAL)''')
        self.conn.commit()

    def add_employee(self, last_name, first_name, phone, email, salary):
        self.cur.execute('''INSERT INTO employees (last_name, first_name, phone, email, salary) 
                            VALUES (?, ?, ?, ?, ?)''', (last_name, first_name, phone, email, salary))
        self.conn.commit()

    def update_employee(self, id, last_name, first_name, phone, email, salary):
        self.cur.execute('''UPDATE employees 
                            SET last_name=?, first_name=?, phone=?, email=?, salary=? 
                            WHERE id=?''', (last_name, first_name, phone, email, salary, id))
        self.conn.commit()

    def delete_employee(self, id):
        self.cur.execute('DELETE FROM employees WHERE id=?', (id,))
        self.conn.commit()

    def search_employee(self, name):
        self.cur.execute('SELECT * FROM employees WHERE last_name LIKE ? OR first_name LIKE ?', ('%' + name + '%', '%' + name + '%'))
        return self.cur.fetchall()

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Список сотрудников компании')
        self.db = EmployeeDatabase()

        self.tree = ttk.Treeview(root, columns=('ID', 'Фамилия', 'Имя', 'Телефон', 'Email', 'Зарплата'))
        self.tree.heading('#1', text='ID')
        self.tree.heading('#2', text='Фамилия')
        self.tree.heading('#3', text='Имя')
        self.tree.heading('#4', text='Телефон')
        self.tree.heading('#5', text='Email')
        self.tree.heading('#6', text='Зарплата')
        self.tree.pack()

        self.last_name_label = tk.Label(root, text='Фамилия')
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(root)
        self.last_name_entry.pack()

        self.first_name_label = tk.Label(root, text='Имя')
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(root)
        self.first_name_entry.pack()

        self.phone_label = tk.Label(root, text='Телефон')
        self.phone_label.pack()
        self.phone_entry = tk.Entry(root)
        self.phone_entry.pack()

        self.email_label = tk.Label(root, text='Email')
        self.email_label.pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        self.salary_label = tk.Label(root, text='Зарплата')
        self.salary_label.pack()
        self.salary_entry = tk.Entry(root)
        self.salary_entry.pack()

        self.id_label = tk.Label(root, text='ID сотрудника (для обновления/удаления)')
        self.id_label.pack()
        self.id_entry = tk.Entry(root)
        self.id_entry.pack()


        self.add_button = tk.Button(root, text='Добавить сотрудника', command=self.add_employee)
        self.add_button.pack()

        self.update_button = tk.Button(root, text='Обновить сотрудника', command=self.update_employee)
        self.update_button.pack()

        self.delete_button = tk.Button(root, text='Удалить сотрудника', command=self.delete_employee)
        self.delete_button.pack()

        self.search_button = tk.Button(root, text='Поиск', command=self.search_employee)
        self.search_button.pack()

        self.tree.bind('<ButtonRelease-1>', self.load_selected_employee)

    def load_selected_employee(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        if values:
            self.clear_entries()
            self.last_name_entry.insert(0, values[1])
            self.first_name_entry.insert(0, values[2])
            self.phone_entry.insert(0, values[3])
            self.email_entry.insert(0, values[4])
            self.salary_entry.insert(0, values[5])

    def add_employee(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        salary = float(self.salary_entry.get())
        self.db.add_employee(last_name, first_name, phone, email, salary)
        self.clear_entries()
        self.load_records()

    def update_employee(self):
        employee_id = self.id_entry.get()
        if employee_id:
            try:
                employee_id = int(employee_id)
                last_name = self.last_name_entry.get()
                first_name = self.first_name_entry.get()
                phone = self.phone_entry.get()
                email = self.email_entry.get()
                salary = float(self.salary_entry.get())
                self.db.update_employee(employee_id, last_name, first_name, phone, email, salary)
                self.clear_entries()
                self.load_records()
            except ValueError:
                print("Неправильный формат ID. Пожалуйста, введите целое число.")
        else:
            print("Введите ID сотрудника для обновления.")

    def delete_employee(self):
        employee_id = self.id_entry.get()
        if employee_id:
            try:
                employee_id = int(employee_id)
                self.db.delete_employee(employee_id)
                self.clear_entries()
                self.load_records()
            except ValueError:
                print("Неправильный формат ID. Пожалуйста, введите целое число.")
        else:
            print("Введите ID сотрудника для удаления.")
            
    def search_employee(self):
        name = self.last_name_entry.get()  # Используем поле Фамилии для поиска
        employees = self.db.search_employee(name)
        self.display_records(employees)

    def clear_entries(self):
        self.last_name_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)

    def display_records(self, employees):
        for record in self.tree.get_children():
            self.tree.delete(record)
        for employee in employees:
            self.tree.insert('', 'end', values=employee)

    def load_records(self):
        employees = self.db.search_employee('')
        self.display_records(employees)

if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    app.load_records()
    root.mainloop()
