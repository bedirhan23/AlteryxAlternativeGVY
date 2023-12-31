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
            extracted_text = ""  #self ekle yarın

            for page in reader.pages:
                extracted_text += page.extract_text()

            return  extracted_text
            #return extracted_text
        except Exception as e:
            print(f"Hata oluştu: {e}")

    def get_extracted_text(self):
        extracted_text = self.extracted_text
        icra_dairesi_match = re.search('(.+) İcra Dairesi', extracted_text)
        self.icra_dairesi = icra_dairesi_match.group(1) if icra_dairesi_match else None

        icra_dosyasi_match = re.search('(.+) İcra Dosyası', extracted_text)
        self.icra_dosyasi = icra_dosyasi_match.group(1) if icra_dosyasi_match else None

        borclu_tckn = re.search(r'Borçlu\s*:\s*(.*)\s*/\s*(\d+)', extracted_text)
        self.borclu = borclu_tckn.group(1) if borclu_tckn else None
        self.tckn = borclu_tckn.group(2) if borclu_tckn else None

        alacak_match = re.findall(r'([\d.,]+) TL', extracted_text)
        self.alacak = alacak_match[0] if alacak_match else None
        print(len(alacak_match))

        feragat_match = re.findall(r'([\d.,]+) TL', extracted_text)
        self.feragat = feragat_match[1] if len(feragat_match) >= 2 else None

        url_match = re.search(r'https://evrakdogrula\.uyap\.gov\.tr/[a-zA-Z0-9]+', extracted_text)
        self.url = url_match.group() if url_match else None

class ConverterFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.output_folder_path = None
        """self.input_label = ttk.Label(self, text= 'Klasor yolunu giriniz')
        self.input_label.grid(column=0, row=0, sticky= tk.W, **options)"""

        self.input_button = ttk.Button(self, text='Input Folder', command= self.call_folder)
        self.input_button.grid(column = 0, row=0, **options)

        self.output_button= ttk.Button(self, text='Output Folder', command= self.call_output_folder)
        self.output_button.grid(column =1, row=0, **options)

        self.process_button = ttk.Button(self, text='Process', command= self.process_folder(self.output_folder_path))
        self.process_button.grid(column=1, row=1, **options)

    def call_folder(self):
        folder_path= fd.askdirectory()
        self.process_folder(folder_path)
        print(f'This is input folder {folder_path}')

    def call_output_folder(self):
        self.output_folder_path= fd.askdirectory()
        self.process_folder(self.output_folder_path)
        print(f'This is output folder {self.output_folder_path}')


    def process_folder(self, folder_path):
        if self.output_folder_path is None:
            print("Lütfen önce Output Folder'ı seçin.")
            return

        pdf_extractor = PdfExtractor(folder_path)

        for pdf_file in glob.glob(os.path.join(folder_path, "*.pdf")):

            pdf_extractor.extract_text_from_pdf(pdf_file)
            pdf_extractor.get_extracted_text()

            if pdf_extractor.feragat is None or len(pdf_extractor.alacak) < 2:
                destination_path = os.path.join(self.output_folder_path, os.path.basename(pdf_file))
                print(f"Moving file {pdf_file} to {destination_path}")
                shutil.move(pdf_file, os.path.join(self.output_folder_path, os.path.basename(pdf_file)))
                continue

            print(f"File: {pdf_file}")
            print("İcra Dairesi:", pdf_extractor.icra_dairesi)
            print("İcra Dosyası:", pdf_extractor.icra_dosyasi)
            print("Borçlu:", pdf_extractor.borclu)
            print("TCKN:", pdf_extractor.tckn)
            print("Asıl Alacak:", pdf_extractor.alacak)
            print("Feragat Edilen Tutar:", pdf_extractor.feragat)
            print("URL:", pdf_extractor.url)
            print("********************************")
            print("\n")



root = tk.Tk()
root.geometry('200x200')
app = ConverterFrame(root)
app.grid(row=0, column=0, padx=10, pady=10)
root.mainloop()


