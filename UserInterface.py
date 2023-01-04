import tkinter as tk
from Linked_List import Linked_List
import math


class UserInterface:
    def __init__(self):
        self.josephus_master = tk.Tk()
        self.josephus_master.title("Josephus")
        self.josephus_master.geometry("600x200")
        self.josephus_master.config(bg="#808B96")
        self.number_entry = tk.Entry()
        self.linked_list = Linked_List()
        self.stack = []
        self.k = tk.Entry()
        self.main_screen()
        self.victims_master = None

    def main_screen(self):
        tk.Label(self.josephus_master, text="Please enter rational numbers !", bg="#808B96", foreground="white", font="Fixedsys").pack(side="top", pady=10)
        tk.Label(self.josephus_master, text="N: ", bg="#808B96", foreground="white", font="Fixedsys").pack(side="left")
        self.number_entry = tk.Entry(self.josephus_master)
        self.number_entry.pack(side="left", padx=20)
        self.k = tk.Entry(self.josephus_master)
        self.k.pack(side="right", padx= 20)
        tk.Label(self.josephus_master, text="K: ", bg="#808B96", foreground="white", font="Fixedsys").pack(side="right")
        tk.Button(self.josephus_master, text="Display", command=self.display, width=15, height=2, bg="white", foreground="black").pack(side="bottom")
        self.josephus_master.mainloop()

    def is_entry_valid(self, n, k):
        try:
            n = int(n)
            k = int(k)
        except:
            return "It should be a number"
        if n > 1000 or n < 1:
            return "N should be a number between 1 and 1000"
        elif k > 1000 or k < 0:
            return "K should be a number between 0 and 1000"
        else:
            return "Yes"

    def display(self):
        if self.is_entry_valid(self.number_entry.get(), self.k.get()) == "Yes":
            self.number_entry = int(self.number_entry.get())
            self.k = int(self.k.get())
            self.victims_master = tk.Tk()
            self.victims_master.title("Victims")
            self.victims_master.geometry("400x400+50+0")
            self.josephus_master.geometry("600x400+500+0")
            self.victims_master.config(bg="#808B96")
            self.linked_list.create(int(self.number_entry))
            self.josephus_master.bind("<space>", self.next)
            self.josephus_master.bind("<s>", self.back_to_main_screen)
            self.display_left_behinds()
        else:
            def Ok():
                error_master.destroy()
            error_master = tk.Tk()
            error_master.geometry("+"+str(int(self.josephus_master.winfo_x() + self.josephus_master.winfo_width()/2))+"+"+str(int(self.josephus_master.winfo_y() + self.josephus_master.winfo_height()/2)))
            error_master.title("Alert")
            tk.Button(error_master, text="Ok", command=Ok).grid(row=2, column=1)
            tk.Label(error_master, text=self.is_entry_valid(self.number_entry.get(), self.k.get())).grid(row=1, column=1)

    def display_victims(self):
        self.clear_victims_master()
        canvas = tk.Canvas(self.victims_master, bg="#808B96", scrollregion=(0, 0, 0, len(self.stack) * 25 + 10))
        canvas.pack(expand=True, side="right", fill=tk.BOTH)
        scroll_bar_y = tk.Scrollbar(self.victims_master, orient=tk.VERTICAL)
        scroll_bar_y.pack(side="left", fill=tk.Y)
        scroll_bar_y.config(command=canvas.yview)
        canvas.config(yscrollcommand=scroll_bar_y.set)
        canvas.yview_moveto((len(self.stack))*20)
        for i in range(1, len(self.stack) + 1):
            canvas.create_oval(10, 25 * i - 10, 30, 25 * i + 10, fill="white")
            canvas.create_text(20, 25*i, text=str(self.stack[i-1].pre.value), fill="black")
            canvas.create_text(40, 25*i, text="-->", fill="black")
            canvas.create_oval(50, 25 * i - 10, 70, 25*i+10, fill="red")
            canvas.create_text(60, 25*i, text=str(self.stack[i-1].value), fill="black")

    def clear_victims_master(self):
        for child in self.victims_master.winfo_children():
            child.destroy()

    def next(self, key):
        if len(self.linked_list) <= 1:
            self.end()
            return
        current = self.linked_list.get_head()
        pre_target = self.linked_list[int(self.k) - 1]
        pre_target.next.pre = current
        self.stack.append(pre_target.next)
        pre_target.next = pre_target.next.next
        current = pre_target.next
        self.linked_list = Linked_List(current)
        self.display_left_behinds()
        self.display_victims()

    def end(self):
        self.clear_josephus_master()
        canvas = tk.Canvas(self.josephus_master, bg="#808B96")
        canvas.pack(expand=True, fill=tk.BOTH)
        canvas.create_text(self.josephus_master.winfo_width() / 2, self.josephus_master.winfo_height() / 2 - 100, text="Winning position is :", fill="white", font="Fixedsys")
        canvas.create_oval(self.josephus_master.winfo_width() / 2 - 20, self.josephus_master.winfo_height() / 2 - 20, self.josephus_master.winfo_width() / 2 + 20, self.josephus_master.winfo_height() / 2 + 20, fill="blue")
        canvas.create_text(self.josephus_master.winfo_width() / 2, self.josephus_master.winfo_height() / 2, fill="black", text=self.linked_list.get_head().value)
        canvas.create_text(self.josephus_master.winfo_width() / 2, self.josephus_master.winfo_height() / 2 + 100, fill="white", text="press 's' to back to main screen", font="Fixedsys")

    def back_to_main_screen(self, key):
        self.clear_josephus_master()
        self.stack.clear()
        self.victims_master.destroy()
        self.main_screen()

    def display_left_behinds(self):
        self.clear_josephus_master()
        degree = 360 / len(self.linked_list)
        r = 20 / math.sin(math.radians(degree)) if degree != 180 else 50
        MAX_HEIGHT = MAX_WIDTH = 2 * r + 200
        canvas = tk.Canvas(self.josephus_master, bg="#808B96", scrollregion=(0, 0, MAX_WIDTH, MAX_HEIGHT))
        scroll_bar_x = tk.Scrollbar(self.josephus_master, orient=tk.HORIZONTAL)
        scroll_bar_x.pack(side="bottom", fill=tk.X)
        scroll_bar_x.config(command=canvas.xview)
        scroll_bar_x.set(0, int(MAX_WIDTH))
        scroll_bar_y = tk.Scrollbar(self.josephus_master, orient=tk.VERTICAL)
        scroll_bar_y.pack(side="left", fill=tk.Y)
        scroll_bar_y.config(command=canvas.yview)
        scroll_bar_y.set(0, int(MAX_HEIGHT))
        canvas.pack(expand=True, fill=tk.BOTH)
        canvas.config(xscrollcommand=scroll_bar_x.set)
        canvas.config(yscrollcommand=scroll_bar_y.set)
        for i in range(1, len(self.linked_list) + 1):
            canvas.create_oval(MAX_WIDTH / 2 + math.cos(math.radians(degree * i)) * r - 10,
                               MAX_HEIGHT / 2 + math.sin(math.radians(degree * i)) * r - 10,
                               MAX_WIDTH / 2 + math.cos(math.radians(degree * i)) * r + 10,
                               MAX_HEIGHT / 2 + math.sin(math.radians(degree * i)) * r + 10, fill="white")
            canvas.create_text(MAX_WIDTH / 2 + math.cos(math.radians(degree * i)) * r,
                               MAX_HEIGHT / 2 + math.sin(math.radians(degree * i)) * r, text=self.linked_list[i].value,
                               fill="black")

    def clear_josephus_master(self):
        for child in self.josephus_master.winfo_children():
            child.destroy()



