import json
import os
import tkinter as tk
from tkinter import filedialog as fd


class Config:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.resizable(False, False)
        self.root.title("Настройка")
        self.root.geometry("300x200+100+100")
        self.root.iconbitmap("icon.ico")
        self.label_info = tk.Label(master=self.root,
                                   pady=20,
                                   text="Введите путь к файлу каталога.\n " +
                                        "Обычно это называется '#Каталог tlib.ru.xls'")
        self.entry_file = tk.Entry(master=self.root,
                                   bg="lightgray")
        self.button_file = tk.Button(master=self.root,
                                     text="Выбрать файл...",
                                     command=self.button_file_choose)
        self.button_save = tk.Button(master=self.root,
                                     text="Сохранить",
                                     command=self.button_file_save)
        self.draw_widgets()
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

    def draw_widgets(self):
        self.label_info.pack(fill=tk.X, anchor=tk.N, padx=20)
        self.entry_file.pack(fill=tk.X, anchor=tk.N, padx=20)
        self.button_file.pack(fill=tk.X, anchor=tk.N, pady=20, padx=20)
        self.button_save.pack(fill=tk.X, anchor=tk.N, padx=20)
        # self.input_xls = tk.Input(master=self.root)
        # self.input_xls.pack(fill=tk.X, side="right", padx=5)

    def button_file_choose(self):
        file_name = fd.askopenfilename(filetypes=[("Excel files", "*.xls")])
        if file_name:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file_name)

    def button_file_save(self):
        file_name = self.entry_file.get()
        if os.path.exists(file_name) and file_name[-4:] == ".xls":
            json_string = {'catalog_path': f'{file_name}'}
            with open("config.json", "w") as f:
                json.dump(json_string, f)
            self.root.destroy()
            self.root.update()
