from tkinter import *
import psycopg
from tkinter import messagebox

root = Tk()
root.geometry('500x400+200+100')
root.title('Visitors')
root.resizable(False, False)

# FRAMES
general_frame = Frame(root)
general_frame.pack()

heading_input_frame = Frame(root)
heading_input_frame.pack()

input_frame = Frame(root)
input_frame.pack()

heading_operations_frame = Frame(root)
heading_operations_frame.pack() 

button_frame = Frame(root)
button_frame.pack()

content_frame = Frame(root)
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
     
## Heading
general_label = Label(general_frame, text='Database of visitors', font=('Times New Roman', 17, 'bold'))
general_label.pack()

## Input section
heading_visitors_label = Label(heading_input_frame, text="Visitor's registration", font=('Arial', 12, 'bold'))
heading_visitors_label.pack()

first_name_label = Label(input_frame, text='First name: ')
first_name_label.grid(row=0, column=0)

first_name_entry = Entry(input_frame)
first_name_entry.grid(row=0, column=1)

second_name_label = Label(input_frame, text='Second name: ')
second_name_label.grid(row=1, column=0)

second_name_entry = Entry(input_frame)
second_name_entry.grid(row=1, column=1)

age_label = Label(input_frame, text='Age: ')
age_label.grid(row=2, column=0)

age_entry = Entry(input_frame)
age_entry.grid(row=2, column=1)

button_register = Button(input_frame, text='Register', command=lambda:insert_data(first_name_entry.get(), second_name_entry.get(), age_entry.get()))
button_register.grid(row=3, column=1)






root.mainloop()