import tkinter as tk
from tkdocviewer import *


class Viewer:
    def __init__(self, parent, view, catalog_path):
        self.view = view
        self.catalog_path = catalog_path
        self.root = tk.Toplevel(parent)
        self.root.resizable(True, True)
        self.root.title("Просмотр архива ")
        self.root.geometry("600x600+100+70")
        self.root.iconbitmap("icon.ico")
        print(self.view)

        self.frame_left = tk.Frame(master=self.root)
        self.frame_left.pack(fill=tk.Y, side="left", expand=False, padx=5, pady=5)

        self.frame_right = tk.Frame(master=self.root)
        self.frame_right.pack(fill=tk.BOTH, side="left", expand=True, padx=5, pady=5)

        self.doc_viewer = DocViewer(self.frame_right)
        self.doc_viewer.pack(fill="both", expand=True)
        self.doc_viewer.display_file("1а-063.tif")

        self.draw_widgets()
        self.root.focus_set()

    def draw_widgets(self):
        pass
