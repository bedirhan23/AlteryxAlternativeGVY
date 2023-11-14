import re

text = ("İstanbul 1. İcra Dairesi\n2023/37171 İcra Dosyası\n\nBorçlu: GÖKHAN BULCU / 45234571482\n\nAlacaklı ve Vekili : GELECEK VARLIK YÖNETİMİ ANONİM ŞİRKETİ  Av. BÜŞRA DAĞ DERNELİ  Av. VERDA\nPAZARBAŞI  Av. ELÇİN YÜKSEL ÖZGÜZ  Av. ÖZGÜR ALTUNDAL\nHSBÇ BANK A.Ş.  Av. MUSTAFA TERZİ\n\nKapanış Tarihi : 01.10.2023\nKapatma Nedeni : 7420 Sayılı Kanunun Geçici 3.Maddesi Kapsamında Feragat\n\nAlacaklı Varlık Yönetim Şirketidir Temlik 16.08.2022 Tarihinden Öncedir.\nVergi veya Mükellefiyet Numarası : 3900579474  / 0000564745742\nTicaret Sicil Numarası : 111606-5\n\nİşbu dosya, 19.10.2005 tarih ve 5411 sayılı Bankacılık Kanunu kapsamında faaliyet gösteren varlık yönetim\nşirketlerince, bankalardan 15.08.2022 tarihi (bu tarih dâhil) itibarıyla devir ve temlik alınan bireysel nitelikli her türlü kredi\nsözleşmesinden kaynaklı alacağın, 7420 sayılı Kanunun yürürlüğe girdiği tarih itibarıyla anapara takip bakiyesinin 2.500\nTürk lirası ve altında kalması ve 03.11.2022 tarihli ve 7420 sayılı Gelir Vergisi Kanunu ile Bazı Kanun ve Kanun\nHükmünde Kararnamelerde Değişiklik Yapılmasına Dair Kanununun Geçici 3 üncü maddesi kapsamında alacak\nhakkından feragat edilmesi nedeniyle kapatılmıştır.\n\nİcra Müdür Yardımcısı\nHÜLYA KOÇAK, 126619\n\nAsıl Alacak : 2.594,78 TL\nFeragat Edilen Tutar : 6.488,12 TL\nZorlu alacak "
        "UYAP Bilisim Sistemindeki bu dökümana https://evrakdogrula.uyap.gov.tr/d971WbL2 adresinden erisebilirsiniz.")


icra_dairesi = re.compile('(.+) İcra Dairesi')
print(icra_dairesi.search(text).group(1))

icra_dosyası = re.compile('(.+) İcra Dosyası')
print(icra_dosyası.search(text).group(1))
# Metni arayın
borclu_tckn = re.findall(r"Borçlu: (.*) / (.*)", text)
alacak_regex = re.compile(r'Asıl Alacak : ([\d.,]+) TL')
alacak = alacak_regex.search(text)
feragat_regex = re.compile(r'Feragat Edilen Tutar : ([\d.,]+) TL')
feragat = feragat_regex.search(text)

# Sonuçları alın
borclu = borclu_tckn[0][0]
tckn = borclu_tckn[0][1]
# Metni arayın
#url = re.findall(r"https://(.*)\s", text)[0]
url_regex = re.compile(r'https://evrakdogrula\.uyap\.gov\.tr/[a-zA-Z0-9]+')
url = url_regex.findall(text)

# Sonuçları alın
if alacak:
        print('Asıl Alacak Tutarı:', alacak.group(1))
else:
        print("Asıl")

if feragat:
        print('Feragat Edilen Tutar:', feragat.group(1))

else:
        print("feragat")
print(url)
print(borclu, tckn)
