import socket
import customtkinter
import customtkinter as c
import time
from threading import Thread
import tkinter as tk


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")



def get_value():
    HEADERSIZE = 6
    full_msg = ''
    new_msg = True
    state = False
    while not state:
        msg = clientsocket.recv(4)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADERSIZE == msglen:
            state = True
            print(full_msg[HEADERSIZE-1])
            return full_msg[HEADERSIZE-1:]


    # msg = clientsocket.recv(1024) 
    # msg = str(msg.decode())
    # return msg


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("350x550")
        self.title("Gym Buddy")

        self.my_frame = MyFrame(master=self, fg_color = "#333333")
        self.my_frame.grid(row=0, column=0, padx=34, pady=70, sticky="nsew")

        title = c.CTkFont(size=20)
        self.label1 = c.CTkLabel(master=self.my_frame, text='Welcome To Gym Buddy!', font=title)
        self.label1.grid(row=0,column=0,padx=(30,30), pady=(100, 0))

        self.button = c.CTkButton(master=self.my_frame, text="Start", width = 120, height = 60, corner_radius = 10, command = self.button_event)
        self.button.grid(row=1,column=0, padx=75, pady=(110,30))


    def button_event(self):
        self.my_frame.grid_forget()
        self.label1.grid_forget()
        self.button.grid_forget()
        self.my_frame = MyFrame(master=self, fg_color = "#333333")
        self.my_frame.grid(row=0, column=0, padx=40, pady=70, sticky="nsew")
        title = c.CTkFont(size=20)
        self.label1 = c.CTkLabel(master=self.my_frame, text="Let's begin our pushups", font=title)
        self.label1.grid(row=0,column=0, padx=(30,30), pady=(20, 0))
        number_font = c.CTkFont(size=35)
        self.count = tk.StringVar(value = "0")
        self.number = c.CTkLabel(master=self.my_frame, textvariable=self.count, font=number_font)
        self.number.grid(row=1,column=0,padx=(30,30), pady=(50,30))
        self.get_count()
    pass

    def get_count(self):
        height = get_value()
        print(height)
        if 0 < float(height) < 23:
            count = self.count.get()
            self.count.set(str(int(count)+1))
        self.after(100, self.get_count)
        
        
        



if __name__ == "__main__":
    print("Starting Server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(1000)
    global clientsocket
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    app = App()
    app.after(100, app.button_event)
    app.mainloop()
    