import re
import glob
import os

from PyPDF2 import PdfReader

class PdfExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.extracted_text = None

    def read_files(self):
        os.chdir(path= "")
        pdfs = []
        for file in glob.glob("*.pdf"):
            print(file)
            pdfs.append(file)

    def extract_text_from_pdf(self):
        try:
            """reader = PdfReader(self.file_path)
            page = reader.pages[0]
            self.extracted_text = page.extract_text()"""
            reader = PdfReader(self.file_path)
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

        feragat_match = re.findall(r'([\d.,]+) TL', extracted_text)
        self.feragat = feragat_match[1] if feragat_match else None

        url_match = re.search(r'https://evrakdogrula\.uyap\.gov\.tr/[a-zA-Z0-9]+', extracted_text)
        self.url = url_match.group() if url_match else None

# Kullanım örneği


pdf_path = "İstanbul 3. İcra Dairesi-2023_34593-Feragat-7420 Belgesi 14.09.2023-299708982-9345836445.pdf"

pdf_extractor = PdfExtractor(pdf_path)
pdf_extractor.extract_text_from_pdf()
extracted_text = pdf_extractor.get_extracted_text()
#print(extracted_text)

print("İcra Dairesi:", pdf_extractor.icra_dairesi)
print("İcra Dosyası:", pdf_extractor.icra_dosyasi)
print("Borçlu:", pdf_extractor.borclu)
print("TCKN:", pdf_extractor.tckn)
print("Asıl Alacak:", pdf_extractor.alacak)
print("Feragat Edilen Tutar:", pdf_extractor.feragat)
print("URL:", pdf_extractor.url)
