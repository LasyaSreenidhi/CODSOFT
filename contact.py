import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database setup
def setup_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY, 
                 name TEXT, 
                 phone TEXT, 
                 email TEXT, 
                 address TEXT)''')
    conn.commit()
    conn.close()

# Add Contact
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    
    if name and phone:
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", 
                  (name, phone, email, address))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Contact added successfully!")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Name and Phone are required!")

# View Contacts
def view_contacts():
    for row in contact_list.get_children():
        contact_list.delete(row)
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT name, phone FROM contacts")
    rows = c.fetchall()
    for row in rows:
        contact_list.insert("", "end", values=row)
    conn.close()

# Search Contact
def search_contact():
    search_term = search_entry.get()
    for row in contact_list.get_children():
        contact_list.delete(row)
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?", 
              ('%' + search_term + '%', '%' + search_term + '%'))
    rows = c.fetchall()
    for row in rows:
        contact_list.insert("", "end", values=row)
    conn.close()

# Update Contact
def update_contact():
    selected_item = contact_list.selection()
    if selected_item:
        contact_name, contact_phone = contact_list.item(selected_item[0], "values")
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if name and phone:
            conn = sqlite3.connect('contacts.db')
            c = conn.cursor()
            c.execute("UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE name = ? AND phone = ?", 
                      (name, phone, email, address, contact_name, contact_phone))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Contact updated successfully!")
            clear_entries()
            view_contacts()
        else:
            messagebox.showwarning("Input Error", "Name and Phone are required!")
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to update.")

# Delete Contact
def delete_contact():
    selected_item = contact_list.selection()
    if selected_item:
        contact_name, contact_phone = contact_list.item(selected_item[0], "values")
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("DELETE FROM contacts WHERE name = ? AND phone = ?", (contact_name, contact_phone))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Contact deleted successfully!")
        view_contacts()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# Clear Entries
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Select Contact
def select_contact(event):
    selected_item = contact_list.selection()
    if selected_item:
        name, phone = contact_list.item(selected_item[0], "values")
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("SELECT * FROM contacts WHERE name = ? AND phone = ?", (name, phone))
        contact = c.fetchone()
        conn.close()
        clear_entries()
        name_entry.insert(0, contact[1])
        phone_entry.insert(0, contact[2])
        email_entry.insert(0, contact[3])
        address_entry.insert(0, contact[4])

# GUI setup
app = tk.Tk()
app.title("Contact Management")

# Frames
frame1 = tk.Frame(app)
frame1.pack(pady=10)
frame2 = tk.Frame(app)
frame2.pack(pady=10)
frame3 = tk.Frame(app)
frame3.pack(pady=10)

# Labels and Entries
tk.Label(frame1, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(frame1)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame1, text="Phone").grid(row=1, column=0, padx=5, pady=5)
phone_entry = tk.Entry(frame1)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame1, text="Email").grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(frame1)
email_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame1, text="Address").grid(row=3, column=0, padx=5, pady=5)
address_entry = tk.Entry(frame1)
address_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
add_btn = tk.Button(frame1, text="Add Contact", command=add_contact)
add_btn.grid(row=4, column=0, padx=5, pady=5)

update_btn = tk.Button(frame1, text="Update Contact", command=update_contact)
update_btn.grid(row=4, column=1, padx=5, pady=5)

delete_btn = tk.Button(frame1, text="Delete Contact", command=delete_contact)
delete_btn.grid(row=5, column=0, padx=5, pady=5)

clear_btn = tk.Button(frame1, text="Clear", command=clear_entries)
clear_btn.grid(row=5, column=1, padx=5, pady=5)

view_btn = tk.Button(frame1, text="View Contacts", command=view_contacts)
view_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Search
tk.Label(frame2, text="Search").grid(row=0, column=0, padx=5, pady=5)
search_entry = tk.Entry(frame2)
search_entry.grid(row=0, column=1, padx=5, pady=5)
search_btn = tk.Button(frame2, text="Search", command=search_contact)
search_btn.grid(row=0, column=2, padx=5, pady=5)

# Contact List
contact_list = ttk.Treeview(frame3, columns=("Name", "Phone"), show="headings")
contact_list.heading("Name", text="Name")
contact_list.heading("Phone", text="Phone")
contact_list.pack()

contact_list.bind("<<TreeviewSelect>>", select_contact)

# Initialize
setup_db()

app.mainloop()