import math
import os
import re
import tkinter as tk
from const import *
from vertical import VerticalScrolledFrame
from tkinter import messagebox as mb
# from viewer import Viewer


class Result:
    def __init__(self, parent, find, catalog_path, count_on_page=10):
        self.parent = parent
        self.find = find
        self.catalog_path = catalog_path
        self.current_page = 1
        self.count_find = len(self.find)
        self.count_on_page = count_on_page
        self.buttons_result = []
        self.count_of_pages = math.ceil(self.count_find / self.count_on_page)
        self.root = tk.Toplevel(parent)
        self.root.resizable(True, True)
        self.root.title("Результаты поиска")
        self.root.geometry("400x700+200+100")
        self.root.iconbitmap("icon.ico")

        self.frame_result = tk.LabelFrame(master=self.root,
                                          text=f"Найдено {self.count_find}")
        self.frame_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.frame_navigation = tk.Frame(master=self.root)
        self.frame_navigation.pack(fill=tk.X,
                                   padx=5, pady=5)
        self.button_last = tk.Button(master=self.frame_navigation,
                                     text="  >|  ",
                                     command=self.button_last_click)
        self.button_last.pack(side="right", padx=5, pady=5)
        self.button_next = tk.Button(master=self.frame_navigation,
                                     text="  >  ",
                                     command=self.button_next_click)
        self.button_next.pack(side="right", padx=5, pady=5)

        self.label_page = tk.Label(master=self.frame_navigation,
                                   text=f"  {self.current_page}/{self.count_of_pages}  ")
        self.label_page.pack(side="right", padx=5, pady=5)

        self.button_prev = tk.Button(master=self.frame_navigation,
                                     text="  <  ",
                                     command=self.button_prev_click)
        self.button_prev.pack(side="right", padx=5, pady=5)
        self.button_first = tk.Button(master=self.frame_navigation,
                                      text="  |<  ",
                                      command=self.button_first_click)
        self.button_first.pack(side="right", padx=5, pady=5)
        self.draw_page()

        # self.root.grab_set()
        self.root.focus_set()
        # self.root.wait_window()

    def draw_page(self):
        print(self.find.head())
        print(self.count_of_pages)
        self.page = None
        self.page = self.find.iloc[(self.current_page-1)*self.count_on_page:
                                   self.current_page*self.count_on_page]
        print(self.page)
        self.frame_vertical = VerticalScrolledFrame(self.frame_result)
        self.frame_vertical.pack(fill=tk.BOTH, expand=True)
        self.buttons_result = []
        var = []
        for curr in range(self.count_on_page):
            try:
                var.append((self.current_page - 1) * self.count_on_page + curr)
                c = self.page.iloc[curr]
                self.buttons_result.append(tk.Button(master=self.frame_vertical.interior,
                                                     text=f"Район: {c[RAIONOBSHII]}, " +
                                                          f"{c[RAION]}\n" +
                                                          f"Шифр: {c[SHIFR]}" +
                                                          f"-{c[DOPSHIFR]}\n" +
                                                          f"Маршрут: {c[MARSHRUT]} \n" +
                                                          f"Тип: {c[TIP]}; " +
                                                          f"Категория похода: {c[KATEGORIYA]}\n" +
                                                          f"Год: {c[GOD]}; " +
                                                          f"Месяц: {month_to_string(c[MESYAC])}\n" +
                                                          f"Автор: {c[AVTOR]}",
                                                     wraplength=350,
                                                     justify="center",
                                                     relief=tk.RIDGE,
                                                     command=lambda vv=var, cc=curr:
                                                     self.button_select_click(vv[cc])))
                self.buttons_result[-1].pack(fill=tk.X, anchor="w", expand=True, padx=5, pady=5)
            except IndexError:
                pass

    def button_first_click(self):
        if self.current_page != 1:
            self.current_page = 1
            self.frame_vertical.pack_forget()
            self.frame_vertical.destroy()
            self.label_page.config(text=f"  {self.current_page}/{self.count_of_pages}  ")
            self.draw_page()

    def button_prev_click(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.frame_vertical.pack_forget()
            self.frame_vertical.destroy()
            self.label_page.config(text=f"  {self.current_page}/{self.count_of_pages}  ")
            self.draw_page()

    def button_next_click(self):
        if self.current_page < self.count_of_pages:
            self.current_page += 1
            self.frame_vertical.pack_forget()
            self.frame_vertical.destroy()
            self.label_page.config(text=f"  {self.current_page}/{self.count_of_pages}  ")
            self.draw_page()

    def button_last_click(self):
        if self.current_page != self.count_of_pages:
            self.current_page = self.count_of_pages
            self.frame_vertical.pack_forget()
            self.frame_vertical.destroy()
            self.label_page.config(text=f"  {self.current_page}/{self.count_of_pages}  ")
            self.draw_page()

    def button_select_click(self, event):
        # Viewer(self.parent, self.find.iloc[event], self.catalog_path)
        shifr = str(self.find.iloc[event][SHIFR]).rjust(5, '0')
        dopshifr = self.find.iloc[event][DOPSHIFR]
        dopshifr1 = ''
        dopshifr2 = ''
        if dopshifr != '':
            dopshifr1 = dopshifr + '-'
            dopshifr2 = '-' + dopshifr
        zip = '/'.join([item for item in self.catalog_path.split("/")[:-1]]) + '/'
        fold = zip
        folder = os.scandir(zip)
        for entry in folder:
            if entry.is_dir():
                r = re.findall(r"^([a-zA-Z0-9]+\-)?(\d+)\-(\d+)$", entry.name)
                if r:
                    print(f"{r[0][0]=} {dopshifr1=}")
                    fold = zip + r[0][0] + r[0][1] + '-' + r[0][2] + '/'
                    tmp = fold + shifr + dopshifr2 + '.zip'
                    if os.path.exists(tmp):
                        zip = tmp
                        break
        if os.path.exists(zip):
            os.startfile(zip)
        else:
            print(f"Файла '{zip}' не существует")
            mb.showerror(f"Файла '{zip}' не существует")
