from customtkinter import*
from socket import socket, AF_INET,SOCK_STREAM
import threading


class RegisteWindow(CTk):
    def __init__(self):
        super().__init__()
        self.username = None
        self.title('Приєднатися до сервера')
        self.geometry("300x300")

        self.label = CTkLabel(self,text='Вхід в LogiTalk',font=('Arial',20,'bold'))
        self.label.pack(pady=40)

        self.name_entry = CTkEntry(self, placeholder_text="Введіть ім'я")
        self.name_entry.pack()

        self.host_entry = CTkEntry(self, placeholder_text="Введіть хост")
        self.host_entry.pack()

        self.port_entry = CTkEntry(self, placeholder_text="Введіть порт")
        self.port_entry.pack()

        self.join_bnt = CTkButton(self,text='Приєднатися',command=self.start_chat)
        self.join_bnt.pack(pady=5)

    def start_chat(self):
        self.username = self.name_entry.get()
        try:
            self.sock = socket(AF_INET,SOCK_STREAM)
            self.sock.connect((self.host_entry.get(),int(self.port_entry.get())))
            hello = f"{self.username} приєднався до чату\n"
            self.sock.send(hello.encode())
            self.destroy()
            win = MyWin(self.sock,self.username)
            win.mainloop()
        except:
            print("Не вдалося підклучитися до сервера!!!")





color_frame = 'lightblue'
class MyWin(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title('Logitalk')
        self.frame = CTkFrame(self,fg_color=color_frame,width=200,height=self.winfo_height())
        self.frame.pack_propagate(False)
        self.frame.configure(width=0)
        self.frame.place(x=0,y=0)

        self.is_show_menu = False
        self.frame_width = 0

        self.bnt = CTkButton(self,text='Menu',command=self.toggle_show_menu,width=30)
        self.bnt.place(x=0,y=0)

        self.chat_text = CTkTextbox(self,state='disabled')
        self.chat_text.place(x=0,y=30)

        self.message_input = CTkEntry(self,placeholder_text='Введіть повідомленя')
        self.message_input.place(x=0,y=250)

        self.label_tema = CTkOptionMenu(self.frame,values=['Темна','Світла'],command=self.change_theme)
        self.label_tema.pack(side='bottom',pady=20)
        self.theme = None

        self.send_btn = CTkButton(self,text='▶️', width=30,command=self.send_mesange)
        self.send_btn.place(x=200,y=250)

        self.adaptive_ui()

        self.label_name = CTkLabel(self.frame, text="ім'я")
        self.label_name.pack(pady=30)

        self.entry = CTkEntry(self.frame,placeholder_text='Ваш нік')
        self.entry.pack()

        self.save_btn = CTkButton(self.frame,text='зберегзи',command=self.change_name)
        self.save_btn.pack()
        
        name = None

    def change_name(self):
        new_name = self.entry.get()
        if new_name:
            self.username = new_name
            self.add_mesange(f"Ваш новий нік: {self.username}")

    def adaptive_ui(self):
        self.chat_text.configure(width=self.winfo_width()-self.frame.winfo_width(),height=self.winfo_height()-self.message_input.winfo_height()-30)
        self.chat_text.place(x=self.frame.winfo_width())
        self.message_input.configure(width=self.winfo_width()-self.frame.winfo_width()-self.send_btn.winfo_width())
        self.message_input.place(x=self.frame.winfo_width(),y=self.winfo_height()-self.send_btn.winfo_height())
        self.send_btn.place(x=self.winfo_width()-self.send_btn.winfo_width(),y=self.winfo_height()-self.send_btn.winfo_height())
        self.after(20,self.adaptive_ui)
    
    def change_theme(self,value):
        if value == 'Темна':
            set_appearance_mode('dark')
        else:
            set_appearance_mode('light')

    def add_mesange(self,text):
        self.chat_text.configure(state='normal')
        self.chat_text.insert(END,text+'\n')
        self.chat_text.configure(state='disable')
    
    def send_mesange(self):
        mesange = self.message_input.get()
        if mesange:
            self.add_mesange(f'{self.username}:{mesange}')
            data = f'TEXT@{mesange}\n'
            try:
                pass
            except:
                pass
        self.message_input.delete(0,END)

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.close_menu()
        else:
            self.is_show_menu = True
            self.show_menu()

    def show_menu(self):
        if self.frame_width <= 200:
            self.frame_width += 5
            self.frame.configure(width=self.frame_width,height=self.winfo_height())
            if self.frame_width >= 30:
                self.bnt.configure(width=self.frame_width)
        if self.is_show_menu:
            self.after(10,self.show_menu)
    
    def close_menu(self):
        if self.frame_width >= 0:
            self.frame_width -= 5
            self.frame.configure(width=self.frame_width,height=self.winfo_height())
            if self.frame_width >= 30:
                self.bnt.configure(width=self.frame_width)
        if not self.is_show_menu:
            self.after(10,self.close_menu)


if __name__ ==  "__main__":
    RegisteWindow().mainloop()

win = MyWin()
win.mainloop()
