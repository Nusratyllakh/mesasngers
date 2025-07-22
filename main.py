import tkinter as tk
from tkinter import messagebox
import requests
from style import style

SERVER_URL = 'http://127.0.0.1:5000'  # адрес вашего сервера

class MessengerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Офисный Мессенджер")
        self.root.configure(bg=style['bg'])
        self.username = None
        self.login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Добро пожаловать", font=("Segoe UI", 16), bg=style['bg'], fg=style['fg']).pack(pady=20)

        tk.Button(self.root, text="Войти", font=style['font'], width=20, bg=style['btn_bg'], command=self.login_form).pack(pady=10)
        tk.Button(self.root, text="Зарегистрироваться", font=style['font'], width=20, bg=style['btn_bg'], command=self.register_form).pack(pady=10)

    def register_form(self):
        self.clear_screen()
        tk.Label(self.root, text="Регистрация", font=("Segoe UI", 14), bg=style['bg'], fg=style['fg']).pack(pady=10)

        username = tk.Entry(self.root, font=style['font'], bg=style['entry_bg'], fg=style['fg'])
        username.pack(pady=5)
        username.insert(0, "Имя пользователя")

        password = tk.Entry(self.root, font=style['font'], bg=style['entry_bg'], fg=style['fg'], show='*')
        password.pack(pady=5)
        password.insert(0, "Пароль")

        def do_register():
            data = {"username": username.get(), "password": password.get()}
            resp = requests.post(f"{SERVER_URL}/register", json=data)
            if resp.ok:
                messagebox.showinfo("Успешно", "Вы зарегистрированы!")
                self.login_screen()
            else:
                messagebox.showerror("Ошибка", resp.json().get('error', 'Ошибка регистрации'))

        tk.Button(self.root, text="Зарегистрироваться", bg=style['btn_bg'], font=style['font'], command=do_register).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.login_screen).pack()

    def login_form(self):
        self.clear_screen()
        tk.Label(self.root, text="Вход", font=("Segoe UI", 14), bg=style['bg'], fg=style['fg']).pack(pady=10)

        username = tk.Entry(self.root, font=style['font'], bg=style['entry_bg'], fg=style['fg'])
        username.pack(pady=5)
        username.insert(0, "Имя пользователя")

        password = tk.Entry(self.root, font=style['font'], bg=style['entry_bg'], fg=style['fg'], show='*')
        password.pack(pady=5)
        password.insert(0, "Пароль")

        def do_login():
            data = {"username": username.get(), "password": password.get()}
            resp = requests.post(f"{SERVER_URL}/login", json=data)
            if resp.ok:
                self.username = username.get()
                self.chat_screen()
            else:
                messagebox.showerror("Ошибка", resp.json().get('error', 'Ошибка входа'))

        tk.Button(self.root, text="Войти", bg=style['btn_bg'], font=style['font'], command=do_login).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.login_screen).pack()

    def chat_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Вы вошли как {self.username}", font=style['font'], bg=style['bg'], fg=style['fg']).pack(pady=5)

        messages_frame = tk.Frame(self.root, bg=style['bg'])
        messages_frame.pack()

        scrollbar = tk.Scrollbar(messages_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_list = tk.Listbox(messages_frame, height=15, width=60, font=style['font'], bg=style['entry_bg'], fg=style['fg'], yscrollcommand=scrollbar.set)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.message_list.yview)

        self.entry_field = tk.Entry(self.root, font=style['font'], width=50, bg=style['entry_bg'], fg=style['fg'])
        self.entry_field.pack(pady=10)
        self.entry_field.bind("<Return>", lambda event: self.send_message())

        tk.Button(self.root, text="Отправить", bg=style['btn_bg'], font=style['font'], command=self.send_message).pack()

        self.load_messages()

    def load_messages(self):
        self.message_list.delete(0, tk.END)
        try:
            resp = requests.get(f"{SERVER_URL}/messages")
            if resp.ok:
                for msg in resp.json():
                    self.message_list.insert(tk.END, f"{msg['sender']}: {msg['content']}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить сообщения")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def send_message(self):
        msg = self.entry_field.get().strip()
        if msg:
            data = {"sender": self.username, "content": msg}
            try:
                resp = requests.post(f"{SERVER_URL}/messages", json=data)
                if resp.ok:
                    self.entry_field.delete(0, tk.END)
                    self.load_messages()
                else:
                    messagebox.showerror("Ошибка", "Не удалось отправить сообщение")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

root = tk.Tk()
root.geometry("500x500")
app = MessengerApp(root)
root.mainloop()
