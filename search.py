import json
import os
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
from result import Result
import pandas
from config import Config
import xlrd
from const import *


class Search:
    def __init__(self, conf):
        self.set_months = set_months
        self.set_months_patterns = set_months_patterns
        self.conf = conf
        self.config = None
        self.catalog = []
        self.catalog_path = None
        self.loaded = False
        self.load_path()
        self.root = tk.Tk()
        self.root.title("TLibViewer v0.9")
        self.root.geometry("550x365+300+200")
        self.root.iconbitmap("icon.ico")
        self.frame_search = tk.LabelFrame(master=self.root, text="Параметры поиска")
        self.frame_search.pack(anchor="center", expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.frame_bottom = tk.Frame(master=self.root)
        self.button_clear = tk.Button(master=self.frame_bottom,
                                      text="Очистить",
                                      command=self.button_clear_click)
        self.button_clear.pack(side="right")
        self.button_search = tk.Button(master=self.frame_bottom,
                                       text="Найти",
                                       command=self.button_search_click)
        self.button_search.pack(side="right", padx=10)
        self.frame_bottom.pack(side="bottom", fill=tk.X, padx=10, pady=10)

        self.frame_sort = tk.Frame(master=self.root)
        self.combo_asc = Combobox(master=self.frame_sort,
                                  values=["Возрастанию", "Убыванию"],
                                  state="readonly")
        self.combo_asc.current(0)
        self.asc = [True, False]
        self.combo_asc.pack(side="right", padx=2)

        self.label_sort_po = tk.Label(master=self.frame_sort, text="по")
        self.label_sort_po.pack(side="right", padx=2)

        self.combo_sort = Combobox(master=self.frame_sort,
                                   values=["Шифр", "Тип", "Категория", "Год"],
                                   state="readonly")
        self.combo_sort.current(0)
        self.sort_by = [SHIFR, TIP, KATEGORIYA, GOD]
        self.combo_sort.pack(side="right", padx=2)

        self.label_sort_pole = tk.Label(master=self.frame_sort, text="Сортировать по полю")
        self.label_sort_pole.pack(side="right", padx=2)

        self.values_combo_count_on_page = [5, 10, 25, 50]
        self.combo_count_on_page = Combobox(master=self.frame_sort,
                                            values=self.values_combo_count_on_page,
                                            state="readonly")
        self.combo_count_on_page.current(1)
        self.combo_count_on_page.pack(side="right", padx=2)

        self.frame_sort.pack(side="bottom", fill=tk.X, padx=10, pady=10)

        # self.root.state('zoomed')
        self.root.bind("<FocusIn>", self.handle_focus)

    def create_config(self):
        self.config = Config(self.root)

    def handle_focus(self, event):
        if event.widget == self.root:
            self.load_path()
            # print(self.catalog_path)
            if not self.loaded:
                self.loaded = True
                book = xlrd.open_workbook(self.catalog_path)
                sh = book.sheet_by_index(0)
                for rx in range(1, sh.nrows):
                    if len(sh.row(rx)) != 16:
                        mb.showerror(title="Ошибка",
                                     message="Количество столбцов не соответствует формату " +
                                             "файла каталога. При настройке Вам необходимо " +
                                             "выбрать путь к файлу '#Каталог tlib.ru.xls'. " +
                                             "Для выбора файла каталога перезапустите программу.")
                        os.remove(self.conf)
                        break
                    self.catalog.append([str(sh.row(rx)[SHIFR].value).split(".")[0],
                                         str(sh.row(rx)[DOPSHIFR].value),
                                         str(sh.row(rx)[RAIONOBSHII].value),
                                         str(sh.row(rx)[RAION].value),
                                         str(sh.row(rx)[AVTOR].value),
                                         str(sh.row(rx)[MARSHRUT].value),
                                         str(sh.row(rx)[GOD].value).split(".")[0],
                                         str(sh.row(rx)[MESYAC].value),
                                         str(sh.row(rx)[KATEGORIYA].value),
                                         str(sh.row(rx)[TIP].value),
                                         str(sh.row(rx)[TIPSYDNA].value),
                                         str(sh.row(rx)[GOROD].value),
                                         str(sh.row(rx)[KOMMENTARII].value),
                                         str(sh.row(rx)[SSYLKA].value),
                                         str(sh.row(rx)[KOLVOSTRANIC].value).split(".")[0],
                                         str(sh.row(rx)[RAZMERARHIVA].value).split(".")[0]])
                    # print(sh.row(rx)[RAIONOBSHII].value)
                    # print(sh.row(rx))

                self.df = pandas.DataFrame(data=self.catalog)

                self.set_raionobshii = sorted(self.df[RAIONOBSHII].unique())

                self.set_tip = sorted(self.df[TIP].unique())

                self.set_kategoriya = self.split_kategoriya(self.df[KATEGORIYA].unique())
                self.set_kategoriya.insert(0, "")
                self.set_kategoriya = list(set(self.set_kategoriya))
                self.set_kategoriya.sort()

                self.set_god = sorted(self.df[GOD].unique())

                self.create_search_widgets()

    def load_path(self):
        if not self.catalog_path:
            if os.path.exists(self.conf):
                f = open(self.conf, "r")
                c = json.load(f)
                self.catalog_path = c['catalog_path']

    def split_kategoriya(self, category):
        data = []
        for c in category:
            spl = c.split(",")
            for s in spl:
                data.append(s.strip())
        return data

    def button_search_click(self):
        self.find = self.df

        entrymarshrut = self.entry_marshrut.get().strip()
        if entrymarshrut != '':
            # print(entrymarshrut)
            self.find = self.find[self.find[MARSHRUT].str.contains(entrymarshrut, case=False)]

        entryshifr = self.entry_shifr.get().strip()
        if entryshifr != '':
            # print(entryshifr)
            self.find = self.find[self.find[SHIFR].str.contains(entryshifr, case=False)]

        entrydopshifr = self.entry_dopshifr.get().strip()
        if entrydopshifr != '':
            self.find = self.find[self.find[DOPSHIFR].str.contains(entrydopshifr, case=False)]

        raionobshii = self.set_raionobshii[self.combo_raion_obshii.current()]
        if raionobshii != '':
            print(raionobshii)
            self.find = self.find[self.find[RAIONOBSHII].str.contains(raionobshii, case=False)]

        entryraion = self.entry_raion.get().strip()
        if entryraion != '':
            self.find = self.find[self.find[RAION].str.contains(entryraion, case=False)]

        entryavtor = self.entry_avtor.get().strip()
        if entryavtor != '':
            self.find = self.find[self.find[AVTOR].str.contains(entryavtor, case=False)]

        tip = self.set_tip[self.combo_tip.current()]
        if tip != '':
            print(tip)
            self.find = self.find[self.find[TIP].str.contains(tip, case=False)]

        kategoriya_c = self.set_kategoriya[self.combo_kategoriya_c.current()]
        kategoriya_po = self.set_kategoriya[self.combo_kategoriya_po.current()]

        if kategoriya_c != "" or kategoriya_po != "":
            if kategoriya_c == "":
                kategoriya_c = self.set_kategoriya[1]
            if kategoriya_po == "":
                kategoriya_po = self.set_kategoriya[-1]
            kategoriya = ''
            fstart = False
            for c in self.set_kategoriya:
                if c == kategoriya_c:
                    fstart = True
                if fstart:
                    s = c[:].replace("/", "\\/").replace("*", "\\*").replace(".", "\\.")
                    kategoriya += f"{s}|"
                if c == kategoriya_po:
                    fstart = False
            kategoriya = kategoriya[:-1]
            # print(kategoriya)
            self.find = self.find[self.find[KATEGORIYA].str.contains(kategoriya,
                                                                     case=False,
                                                                     regex=True)]

        god_c = self.set_god[self.combo_god_c.current()]
        god_po = self.set_god[self.combo_god_po.current()]

        if god_c != "" or god_po != "":
            if god_c == "":
                god_c = self.set_god[1]
            if god_po == "":
                god_po = self.set_god[-1]
            god = ''
            fstart = False
            for c in self.set_god:
                if c == god_c:
                    fstart = True
                if fstart:
                    # s = c[:].replace("/", "\\/").replace("*", "\\*").replace(".", "\\.")
                    god += f"{c}|"
                if c == god_po:
                    fstart = False
            god = god[:-1]
            print(god)
            self.find = self.find[self.find[GOD].str.contains(god, case=False, regex=True)]

        mesyac_c = self.set_months[self.combo_mesyac_c.current()]
        mesyac_po = self.set_months[self.combo_mesyac_po.current()]

        if mesyac_c != "" or mesyac_po != "":
            if mesyac_c == "":
                mesyac_c = self.set_months[1]
            if mesyac_po == "":
                mesyac_po = self.set_months[-1]
            mesyac = ''
            fstart = False
            i = 0
            for c in self.set_months:
                if c == mesyac_c:
                    fstart = True
                if fstart:
                    mesyac += f"{self.set_months_patterns[i]}|"
                if c == mesyac_po:
                    fstart = False
                i += 1
            mesyac = mesyac[:-1]
            print(mesyac)
            self.find = self.find[self.find[MESYAC].str.contains(mesyac, case=False, regex=True)]

        self.find.sort_values(by=[self.sort_by[self.combo_sort.current()]],
                              inplace=True,
                              ascending=self.asc[self.combo_asc.current()])

        Result(self.root,
               self.find,
               self.catalog_path,
               self.values_combo_count_on_page[self.combo_count_on_page.current()])
        # print(self.find.head())
        # print(len(self.find))

    def button_clear_click(self):
        self.entry_marshrut.delete(0, tk.END)
        self.entry_shifr.delete(0, tk.END)
        self.entry_dopshifr.delete(0, tk.END)
        self.combo_raion_obshii.current(0)
        self.entry_raion.delete(0, tk.END)
        self.entry_avtor.delete(0, tk.END)
        self.combo_tip.current(0)
        self.combo_kategoriya_c.current(0)
        self.combo_kategoriya_po.current(0)
        self.combo_god_c.current(0)
        self.combo_god_po.current(0)
        self.combo_mesyac_c.current(0)
        self.combo_mesyac_po.current(0)

        self.combo_asc.current(0)
        self.combo_sort.current(0)

    def create_search_widgets(self):
        self.label_marshrut = tk.Label(master=self.frame_search, text="Маршрут")
        self.label_marshrut.grid(row=0, column=0, sticky=tk.W)
        self.entry_marshrut = tk.Entry(master=self.frame_search)
        self.frame_search.columnconfigure(1, weight=1)
        self.entry_marshrut.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=3)
        self.label_shifr = tk.Label(master=self.frame_search, text="Шифр-Доп. Шифр")
        self.label_shifr.grid(row=1, column=0)
        self.frame_shifr = tk.Frame(master=self.frame_search)
        self.frame_shifr.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=3)
        self.entry_shifr = tk.Entry(master=self.frame_shifr)
        self.entry_shifr.pack(fill=tk.X, side="left", expand=True)
        self.label_shifr_po = tk.Label(master=self.frame_shifr, text="-")
        self.label_shifr_po.pack(side="left")
        self.entry_dopshifr = tk.Entry(master=self.frame_shifr)
        self.entry_dopshifr.pack(fill=tk.X, side="left", expand=True)

        self.label_raion_obshii = tk.Label(master=self.frame_search, text="Район общий")
        self.label_raion_obshii.grid(row=2, column=0, sticky=tk.W, pady=3)
        self.combo_raion_obshii = Combobox(master=self.frame_search,
                                           values=self.set_raionobshii,
                                           state="readonly")
        self.combo_raion_obshii.current(0)
        self.combo_raion_obshii.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=3)

        self.label_raion = tk.Label(master=self.frame_search, text="Район")
        self.label_raion.grid(row=3, column=0, sticky=tk.W, pady=3)
        self.entry_raion = tk.Entry(master=self.frame_search)
        self.entry_raion.grid(row=3, column=1, sticky=tk.NSEW, padx=5, pady=3)

        self.label_avtor = tk.Label(master=self.frame_search, text="Автор")
        self.label_avtor.grid(row=4, column=0, sticky=tk.W, pady=3)
        self.entry_avtor = tk.Entry(master=self.frame_search)
        self.entry_avtor.grid(row=4, column=1, sticky=tk.NSEW, padx=5, pady=3)

        self.label_tip = tk.Label(master=self.frame_search, text="Тип")
        self.label_tip.grid(row=5, column=0, sticky=tk.W, pady=3)
        self.combo_tip = Combobox(master=self.frame_search,
                                  values=self.set_tip,
                                  state="readonly")
        self.combo_tip.current(0)
        self.combo_tip.grid(row=5, column=1, sticky=tk.NSEW, padx=5, pady=3)

        self.label_kategoriya = tk.Label(master=self.frame_search, text="Категория похода")
        self.label_kategoriya.grid(row=6, column=0, sticky=tk.W, pady=3)
        self.frame_kategoriya = tk.Frame(master=self.frame_search)
        self.frame_kategoriya.grid(row=6, column=1, sticky=tk.NSEW, padx=5, pady=3)
        self.label_kategoriya_c = tk.Label(master=self.frame_kategoriya, text="с")
        self.label_kategoriya_c.pack(side="left")
        self.combo_kategoriya_c = Combobox(master=self.frame_kategoriya,
                                           values=self.set_kategoriya,
                                           state="readonly")
        self.combo_kategoriya_c.current(0)
        self.combo_kategoriya_c.pack(fill=tk.X, side="left", expand=True)
        self.label_kategoriya_po = tk.Label(master=self.frame_kategoriya, text="по")
        self.label_kategoriya_po.pack(side="left")
        self.combo_kategoriya_po = Combobox(master=self.frame_kategoriya,
                                            values=self.set_kategoriya,
                                            state="readonly")
        self.combo_kategoriya_po.current(0)
        self.combo_kategoriya_po.pack(fill=tk.X, side="left", expand=True)

        self.label_god = tk.Label(master=self.frame_search, text="Год")
        self.label_god.grid(row=7, column=0, sticky=tk.W, pady=3)
        self.frame_god = tk.Frame(master=self.frame_search)
        self.frame_god.grid(row=7, column=1, sticky=tk.NSEW, padx=5, pady=3)
        self.label_god_c = tk.Label(master=self.frame_god, text="с")
        self.label_god_c.pack(side="left")
        self.combo_god_c = Combobox(master=self.frame_god,
                                    values=self.set_god,
                                    state="readonly")
        self.combo_god_c.current(0)
        self.combo_god_c.pack(fill=tk.X, side="left", expand=True)
        self.label_god_po = tk.Label(master=self.frame_god, text="по")
        self.label_god_po.pack(side="left")
        self.combo_god_po = Combobox(master=self.frame_god,
                                     values=self.set_god,
                                     state="readonly")
        self.combo_god_po.current(0)
        self.combo_god_po.pack(fill=tk.X, side="left", expand=True)

        self.label_mesyac = tk.Label(master=self.frame_search, text="Месяц")
        self.label_mesyac.grid(row=8, column=0, sticky=tk.W, pady=3)
        self.frame_mesyac = tk.Frame(master=self.frame_search)
        self.frame_mesyac.grid(row=8, column=1, sticky=tk.NSEW, padx=5, pady=3)
        self.label_mesyac_c = tk.Label(master=self.frame_mesyac, text="с")
        self.label_mesyac_c.pack(side="left")
        self.combo_mesyac_c = Combobox(master=self.frame_mesyac,
                                       values=self.set_months,
                                       state="readonly",
                                       height=13)
        self.combo_mesyac_c.current(0)
        self.combo_mesyac_c.pack(fill=tk.X, side="left", expand=True)
        self.label_mesyac_po = tk.Label(master=self.frame_mesyac, text="по")
        self.label_mesyac_po.pack(side="left")
        self.combo_mesyac_po = Combobox(master=self.frame_mesyac,
                                        values=self.set_months,
                                        state="readonly",
                                        height=13)
        self.combo_mesyac_po.current(0)
        self.combo_mesyac_po.pack(fill=tk.X, side="left", expand=True)
