from PyPDF2 import PdfReader


def extractPdf(rawPdf):
    reader = PdfReader(rawPdf)
    page = reader.pages[0]
    extractedPdf = page.extract_text()
    return extractedPdf
extractPdf("İstanbul Anadolu 6. İcra Dairesi-2019_33917-Feragat-7420 Belgesi 06.09.2023-183232300-9313707124.pdf")

#def extractInfo()