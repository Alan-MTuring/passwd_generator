import hashlib
import tkinter as tk
import pyperclip
import pickle


class PasswordGenerator:
    def __init__(self, fixed_password, key):
        self.fixed_password = fixed_password
        self.key = key

    def generate_password(self, account_name, domain):
        combined = account_name + self.fixed_password + self.key + domain
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        password = hashed[:20]
        return password


class App:
    def __init__(self, root):
        self.root = root
        self.generator = None

        try:
            with open('data.pkl', 'rb') as f:
                data = pickle.load(f)
                self.fixed_password = data['fixed_password']
                self.key = data['key']
        except:
            self.fixed_password = ''
            self.key = ''

        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg='white')

        tk.Label(self.root, text='Fixed Password', bg='white').pack(
            pady=(10, 0), padx=20
        )
        self.fixed_password_entry = tk.Entry(self.root)
        self.fixed_password_entry.insert(0, self.fixed_password)
        self.fixed_password_entry.pack(pady=(0, 10), padx=20)

        tk.Label(self.root, text='Key', bg='white').pack(pady=(10, 0), padx=20)
        self.key_entry = tk.Entry(self.root)
        self.key_entry.insert(0, self.key)
        self.key_entry.pack(pady=(0, 10), padx=20)

        tk.Label(self.root, text='Account Name', bg='white').pack(pady=(10, 0), padx=20)
        self.account_name_entry = tk.Entry(self.root)
        self.account_name_entry.pack(pady=(0, 10), padx=20)

        tk.Label(self.root, text='Domain', bg='white').pack(pady=(10, 0), padx=20)
        self.domain_entry = tk.Entry(self.root)
        self.domain_entry.pack(pady=(0, 10), padx=20)

        tk.Label(self.root, text='Number of Passwords', bg='white').pack(
            pady=(10, 0), padx=20
        )
        self.num_passwords_entry = tk.Entry(self.root)
        self.num_passwords_entry.pack(pady=(0, 10), padx=20)

        self.generate_button = tk.Button(
            self.root, text='Generate Password', command=self.generate_password
        )
        self.generate_button.pack(pady=10, padx=20)

        self.passwords_var = tk.StringVar()
        self.passwords_label = tk.Label(
            self.root, textvariable=self.passwords_var, bg='white'
        )
        self.passwords_label.pack(pady=(10, 0), padx=20)

        self.copy_button = tk.Button(
            self.root, text='Copy Passwords', command=self.copy_password
        )
        self.copy_button.pack(pady=10, padx=20)

        self.copy_success_label = tk.Label(self.root, text='', bg='white')
        self.copy_success_label.pack(pady=10, padx=20)

    def generate_password(self):
        self.fixed_password = self.fixed_password_entry.get()
        self.key = self.key_entry.get()
        account_name = self.account_name_entry.get()
        domain = self.domain_entry.get()
        num_passwords = int(self.num_passwords_entry.get())

        self.generator = PasswordGenerator(self.fixed_password, self.key)
        passwords = [
            self.generator.generate_password(account_name, domain)
            for _ in range(num_passwords)
        ]

        self.passwords_var.set('\n'.join(passwords))

        with open('data.pkl', 'wb') as f:
            data = {'fixed_password': self.fixed_password, 'key': self.key}
            pickle.dump(data, f)

    def copy_password(self):
        passwords = self.passwords_var.get()
        pyperclip.copy(passwords)
        self.copy_success_label.config(text='Passwords have been copied to clipboard.')


root = tk.Tk()
app = App(root)
root.update_idletasks()
width = 500
height = int(width / 1.618)  # 黄金比例
x = (root.winfo_screenwidth() - width) / 2
y = (root.winfo_screenheight() - height) / 2
root.geometry("%dx%d+%d+%d" % (width, height, int(x), int(y)))
root.mainloop()
