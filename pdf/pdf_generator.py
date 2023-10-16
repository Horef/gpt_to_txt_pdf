from fpdf import FPDF
from reportlab.lib.pagesizes import A4
import textwrap

import tkinter as tk
from tkinter import font as TkFont 

import math
import time

import configparser

class PdfGenerator():
    """
    A class to manage the pdf generation.
    """
    def __init__(self):
        # Importing the settings.
        self.config = configparser.ConfigParser()
        self.config.read("settings/config.ini")

        settings = self.config["PDF Generator Settings"]

        pd_name = settings.get('pdf_name')
        if pd_name == 'random':
            pd_name = str(time.time())
        self.pdf_name = settings.get('pdf_folder') + '/' + pd_name + '.pdf'

        
        self.width, self.height = A4
        self.fontsize_pt = settings.getint('font_size')
        
        # Calculate the width of a character in points.
        root = tk.Tk()        
        font = TkFont.Font(family="Arial", size=self.fontsize_pt)
        char_length = font.measure("a")
        dpi = settings.getint('dpi')
        self.char_length_pt = char_length * 72 / dpi
        root.destroy()

        # Calculate the number of characters that fit in a line.
        self.width_chars = math.ceil(self.width / self.char_length_pt)
        margin_bottom_pt = 10

        # Create the pdf object.
        self.pdf = FPDF(orientation='P', unit="pt", format=A4)
        self.pdf.set_auto_page_break(auto=True, margin=margin_bottom_pt)
        self.pdf.add_page()
        self.pdf.set_font(family="Arial", size=self.fontsize_pt)

        # Handling the txt file.
        tx_name = settings.get('txt_name')
        if tx_name == 'random':
            tx_name = str(time.time())
        self.txt_name = settings.get('txt_folder') + '/' + tx_name + '.txt'
        self.txt_file = open(self.txt_name, "w")

    def add_text(self, text: str):
        self.txt_file.write(text)

    def save_pdf(self):
        self.txt_file.close()
        with open(self.txt_name, "r") as file:
            for line in file:
                wrapped_lines = textwrap.wrap(line, width=self.width_chars)

                if len(wrapped_lines) == 0:
                    self.pdf.ln()

                for wrap in wrapped_lines:
                    self.pdf.cell(w=0, h=self.fontsize_pt, txt=wrap, ln=1)
        
        self.pdf.output(self.pdf_name)