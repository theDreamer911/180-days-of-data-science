from bs4 import BeautifulSoup
import requests
import json
import re

gheaders = {
    'Referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp? \
    newsearch=true&queryText=support',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) \
    Gecko/20100101 Firefox/27.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, \
    image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}
# URL
url = input("Masukkan link: ")
IEEE_response = requests.get(url=url, headers=gheaders)
# Mengambil response dengan format lxml
soup = BeautifulSoup(IEEE_response.text, 'lxml')


# Menerapkan regex untuk memperoleh informasi penting pada xplGlobal
pattern = re.compile(r'xplGlobal.document.metadata=(.*?);',
                     re.MULTILINE | re.DOTALL)
# Mengimplementasikan regex pada script
script = soup.find("script", text=pattern)
# Melakukan groupping pada script
res_dic = pattern.search(script.string).group(1)


# Menyimpan data dalam format json
json_data = json.loads(res_dic)

try:
    # Data author
    author = json_data['authors']
    writer = ', '.join([author[i]['name'] for i in range(len(author))])

    # Data judul
    title = json_data['formulaStrippedArticleTitle']

    # Data abstraksi
    abstract = json_data['abstract']

    # Data tahun terbit
    years = json_data['publicationYear']

    # Data nama publikasi
    publication = json_data['publicationTitle']

    # print("Pemrosesan data...")

    # Menulis data yang diperoleh menjadi suatu dataset
    print(writer, ';', title, ';', abstract, ';', years, ';',
          publication, ';\n', file=open("paper_data.csv", 'a'))

    print("\aData berhasil ditambahkan...")

except:
    print("Format data berbeda, parsing gagal...")
