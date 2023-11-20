import re
import glob
import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PyPDF2 import PdfReader

class PdfExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.extracted_text = None

    def extract_text_from_pdf(self, pdf_file):
        try:
            reader = PdfReader(pdf_file)
            self.extracted_text = ""

            for page in reader.pages:
                self.extracted_text += page.extract_text()

            return  self.extracted_text
        except Exception as e:
            print(f"Hata oluştu: {e}")

    def get_extracted_text(self):
        extracted_text = self.extracted_text
        icra_dairesi_match = re.search('(.+) İcra Dairesi', extracted_text)
        self.icra_dairesi = icra_dairesi_match.group(1) if icra_dairesi_match else None

        icra_dosyasi_match = re.search('(.+) İcra Dosyası', extracted_text)
        self.icra_dosyasi = icra_dosyasi_match.group(1) if icra_dosyasi_match else None

        borclu_tckn = re.search(r'Borçlu\s*:\s*([^\/]+)\s*\/\s*(\d{11})', extracted_text)
        self.borclu = borclu_tckn.group(1) if borclu_tckn else None
        self.tckn = borclu_tckn.group(2) if borclu_tckn else None
        self.birlikte = borclu_tckn if borclu_tckn else None

        alacak_match = re.findall(r'([\d.,]+) TL', extracted_text)
        self.alacak = alacak_match[0] if alacak_match else None

        feragat_match = re.findall(r'([\d.,]+) TL', extracted_text)
        self.feragat = feragat_match[1] if len(feragat_match) >= 2 else None

        url_match = re.search(r'https://evrakdogrula\.uyap\.gov\.tr/[a-zA-Z0-9]+', extracted_text)
        self.url = url_match.group() if url_match else None

class ConverterFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.output_folder_path = None
        self.output_txt_file = None

        self.input_button = ttk.Button(self, text='Input Folder', command=self.call_folder)
        self.input_button.grid(column=0, row=0, **options)

        self.output_button = ttk.Button(self, text='Output Folder', command=self.call_output_folder)
        self.output_button.grid(column=1, row=0, **options)

        self.output_txt_button = ttk.Button(self, text= 'Output Txt', command= self.call_output_txt)
        self.output_txt_button.grid(column= 0, row= 1, **options)

    def call_folder(self):
        folder_path = fd.askdirectory()
        self.process_folder(folder_path)

    def call_output_folder(self):
        self.output_folder_path = fd.askdirectory()
        self.process_folder(self.output_folder_path)

    def call_output_txt(self):
        output_txt_file = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if not output_txt_file:
            # Eğer kullanıcı dosya seçimini iptal ederse, işlemi sonlandır
            return

        self.output_txt_file = output_txt_file
        self.process_folder(self.output_txt_file)

    def process_folder(self, folder_path):

        """if self.output_txt is None:
            print("Lütfen önce Output Txt dosyası seçin.")
            return"""
        if self.output_folder_path is None:
            print("Lütfen önce Output Folder'ı seçin.")
            return

        pdf_extractor = PdfExtractor(folder_path)

        for pdf_file in glob.glob(os.path.join(folder_path, "*.pdf")):
            pdf_extractor.extract_text_from_pdf(pdf_file)
            pdf_extractor.get_extracted_text()

            if pdf_extractor.borclu is None or pdf_extractor.feragat is None or len(pdf_extractor.alacak) < 2:
                destination_path = os.path.join(self.output_folder_path, os.path.basename(pdf_file))
                print(f"Moving file {pdf_file} to {self.output_folder_path}")
                shutil.move(pdf_file, destination_path)
                continue

            print(f"File: {pdf_file}")
            print("İcra Dairesi:", pdf_extractor.icra_dairesi)
            print("İcra Dosyası:", pdf_extractor.icra_dosyasi)
            #print("Birlikte", pdf_extractor.birlikte)
            print("Borçlu:", pdf_extractor.borclu)
            print("TCKN:", pdf_extractor.tckn)
            print("Asıl Alacak:", pdf_extractor.alacak)
            print("Feragat Edilen Tutar:", pdf_extractor.feragat)
            print("URL:", pdf_extractor.url)
            print("********************************")
            print("\n")

            if self.output_txt_file is None or not hasattr(self.output_txt_file, 'write'):
                # Dosya nesnesi yoksa veya yazma özelliği yoksa, dosyayı açın
                self.output_txt_file = open(self.output_txt_file, 'w', encoding='utf-8')

            #output_txt = open(self.output_txt, 'w')
            self.output_txt_file.write(f"File: {pdf_file} \n")
            self.output_txt_file.write(f"{pdf_extractor.icra_dairesi} İcra Dairesi \n")
            self.output_txt_file.write(f"{pdf_extractor.icra_dosyasi} \n")
            self.output_txt_file.write(f"Borçlu: {pdf_extractor.borclu} \n")
            #self.output_txt_file.write(f"Borçlu: {pdf_extractor.borclu} \n")
            self.output_txt_file.write(f"TCKN: {pdf_extractor.tckn} \n")
            self.output_txt_file.write(f"Asıl Alacak: {pdf_extractor.alacak} \n")
            self.output_txt_file.write(f"Feragat: {pdf_extractor.feragat} \n")
            self.output_txt_file.write(f"URL: {pdf_extractor.url} \n")



root = tk.Tk()
root.geometry('200x200')
app = ConverterFrame(root)
app.grid(row=0, column=0, padx=10, pady=10)
root.mainloop()
