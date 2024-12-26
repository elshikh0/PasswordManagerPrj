from tkinter import Tk, Label, Button, Entry, Frame, END, ttk, messagebox, PhotoImage
from db_operations import DbOperations
import pyperclip
import re

class root_window:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("930x500+400+120")

        self.root.config(bg="#fff")
        font_style = ("Microsoft YaHei UI Light", 12, 'bold')

        # Header
        head_title = Label(self.root, text="Password Manager", width=20, bg="#fff", fg="#57a1f8",
                           font=("Microsoft YaHei UI Light", 23, "bold"), padx=10, pady=10)
        head_title.pack(pady=10)

        # Main Frame
        self.main_frame = Frame(self.root, bg="#fff")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # CRUD Frame (Left Side)
        self.crud_frame = Frame(self.main_frame, bg="#fff")
        self.crud_frame.grid(row=0, column=0, sticky="nw")

        # Create Entry Labels and Boxes
        self.create_entry_labels_and_boxes()

        # Records Tree (Right Side)
        self.records_tree_frame = Frame(self.main_frame, bg="#fff")
        self.records_tree_frame.grid(row=0, column=1, sticky="ne", padx=10)
        self.create_records_tree()

        # Buttons (Bottom)
        self.buttons_frame = Frame(self.root, bg="#fff")
        self.buttons_frame.pack(side="bottom", fill="x", pady=10)
        self.create_crud_buttons()

    

    def create_entry_labels_and_boxes(self):
        labels_info = ('ID', 'Website', 'Username', 'Password')
        placeholders = ('ID', 'Website', 'Username', 'Password')
        self.entry_boxes = []

        def on_focus_in(event, idx):
            entry = event.widget
            if entry.get() == placeholders[idx]:
                entry.delete(0, END)
                if idx == 3:
                    entry.config(show="*")
                entry.config(fg="black")

        def on_focus_out(event, idx):
            entry = event.widget
            if not entry.get():
                entry.insert(0, placeholders[idx])
                if idx==3:
                    entry.config(show="")
                entry.config(fg="black")
                


        for idx, lbl_info in enumerate(labels_info):
            #Label(self.crud_frame, text=lbl_info, bg='#fff', fg="black", font=("Microsoft YaHei UI Light", 12, 'bold')).grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            #show = "*" if lbl_info == 'Password' else ""
            entry_box = Entry(self.crud_frame, width=20, bg="#fff", relief="sunken",border=0, font=("Microsoft YaHei UI Light", 12), fg="grey")
            entry_box.insert(0, placeholders[idx])
            if lbl_info == 'Password':
                entry_box.config(show="")
            #entry_box.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entry_box.bind("<FocusIn>", lambda e, idx=idx: on_focus_in(e, idx))
            entry_box.bind("<FocusOut>", lambda e, idx=idx: on_focus_out(e, idx))

            entry_box.grid(row=idx *2, column=1, padx=5, pady=5, sticky="w")

            line = Frame(self.crud_frame, width=150, height=2, bg='black')
            line.grid(row=idx * 2 + 1, column=1, padx=5, pady=(0, 10), sticky="w")

            image = PhotoImage(file="secure.png")
            image_label = Label(self.crud_frame, image=image, bg="#fff")
            image_label.grid(row=20,column=1, padx=50, pady=30, sticky="w")
            self.image = image

            self.entry_boxes.append(entry_box)



    


    def create_crud_buttons(self):
        buttons_info = [
            ('Save', '#57a1f8', self.save_record),
            ('Update', '#E0E0E0', self.update_record),
            ('Delete', '#E0E0E0', self.delete_record),
            ('Copy', '#E0E0E0', self.copy_password),
            ('Show All Records', '#E0E0E0', self.show_records),
            ('Show/Hide', '#E0E0E0', self.toggle_password)
        ]

        for idx, btn_info in enumerate(buttons_info):
            Button(self.buttons_frame, text=btn_info[0], bg='#57a1f8', fg="#fff", cursor="hand2", relief='raised',
                   font=("Microsoft YaHei UI Light", 10, 'bold'), width=15, command=btn_info[2]).grid(row=0, column=idx, padx=5, pady=10)

    def create_records_tree(self):
        columns = ('ID', 'Website', 'Username', 'Password')
        self.records_tree = ttk.Treeview(self.records_tree_frame, columns=columns, show='headings', height=15)
        self.records_tree.heading('ID', text="ID")
        self.records_tree.heading('Website', text="Website")
        self.records_tree.heading('Username', text="Username")
        self.records_tree.heading('Password', text="Password")
        self.records_tree['displaycolumns'] = ('Website', 'Username', 'Password')

        style = ttk.Style()
        style.configure("Treeview", background="#fff", foreground="black", fieldbackground="#C0C0C0")
        style.configure("Treeview.Heading", font=('Microsoft YaHei UI Light', 12), relief="flat", background="#A0A0A0")

        self.records_tree.pack(fill="both", expand=True)

        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                record = item['values']
                for entry_box, item in zip(self.entry_boxes, record):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item)

        self.records_tree.bind('<<TreeviewSelect>>', item_selected)

    def save_record(self):
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()
        data = {'website': website, 'username': username, 'password': password}
        self.db.create_record(data)
        self.show_records()

    def update_record(self):
        ID = self.entry_boxes[0].get()
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()
        data = {'ID': ID, 'website': website, 'username': username, 'password': password}
        self.db.update_record(data)
        self.show_records()

    def delete_record(self):
        ID = self.entry_boxes[0].get().strip()
        if not ID.isdigit():
            messagebox.showerror("Error", "Invalid ID. Please Select a Password to delete.")
            return
        self.db.delete_record(ID)
        messagebox.showinfo("Success", "Record has been deleted.")
        self.show_records()

    def show_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        records_list = self.db.show_records()
        for record in records_list:
            self.records_tree.insert('', END, values=(record[0], record[3], record[4], record[5]))

    def copy_password(self):
        selected_item = self.records_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No record selected. Please select a record.")
            return
        item = self.records_tree.item(selected_item)
        password = item['values'][3]
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password has been copied to clipboard.")

    def toggle_password(self):
        password_entry = self.entry_boxes[3]
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
        else:
            password_entry.config(show='*')


if __name__ == "__main__":
    db_class = DbOperations()
    db_class.create_table()
    root = Tk()
    root_class = root_window(root, db_class)
    root.mainloop()


