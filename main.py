from tkinter import *
import psycopg
from tkinter import messagebox
import customtkinter

root = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
root.geometry('500x470+200+100')
root.title('Visitors')
root.resizable(False, False)

# FRAMES
general_frame = customtkinter.CTkFrame(root, fg_color='transparent')
general_frame.pack()

heading_input_frame = customtkinter.CTkFrame(root, fg_color='transparent')
heading_input_frame.pack()

input_frame = customtkinter.CTkFrame(root, fg_color='transparent')
input_frame.pack()

heading_operations_frame = customtkinter.CTkFrame(root, fg_color='transparent')
heading_operations_frame.pack()

id_frame = customtkinter.CTkFrame(root, fg_color='transparent')
id_frame.pack()

button_frame = customtkinter.CTkFrame(root, fg_color='transparent')
button_frame.pack()

heading_content_frame = customtkinter.CTkFrame(root, fg_color='transparent')
heading_content_frame.pack()

content_frame = customtkinter.CTkFrame(root, fg_color='transparent')
content_frame.pack()

## FUNCTIONS section
# function to create table
def create():
    try:
        query = '''CREATE TABLE IF NOT EXISTS visitors (
                id SERIAL PRIMARY KEY,
                first_name TEXT,
                second_name TEXT,
                age INT 
                )'''
        with psycopg.connect(dbname='visitorsdb', user='myuser', password='admin', host='localhost', port='5432') as connection:
            with connection.cursor() as cur:
                cur.execute(query)
    except psycopg.DatabaseError as e:
        print(f'Error database: {e}')
    except Exception as e:
        print(f'Error: {e}')
create()

# fuction to insert data into database
def insert_data(first_name, second_name, age):

    try:
        first_name = first_name_entry.get()
        second_name = second_name_entry.get()
        age = age_entry.get()

        first_name = str(first_name)
        second_name = str(second_name)
        age = int(age)

        first_name_entry.delete(0, END)
        second_name_entry.delete(0, END)
        age_entry.delete(0, END)
    
        if first_name == '' or second_name == '' or age == '':
            messagebox.showinfo('Status', 'Set all inputs, please.')
        else:    
            query = '''INSERT INTO visitors (first_name, second_name, age)
                    VALUES (%s, %s, %s)'''
            with psycopg.connect(dbname='visitorsdb', user='myuser', password='admin', host='localhost', port='5432') as connection:
                with connection.cursor() as cur:
                    cur.execute(query, (first_name, second_name, age))
                    messagebox.showinfo('Status', 'New visitor was succesfully added.')

    except psycopg.errors.InvalidTextRepresentation:
        messagebox.showerror('Error', 'Set correct values !')
    except ValueError:
        messagebox.showerror('Error', 'Set correct values !')
    except psycopg.DatabaseError as e:
        print(f'Error databse: {e}')
    except Exception as e:
        print(f'Error: {e}')

# function to find selected visitor from database by his ID
def search(id):
    try:
        id = id_entry.get()
        id = int(id)

        query = '''SELECT * FROM visitors WHERE id = %s'''
        with psycopg.connect(dbname='visitorsdb', user='myuser', password='admin', host='localhost', port='5432') as connection:
            with connection.cursor() as cur:
                cur.execute(query, (id,))
                selected_visitor = cur.fetchone()
                if selected_visitor:
                    search_listbox = Listbox(content_frame, width=20, height=1, justify='center', font=('Arial', 15), bg='black', fg='White')
                    search_listbox.insert(0, selected_visitor)
                    search_listbox.grid(row=0, column=0)
                else:
                    messagebox.showerror('Error', 'ID not exists !')
                
    except psycopg.errors.InvalidTextRepresentation:
        messagebox.showerror('Error', 'Set correct ID value !')
    except ValueError:
        messagebox.showerror('Error', 'Set correct ID value !')
    except psycopg.DatabaseError as e:
        print(f'Error databse: {e}')
    except Exception as e:
        print(f'Error: {e}')

# listbox to display all visitors - part of content section 
listbox = Listbox(content_frame, width=40, height=5, font=('Arial', 15), bg='black', fg='White')
listbox.grid(row=1, column=0)

scrollbar = Scrollbar(content_frame)
scrollbar.grid(row=1, column=2, sticky='nsw')

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# function to display all visitor in listbox
def display_all_visitors():
    listbox.delete(0, END)
    try:
        query = '''SELECT * FROM visitors'''
        with psycopg.connect(dbname='visitorsdb', user='myuser', password='admin', host='localhost', port='5432') as connection:
            with connection.cursor() as cur:
                cur.execute(query)
                all_visitors = cur.fetchall()
                for one_visitor in all_visitors:
                    listbox.insert(0, one_visitor)
    except psycopg.DatabaseError as e:
        print(f'Error database: {e}')
    except Exception as e:
        print(f'Error: {e}')
        
display_all_visitors()

# function to delete selected visitor from database by his ID
def delete(id):
    try:
        id = id_entry.get()
        id = int(id)

        select_query = '''SELECT id FROM visitors WHERE id = %s'''
        delete_query = '''DELETE FROM visitors WHERE id = %s'''

        with psycopg.connect(dbname='visitorsdb', user='myuser', password='admin', host='localhost', port='5432') as connection:
            with connection.cursor() as cur:
                cur.execute(select_query, (id,))
                result = cur.fetchone()
                if not result:
                    messagebox.showerror('Error', 'ID not exists !')
                    return

                cur.execute(delete_query, (id,)) 
                listbox.delete(ANCHOR)
                messagebox.showinfo('Status', 'Selected visitor was succesfully deleted!')
                                     
    except Exception as e:
        print(f'Error: {e}')

# function to update values in database
def update(first_name, second_name, age, id):
    try:
        first_name = first_name_entry.get()
        second_name = second_name_entry.get()
        age = age_entry.get()
        id = id_entry.get()

        first_name_entry.delete(0, END)
        second_name_entry.delete(0, END)
        age_entry.delete(0, END)
        id_entry.delete(0, END)

        if first_name == '' or second_name == '' or age == '' or id == '': 
            messagebox.showwarning('Warning', 'You must fill First name, Second name, Age and ID !')
        else:
            query_select = '''SELECT id FROM visitors WHERE id = %s'''
            query_update = '''UPDATE visitors
                                SET first_name = %s,
                                    second_name = %s,
                                    age = %s
                                WHERE id = %s'''
            
            with psycopg.connect(dbname='visitorsdb', user='myuser', password='admin', host='localhost', port='5432') as connection:
                with connection.cursor() as cur:
                    cur.execute(query_select, (id,))
                    result = cur.fetchone()
                    if not result:
                        messagebox.showerror('Error', 'ID not exists !')
                        return

                    cur.execute(query_update, (first_name, second_name, age, id))
                    messagebox.showinfo('Status', 'Selected visitor was succesfully updated !')
    except psycopg.DatabaseError as e:
        print(f'Error database: {e}')
    except Exception as e:
        print(f'Error: {e}')  
            
   
## Heading
general_label = customtkinter.CTkLabel(general_frame, text='Database of visitors', font=('Times New Roman', 25, 'bold'))
general_label.pack(pady=(5, 10))

## Input section
heading_visitors_label = customtkinter.CTkLabel(heading_input_frame, text="Visitor's registration", font=('Arial', 17, 'bold'))
heading_visitors_label.pack(pady=(0, 5))

first_name_label = customtkinter.CTkLabel(input_frame, text='First name: ')
first_name_label.grid(row=0, column=0)

first_name_entry = customtkinter.CTkEntry(input_frame, fg_color='black')
first_name_entry.grid(row=0, column=1, pady=(0, 3))

second_name_label = customtkinter.CTkLabel(input_frame, text='Second name: ')
second_name_label.grid(row=1, column=0)

second_name_entry = customtkinter.CTkEntry(input_frame, fg_color='black')
second_name_entry.grid(row=1, column=1, pady=(0, 3))

age_label = customtkinter.CTkLabel(input_frame, text='Age: ')
age_label.grid(row=2, column=0)

age_entry = customtkinter.CTkEntry(input_frame, fg_color='black')
age_entry.grid(row=2, column=1, pady=(0, 5))

button_register = customtkinter.CTkButton(input_frame, text='Register', width=30, command=lambda:insert_data(first_name_entry.get(), second_name_entry.get(), age_entry.get()))
button_register.grid(row=3, column=1)

## Operations section
operatins_heading_label = customtkinter.CTkLabel(heading_operations_frame, text='Operations', font=('Arial', 17, 'bold'))
operatins_heading_label.pack(pady=(5, 2))

id_label = customtkinter.CTkLabel(id_frame, text="Visitor's ID: ")
id_label.grid(row=0, column=0)

id_entry = customtkinter.CTkEntry(id_frame, fg_color='black')
id_entry.grid(row=0, column=1, pady=(0, 5))

# Button section
button_search = customtkinter.CTkButton(button_frame, text='Search', width=30, command=lambda:search(id_entry.get() if id_entry.get().strip() else None))
button_search.grid(row=0, column=0, padx=(0, 5))

button_delete = customtkinter.CTkButton(button_frame, text='Delete', width=30, command=lambda:delete(id_entry.get() if id_entry.get().strip() else None))
button_delete.grid(row=0, column=1, padx=(0, 5))

button_update = customtkinter.CTkButton(button_frame, text='Update', width=30, command=lambda:update(first_name_entry.get(), second_name_entry.get(), age_entry.get(), id_entry.get()))
button_update.grid(row=0, column=2, padx=(0, 5))

button_reload = customtkinter.CTkButton(button_frame, text='Show changes', width=30, command=lambda:display_all_visitors())
button_reload.grid(row=0, column=3)

# Content section
heading_content_label = customtkinter.CTkLabel(heading_content_frame, text='All visitors', font=('Arial', 17, 'bold'))
heading_content_label.pack(pady=(5, 2))








root.mainloop()