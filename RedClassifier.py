import pandas as pd
from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter as tk
import re
import glob
import os
import shutil
from PyPDF2 import PdfReader
import locale
import openpyxl

locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')


class RedClassifierGUI(tk.Frame):  # Inherit from tk.Frame
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Red Classifier GUI")

        self.folder_path = None
        self.excel_path = None

        # Create buttons
        self.select_folder_button = tk.Button(self, text="PDF Klasörünü Seç ", command=self.select_folder)
        self.select_excel_button = tk.Button(self, text="Excel Dosyasını Seç", command=self.select_excel)
        self.process_folder_button = tk.Button(self, text="Programı Başlat", command=self.process_folder)

        # Place buttons on the GUI
        self.select_folder_button.pack(pady=10)
        self.select_excel_button.pack(pady=10)
        self.process_folder_button.pack(pady=10)

    def select_folder(self):
        # Open a file dialog to select the folder
        self.folder_path = filedialog.askdirectory()
        print(f"Selected Folder: {self.folder_path}")
        messagebox.showinfo("Başarılı", "PDF klasörü başarıyla seçildi.")


    def select_excel(self):
        # Open a file dialog to select the Excel file
        self.excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        print(f"Selected Excel: {self.excel_path}")
        messagebox.showinfo("Başarılı", "Doldurulacak excel dosyası başarıyla seçildi.")

    def process_folder(self):
        if self.folder_path and self.excel_path:
            red_classifier = RedClassifier(self.folder_path, self.excel_path)

            if self.folder_path is None:
                messagebox.showwarning("Error", "Lütfen klasörü seçiniz.")
                return

            if self.excel_path is None:
                messagebox.showwarning("Error", "Lütfen exceli seçiniz.")
                return
            red_classifier.process_folder()

            # Display a message box when the process is finished
            messagebox.showinfo("Finished", "Program sonlandı.")
        else:
            messagebox.showwarning("Error", "Klasör ve exceli seçiniz.")


class RedClassifier:

    def __init__(self, folder_path, excel_path):  # Modified constructor to include excel_path
        self.folder_path = folder_path
        self.excel_path = excel_path  # Store the Excel path

    def extract_text_from_pdf(self, pdf_file):
        try:
            reader = PdfReader(pdf_file)
            self.extracted_text = ""

            for page in reader.pages:
                self.extracted_text += page.extract_text()

            return self.extracted_text
        except Exception as e:
            print(f"Hata oluştu (PDF okunamadı): {e}")
            return None

    def get_extracted_text(self):
        extracted_text = self.extracted_text

        # Replace consecutive whitespace characters with a single space
        extracted_text = re.sub(r'\s+', ' ', extracted_text)

        icra_dairesi_match = re.search(r'\b([A-ZĞÜŞİÖÇ]+\s\d+\.)', extracted_text, re.MULTILINE)
        self.icra_dairesi = icra_dairesi_match.group(1).replace('\n', ' ') if icra_dairesi_match else None

        icra_dosyasi_match = re.search('İCRA DAİRESİ (\d{4}/\d{2,7}) ESAS', extracted_text)
        self.icra_dosyasi = icra_dosyasi_match.group(1) if icra_dosyasi_match else None

        karar_match = re.search(r'tensip(.+?)\s*yard[ıi]mc[ıi]', extracted_text, re.DOTALL | re.IGNORECASE)
        self.karar = karar_match.group(1).strip() if karar_match else None

        if self.karar is None and "karar verildi" in extracted_text.lower():
            self.karar = "Karar Verildi"

    def get_kategori(self):
        aciz_keywords = ["aciz vesikası", "aciz belgesi"]
        infaz_keywords = ["infazen kapalı", "infazen"]
        temlik_keywords = ["temlik listesi"," temlik sözleşmesi listesi", "temlik ve vekaletname", "temlikname ve vekaletname"]
        itiraz_olmayanlar = ["7 gün içinde itiraz", "7 gün içerisinde itiraz", "İİK'nun 16. Madde", "7(yedi) gün içinde", "7 gün", "7 gün içinde", "16. madde", "itiraz ve şikayet", "itiraz/şikayet", "16 madde", "İ.İ.K."]
        itiraz_keywords = ["itiraz"]
        haricen_keywords = ["haricen tahsil"]
        tckn_keywords = ["tckn eksik", "T.C kimlik numarası", "T.C kimlik bilgisi", "TC kimlik", "kimlik numarası"]
        bakanlık_keywords = ["hazine bakanlığı", "maliye bakanlığı"]
        taraf_keywords = ["taraf uyuşmazlığı"]

        tutar_keywords = ["2500 TL", "takip çıkış miktarı", "yasal sınırı", "belirtilen miktardan fazla", "anapara", "takip bakiye", "2.500 TL"]

        takip_keywords = ["takip talebi eksik", "takip talebi"]
        if self.karar is None:
            return None
        elif any(keyword.lower() in self.karar.lower() for keyword in itiraz_olmayanlar):
            return None  # If "itiraz olmayanlar" keywords are present, return None
        elif any(keyword.lower() in self.karar.lower() for keyword in itiraz_keywords):
            return "itiraz"  # If "itiraz" keywords are present, return "itiraz"
        elif any(keyword.lower() in self.karar.lower() for keyword in itiraz_olmayanlar):
            return None  # If "itiraz olmayanlar" keywords are present, return None
        elif any(keyword.lower() in self.karar.lower() for keyword in itiraz_keywords):
            return "itiraz"  # If "itiraz" keywords are present, return "itiraz"

        elif any(keyword.lower() in self.karar.lower() for keyword in
                 aciz_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "aciz vesikası"

        elif any(keyword.lower() in self.karar.lower() for keyword in takip_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "takip talebi"

        elif any(keyword.lower() in self.karar.lower() for keyword in
                 temlik_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "temlik"

        elif any(keyword.lower() in self.karar.lower() for keyword in
                 tckn_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "tckn"

        elif any(keyword.lower() in self.karar.lower() for keyword in
                 tutar_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "yasal tutar"

        elif any(keyword.lower() in self.karar.lower() for keyword in
                 infaz_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "infazen kapalı"

        elif any(keyword.lower() in self.karar.lower() for keyword in
                 bakanlık_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "bakanlık"

        elif any(keyword.lower() in self.karar.lower() for keyword in
                 haricen_keywords) and "7 gün içinde itiraz" not in self.karar.lower():
            return "haricen tahsil"

        elif any(keyword.lower() in self.karar.lower() for keyword in itiraz_olmayanlar):
            return None  # If "itiraz olmayanlar" keywords are present, return None
        elif any(keyword.lower() in self.karar.lower() for keyword in itiraz_keywords):
            return "itiraz"  # If "itiraz" keywords are present, return "itiraz"

    def process_folder(self):
        pdf_extractor = RedClassifier(self.folder_path, self.excel_path)

        data = []
        columns = ["ICRA_DAIRESI", "ICRA_DOSYASI", "KARAR", "KATEGORI"]

        # Load existing data from the Excel file, if it exists
        if os.path.exists(self.excel_path):
            existing_df = pd.read_excel(self.excel_path)
            data.extend(existing_df.values.tolist())

        for pdf_file in glob.glob(os.path.join(self.folder_path, "*.pdf")):
            pdf_extractor.extract_text_from_pdf(pdf_file)
            pdf_extractor.get_extracted_text()

            if pdf_extractor.icra_dairesi and pdf_extractor.icra_dosyasi and pdf_extractor.karar:
                data.append([
                    pdf_extractor.icra_dairesi,
                    pdf_extractor.icra_dosyasi,
                    pdf_extractor.karar,
                    pdf_extractor.get_kategori()
                ])

        df = pd.DataFrame(data, columns=columns)

        try:
            df.to_excel(self.excel_path, index=False)
            print("Data written to Excel successfully.")
        except Exception as e:
            print(f"Error writing to Excel: {e}")

    # def load_data(self):
    #     excel_data = pd.read_excel(self.excel_file, sheet_name='Sheet1', usecols='B,G,H,I')
    #     self.df = excel_data.copy()


# # Example usage:
# folder_path = "C:/Users/hademir/Desktop/RED PDFLER"
# red_classifier = RedClassifier(folder_path)
# red_classifier.process_folder(folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_minsize(width=400, height=300)
    app = RedClassifierGUI(root)
    app.grid(row=0, column=0, padx=10, pady=10)
    root.mainloop()
