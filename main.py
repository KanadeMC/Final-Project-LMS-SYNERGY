from tkinter import ttk, simpledialog, messagebox
import sqlite3
import tkinter as tk


class EmployeeManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Employee Manager")

        # Подключаем ДБ
        self.db = sqlite3.connect("employee.db")
        self.create_table()

        # Создаём treeview
        self.tree = ttk.Treeview(master)
        self.tree["collumns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="Salary")
        self.tree.pack(padx=20, pady=20)

        self.create_widgets()
        self.update_treeview()

    def create_table(self):
        # Процесс создания таблицы Employee
        cursor = self.db.cursor
        cursor.execute("""CREATE TABLE IF NOT EXISTS Employee(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary INTEGER
                    );""")
        self.db.commit()

    def create_widgets(self):
        # Создание виджетов
        self.add_button = tk.Button(self.master, text="Добавить сотудника",
                                    command=self.add_employee)
        self.add_button.pack(pady=10)

        # Кнопка обновления
        self.update_button = tk.Button(self.master, text="Обновить сотрудника",
                                       command=self.update_employee)
        self.update_button.pack(pady=10)

        # Кнопка удаления
        self.delete_button = tk.Button(self.master, text="Удалить сотрудника",
                                       command=self.delete_employee)
        self.delete_button.pack(pady=10)

        # Кнопка поиска
        self.search_button = tk.Button(self.master, text="Искать сотрудника",
                                       command=self.search_employee)
        self.search_button.pack(pady=10)

        # Кнопка отмены действия
        self.undo_button = tk.Button(self.master, text="Назад",
                                     command=self.undo_action)
        self.undo_button.pack(pady=10)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.last_action = None  # Для хранения действия

    def add_employee(self):
        # Добавление сотрудника
        name = simpledialog.askstring("Input", "Введите полное имя сотрудника:")
        phone = simpledialog.askstring("Input", "Введите номер телефона сотрудника:")
        email = simpledialog.askstring("Input", "Введите электронную почту сотрудника:")
        salary = simpledialog.askinteger("Input", "Введите зарплату сотрудника:")

        cursor = self.db.cursor()
        cursor.execute("INSERT INTO Employee (name, phone, email, salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))

        self.db.commit()
        self.update_treeview()
        self.last_action = "add"

    def update_employee(self):
        employee_id = simpledialog.askstring("Input", "Введите ID сотрудника:")

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Employee WHERE name=?", (employee_id))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring("Input", "Введите полное имя сотрудника:", initialvalue=employee[1])
            phone = simpledialog.askstring("Input", "Введите номер телефона сотрудника:", initialvalue=employee[2])
            email = simpledialog.askstring("Input", "Введите электронную почту сотрудника:", initialvalue=employee[3])
            salary = simpledialog.askinteger("Input", "Введите зарплату сотрудника:", initialvalue=employee[4])

            cursor.execute("UPDATE Employee SET name=?, phone=?, email=?, salary=? WHERE id=?", (name, phone, email, salary, employee_id))
            self.db.commit()
            self.update_treeview()
            self.last_action = "update"

        else:
            messagebox.showerror("Error", "Работник не найден.")

    def delete_employee(self):
        employee_id = simpledialog.askinteger("Input", "Введите ID сотрудника:")

        cursor = self.db.cursor()
        cursor.execute("DELETE FROM Employee WHERE id=?", (employee_id))
        self.db.commit()
        self.update_treeview()
        self.last_action = "delete"

    def search_employee(self):
        name = simpledialog.askstring("Input", "Введите полное имя сотрудника")

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Employees WHERE name=?", (name))
        all_employees = cursor.fetchall()

        if all_employees:
            self.tree.delete(*self.tree.get_children())
            for employee in all_employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("Info", "Работника с заданным именем не найдено.")

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Employee")
        all_employees = cursor.fetchall()

        for employee in all_employees:
            self.tree.insert("", "end", values=employee)

    def on_double_click(self, event):
        # Действие при двойном клике
        item = self.tree.selection()[0]
        employee_name = self.tree.item(item, "values")[0]
        messagebox.showinfo("Employee ID", f"Имя работника: {employee_name}")

    def undo_action(self):
        # Отмена действия
        if self.last_action == "add":
            messagebox.showinfo("Undo", "Отменено добавление сотрудника")
        elif self.last_action == "update":
            messagebox.showinfo("Undo", "Отменено обновление данных сотрудника")
        elif self.last_action == "delete":
            messagebox.showinfo("Undo", "Отменено удаление сотрудника")
        else:
            messagebox.showinfo("Undo", "Нет действия которое возможно бы было отменить")

    def on_closing(self):
        # Логика заврешения работы
        self.db.close()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManager
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
