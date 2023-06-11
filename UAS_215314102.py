import tkinter as tk
from tkinter import messagebox
import bcrypt
import csv
import mysql.connector
from tkinter import ttk
from mysql.connector import Error
import pandas as pd

# Establish the database connection
db = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="ticket_shop"  # Replace with the desired database name
)

# Create a cursor object to interact with the database
cursor = db.cursor()

def create_user_table():
    # Define the SQL statement to create the "user" table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(255),
        email VARCHAR(255),
        nomer_telpon VARCHAR(20),
        password VARCHAR(255)
    )
    """

    # Execute the SQL statement to create the table
    cursor.execute(create_table_query)

    # Commit the changes to the database
    db.commit()



def create_payment_table():
    # Define the SQL statement to create the "kereta" table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS payment (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(255),
        nik VARCHAR(255),
        kota_tujuan VARCHAR(255),
        kereta VARCHAR(255),
        waktu_keberangkatan VARCHAR(255),
        total_harga INT
    )
    """

    # Execute the SQL statement to create the table
    cursor.execute(create_table_query)

    # Commit the changes to the database
    db.commit()


class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Ticket Shop")
        self.window.geometry("1280x720")  # Set the window size to 1280x720
        self.window.configure(bg="#9179A3")

        self.create_widgets()

    def create_widgets(self):
        # Create and configure the email label and entry field
        self.email_label = tk.Label(self.window, text="Email:")
        self.email_label.pack()

        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack()

        # Create and configure the password label and entry field
        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        # Create the login button
        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.login_button.pack()

        # Create the register button
        self.register_button = tk.Button(self.window, text="Register", command=self.open_registration)
        self.register_button.pack()

    def login(self):
        # Get input from the user for email and password
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Execute SQL query to retrieve the hashed password for the provided email
        query = "SELECT password FROM user WHERE email = %s"
        values = (email,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            # Compare the stored hashed password with the user-provided password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # Display a message that the login is successful
                messagebox.showinfo("Login", "Login successful!")
                self.window.destroy()  # Close the login window
                home = Home()  # Create an instance of TicketShopGUI
                home.run()  # Run the TicketShopGUI application
            else:
                # Display a message that the password is incorrect and prompt the user to try again
                messagebox.showerror("Login Error", "Incorrect password. Please try again.")
        else:
            # Display a message that the email is incorrect and prompt the user to try again
            messagebox.showerror("Login Error", "Incorrect email. Please try again.")


    def open_registration(self):
        # Close the login window
        self.window.destroy()

        # Open the registration window
        registration = Registration()
        registration.run()

    def run(self):
        self.window.mainloop()


class Registration:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Registration")
        self.window.geometry("1280x720")  # Set the window size to 1280x720
        self.window.configure(bg="#9179A3")

        self.create_widgets()

    def create_widgets(self):
        # Create and configure the name label and entry field
        self.name_label = tk.Label(self.window, text="Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack()

        # Create and configure the email label and entry field
        self.email_label = tk.Label(self.window, text="Email:")
        self.email_label.pack()

        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack()

        # Create and configure the phone number label and entry field
        self.phone_label = tk.Label(self.window, text="Phone Number:")
        self.phone_label.pack()

        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.pack()

        # Create and configure the password label and entry field
        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        # Create and configure the confirm password label and entry field
        self.confirm_password_label = tk.Label(self.window, text="Confirm Password:")
        self.confirm_password_label.pack()

        self.confirm_password_entry = tk.Entry(self.window, show="*")
        self.confirm_password_entry.pack()

        # Create the register button
        self.register_button = tk.Button(self.window, text="Register", command=self.register)
        self.register_button.pack()

        # Create the back button to return to the login window
        self.back_button = tk.Button(self.window, text="Back", command=self.back_to_login)
        self.back_button.pack()

    def register(self):
        # Get input from the user for name, email, phone number, password, and confirm password
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check if any field is empty
        if name == "" or email == "" or phone == "" or password == "" or confirm_password == "":
            messagebox.showerror("Registration Error", "Please fill in all fields.")
            return

        # Check if the password and confirm password match
        if password != confirm_password:
            messagebox.showerror("Registration Error", "Password and Confirm Password do not match.")
            return

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Execute SQL query to insert the user details into the users table
        query = "INSERT INTO user (nama, email, nomer_telpon, password) VALUES (%s, %s, %s, %s)"
        values = (name, email, phone, hashed_password.decode('utf-8'))
        cursor.execute(query, values)
        db.commit()

        # Display a message that the registration is successful and prompt the user to login
        messagebox.showinfo("Registration", "Registration successful! Please login.")

        # Close the registration window
        self.window.destroy()

        # Open the login window
        login = Login()
        login.run()

    def back_to_login(self):
        # Close the registration window
        self.window.destroy()

        # Open the login window
        login = Login()
        login.run()

    def run(self):
        self.window.mainloop()



class Home:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Ticket Shop")
        self.window.geometry("1280x720")
        self.window.configure(bg="#9179A3")
        self.create_widgets()

    def create_widgets(self):
        # Create the "Input Data" button on the left side
        self.input_button = tk.Button(self.window, text="Input Data", command=self.input_data)
        self.input_button.place(relx=0.2, rely=0.5, anchor=tk.CENTER)

        # Create the "Keluar Program" button on the right side
        self.exit_button = tk.Button(self.window, text="Keluar Program", command=self.exit_program)
        self.exit_button.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

    def input_data(self):
        # Display a message box when the "Input Data" button is clicked
        messagebox.showinfo("Input Data", "Input Data button clicked!")
        buyTicket=InputData()
    def exit_program(self):
        # Exit the program when the "Keluar Program" button is clicked
        self.window.destroy()

    def run(self):
        self.window.mainloop()

class Ticket:
    def __init__(self, harga):
        self.harga = harga

    def beli_tiket(self, input_data):
        df = pd.DataFrame(input_data)
        df['Umur'] = df['Umur'].astype(int)
        df['ValidAge'] = df['Umur'].apply(self.is_valid_age)
        valid_data = df[df['ValidAge']]

        if len(valid_data) != len(df):
            print(f"Maaf, tiket {self.jenis_tiket} hanya dapat dibeli untuk {self.jenis_tiket}.")
            return 0

        total_harga = valid_data.shape[0] * self.harga
        return total_harga

    def is_valid_age(self, usia):
        raise NotImplementedError("Subclasses must implement is_valid_age method.")


class TiketAnak(Ticket):
    def __init__(self):
        super().__init__(50000)
        self.jenis_tiket = "anak-anak"

    def is_valid_age(self, usia):
        return usia < 18


class TiketDewasa(Ticket):
    def __init__(self):
        super().__init__(100000)
        self.jenis_tiket = "dewasa"

    def is_valid_age(self, usia):
        return usia >= 18

class InputData:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.configure(bg="#9179A3")

        self.jumlah_label = tk.Label(
            self.window,
            text="Jumlah Penumpang:",
            font=("Mina Regular", 12),
            bg="#9179A3",
            fg="white"
        )
        self.jumlah_label.pack()
        self.jumlah_entry = tk.Entry(self.window)
        self.jumlah_entry.pack(pady=10)

        self.submit_button = tk.Button(
            self.window,
            text="Submit",
            font=("Mina Regular", 12),
            bg="#755A7C",
            fg="white",
            command=self.submit_data
        )
        self.submit_button.pack(pady=10)

        self.passenger_entries = []
        self.data = []  # Array untuk menyimpan data penumpang

        self.window.mainloop()

    def submit_data(self):
        jumlah_penumpang = int(self.jumlah_entry.get())

        for i in range(jumlah_penumpang):
            passenger_number = i + 1

            nik_label = tk.Label(
                self.window,
                text=f"NIK Penumpang {passenger_number}:",
                font=("Mina Regular", 12),
                bg="#9179A3",
                fg="white"
            )
            nik_label.pack()
            nik_entry = tk.Entry(self.window)
            nik_entry.pack()

            nama_label = tk.Label(
                self.window,
                text=f"Nama Penumpang {passenger_number}:",
                font=("Mina Regular", 12),
                bg="#9179A3",
                fg="white"
            )
            nama_label.pack()
            nama_entry = tk.Entry(self.window)
            nama_entry.pack()

            umur_label = tk.Label(
                self.window,
                text=f"Umur Penumpang {passenger_number}:",
                font=("Mina Regular", 12),
                bg="#9179A3",
                fg="white"
            )
            umur_label.pack()
            umur_entry = tk.Entry(self.window)
            umur_entry.pack()

            nomer_label = tk.Label(
                self.window,
                text=f"Nomer Telpon Penumpang {passenger_number}:",
                font=("Mina Regular", 12),
                bg="#9179A3",
                fg="white"
            )
            nomer_label.pack()
            nomer_entry = tk.Entry(self.window)
            nomer_entry.pack()

            spacer_label = tk.Label(
                self.window,
                text="",
                bg="#9179A3"
            )
            spacer_label.pack()

            self.passenger_entries.append((nik_entry, nama_entry, umur_entry, nomer_entry))

        submit_button = tk.Button(
            self.window,
            text="Submit",
            font=("Mina Regular", 12),
            bg="#755A7C",
            fg="white",
            command=self.save_data
        )
        submit_button.pack(pady=10)

    def save_data(self):
        self.data = []  # Mengosongkan array data sebelum mengisi dengan data baru

        for entry_tuple in self.passenger_entries:
            nik = entry_tuple[0].get()
            nama = entry_tuple[1].get()
            umur = entry_tuple[2].get()
            nomer = entry_tuple[3].get()

            self.data.append((nik, nama, umur, nomer))

        self.window.destroy()
        payment_window = PaymentWindow(self.data)


class PaymentWindow:
    def __init__(self, data):
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.configure(bg="#9179A3")

        self.data = data

        self.kota_var = tk.StringVar(self.window)
        self.kota_var.set("Pilih Kota Asal")

        self.kota_label = tk.Label(
            self.window,
            text="Kota Asal:",
            font=("Mina Regular", 12),
            bg="#9179A3",
            fg="white"
        )
        self.kota_label.pack()
        self.kota_optionmenu = tk.OptionMenu(self.window, self.kota_var, "Jakarta", "Surabaya", "Yogyakarta")
        self.kota_optionmenu.pack(pady=10)

        self.kereta_var = tk.StringVar(self.window)
        self.kereta_var.set("Pilih Kereta")

        self.kereta_label = tk.Label(
            self.window,
            text="Kereta:",
            font=("Mina Regular", 12),
            bg="#9179A3",
            fg="white"
        )
        self.kereta_label.pack()
        self.kereta_optionmenu = tk.OptionMenu(self.window, self.kereta_var, "Argo Bromo Anggrek", "Gajayana", "Matarmaja")
        self.kereta_optionmenu.pack(pady=10)

        self.waktu_var = tk.StringVar(self.window)
        self.waktu_var.set("Pilih Waktu")

        self.waktu_label = tk.Label(
            self.window,
            text="Waktu:",
            font=("Mina Regular", 12),
            bg="#9179A3",
            fg="white"
        )
        self.waktu_label.pack()
        self.waktu_optionmenu = tk.OptionMenu(self.window, self.waktu_var, "08:00", "13:00", "19:00")
        self.waktu_optionmenu.pack(pady=10)

        self.submit_button = tk.Button(
            self.window,
            text="Submit",
            font=("Mina Regular", 12),
            bg="#755A7C",
            fg="white",
            command=self.submit_data
        )
        self.submit_button.pack(pady=10)

        self.window.mainloop()

    def submit_data(self):
        if self.kota_var.get() == "Pilih Kota Asal" or self.kereta_var.get() == "Pilih Kereta" or self.waktu_var.get() == "Pilih Waktu":
            messagebox.showerror("Error", "Mohon pilih kota asal, kereta, dan waktu")
        else:
            self.window.destroy()
            payment_confirmation_window = PaymentConfirmationWindow(self.data, self.kota_var.get(), self.kereta_var.get(), self.waktu_var.get())


class PaymentConfirmationWindow:
    def __init__(self, data, kota, kereta, waktu):
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.configure(bg="#9179A3")

        self.data = data
        self.kota = kota
        self.kereta = kereta
        self.waktu = waktu

        self.confirmation_label = tk.Label(
            self.window,
            text="Konfirmasi Pembayaran",
            font=("Mina Regular", 16),
            bg="#9179A3",
            fg="white"
        )
        self.confirmation_label.pack(pady=10)

        self.kota_label = tk.Label(
            self.window,
            text=f"Kota Asal: {self.kota}",
            font=("Mina Regular", 12),
            bg="#9179A3",
            fg="white"
        )
        self.kota_label.pack()

        self.kereta_label = tk.Label(
            self.window,
            text=f"Kereta: {self.kereta}",
            font=("Mina Regular", 12),
            bg="#9179A3",
            fg="white"
        )
        self.kereta_label.pack()

        self.waktu_label = tk.Label(
            self.window,
            text=f"Waktu: {self.waktu}",
            font=("Mina Regular", 12),
            bg="#9179A3",
            fg="white"
        )
        self.waktu_label.pack()

        self.passenger_label = tk.Label(
            self.window,
            text="Data Penumpang",
            font=("Mina Regular", 14),
            bg="#9179A3",
            fg="white"
        )
        self.passenger_label.pack(pady=10)

        self.passenger_treeview = ttk.Treeview(
            self.window,
            columns=("NIK", "Nama", "Umur", "Nomor Telepon"),
            show="headings",
            selectmode="none"
        )
        self.passenger_treeview.pack()

        self.passenger_treeview.heading("NIK", text="NIK")
        self.passenger_treeview.heading("Nama", text="Nama")
        self.passenger_treeview.heading("Umur", text="Umur")
        self.passenger_treeview.heading("Nomor Telepon", text="Nomor Telepon")

        self.passenger_treeview.column("NIK", width=100)
        self.passenger_treeview.column("Nama", width=200)
        self.passenger_treeview.column("Umur", width=100)
        self.passenger_treeview.column("Nomor Telepon", width=150)

        for passenger in self.data:
            self.passenger_treeview.insert("", tk.END, values=passenger)

        self.confirm_button = tk.Button(
            self.window,
            text="Konfirmasi",
            font=("Mina Regular", 12),
            bg="#755A7C",
            fg="white",
            command=self.save_data
        )
        self.confirm_button.pack(pady=10)

        self.window.mainloop()

    def save_data(self):
        try:
            cursor = db.cursor()
            total_harga = 0

            with open("transaction_data.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["NIK", "Nama", "Umur", "Nomor Telepon", "Total Harga"])

                for passenger in self.data:
                    nik = passenger[0]
                    nama = passenger[1]
                    umur = int(passenger[2])
                    nomer = passenger[3]

                    # Determine the ticket type based on age
                    if umur < 18:
                        ticket = TiketAnak()
                    else:
                        ticket = TiketDewasa()

                    harga = ticket.beli_tiket([{"Umur": umur}])
                    total_harga += harga

                    # Menjalankan perintah SQL untuk memasukkan data pembayaran ke dalam tabel
                    insert_query = """
                    INSERT INTO payment (nama, nik, kota_tujuan, kereta, waktu_keberangkatan, total_harga)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    values = (nama, nik, self.kota, self.kereta, self.waktu, harga)
                    cursor.execute(insert_query, values)

                    writer.writerow([nik, nama, umur, nomer, harga])

            db.commit()
            cursor.close()
            db.close()

            messagebox.showinfo("Info", "Data penumpang berhasil disimpan. Total harga: Rp" + str(total_harga))
        except Exception as e:
            messagebox.showerror("Error", "Terjadi kesalahan dalam menyimpan data penumpang: " + str(e))

        self.window.destroy()


if __name__ == "__main__":
    create_user_table() #Untuk Generate Table User ketika program di jalankan
    create_payment_table() #Untuk Generate Table Payment ketika program dijalankan
    # Create an instance of the Login class
    login = Login()
    login.run()