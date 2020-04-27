import tkinter

class DelayServerGui(tkinter.Frame):
   def __init__(self, master=None):
      tkinter.Frame.__init__(self, master)
      self.master = master
      self.init_window()
      
   def init_window(self):
      self.master.title("DelayServer")
      self.pack(fill=tkinter.BOTH, expand=1)
      menu = tkinter.Menu(self.master)
      self.master.config(menu=menu)
      file = tkinter.Menu(menu)
      file.add_command(label="Exit", command=self.client_exit)
      menu.add_cascade(label="File", menu=file)
      
   def client_exit(self):
      exit()
   
root = tkinter.Tk()
root.geometry("400x300")
app = DelayServerGui(root)
root.mainloop()