from tkinter import *
import psycopg

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

filter_frame = Frame(root)
filter_frame.pack()

button_frame = Frame(root)
button_frame.pack()

content_frame = Frame(root)
content_frame.pack()

## Heading
general_label = Label(general_frame, text='Database of visitors', font=('Times New Roman', 15, 'bold'))
general_label.pack()






root.mainloop()