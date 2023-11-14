import re
import glob
import os
import shutil

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

# Kullanım örneği
folder_path = "C:/Users/hademir/PycharmProjects/pythonProject"
output_folder_path = "C:/Users/hademir/PycharmProjects/pythonProject/output"

pdf_extractor = PdfExtractor(folder_path)

for pdf_file in glob.glob(os.path.join(folder_path, "*.pdf")):


    pdf_extractor.extract_text_from_pdf(pdf_file)
    pdf_extractor.get_extracted_text()

    if pdf_extractor.feragat is None or len(pdf_extractor.alacak) < 2:
        print(f"Moving file {pdf_file}")
        shutil.move(pdf_file, os.path.join(output_folder_path, os.path.basename(pdf_file)))
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
