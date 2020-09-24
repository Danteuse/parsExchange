
""" 
Скрипт скачивает ежедневный курс 
валюты с помощью API сайта ЦБ РФ в виде XML файла. 
Затем извлекает из скачанного XML-файла 
данные о курсе валюты и записывает их в отдельный файл exchange.txt.

"""

import urllib.request
from xml.dom import minidom

# Ежедневные курсы валют ЦБ РФ
url = "http://www.cbr.ru/scripts/XML_daily.asp"

# Чтение URL
webFile = urllib.request.urlopen(url)
data = webFile.read()
	
# Имя файла
UrlSplit = url.split("/")[-1]
ExtSplit = UrlSplit.split(".")[1]
FileName = UrlSplit.replace(ExtSplit, "xml")
			
with open(FileName, "wb") as localFile:
	localFile.write(data)

webFile.close()

# Парсинг xml и запись данных в файл
doc = minidom.parse(FileName)

# Извлечение даты
root = doc.getElementsByTagName("ValCurs")[0]
date = "Текущий курс гонконгского доллара к российскому рублю на {date}г.: \n".format(date=root.getAttribute('Date'))

# Извлечение данных по валюте
currency = doc.getElementsByTagName("Valute")

with open("exchange.txt","w") as out:
	out.write(date)
	for rate in currency:
		value = rate.getElementsByTagName("Value")[0]
		nominal = rate.getElementsByTagName("Nominal")[0]
		sid = rate.getAttribute("ID")
		if sid == "R01200":
			break
	value = value.firstChild.data
	nominal = nominal.firstChild.data
	valueFloat = float(value.replace(",", "."))
	nominalInt = int(nominal)
	exchangeRate = valueFloat / nominalInt
	
	str = "{0}".format(exchangeRate)
	out.write(str)