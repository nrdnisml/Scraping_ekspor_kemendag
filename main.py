import requests
import ast
from bs4 import BeautifulSoup
import re
import pandas as pd
import lxml

# CHECK HSV
# HS17 : DATA HANYA SAMPAI ID 252610
# HS12 : DATA HANYA SAMPAI ID 262060

url = "https://exim.kemendag.go.id/home/checkHsV"
token = "dd57916ea5cb6fc242f06b66ae2287eee8007ddf01ca9c6f75df94cf353b36ba"
negara_id = '213'
form_data = {"negara_id": negara_id,"token":token}
r = requests.post(url,form_data)
hs_v = r.text

# get hs master
url = "https://exim.kemendag.go.id/home/getMasterHS"
form_data = {'hs_v': hs_v, 'token': token}
r = requests.post(url, form_data)
soup = BeautifulSoup(r.text, 'lxml')
items = soup.findAll('option')

id_komoditi = []
nama_komoditi = []

for i in items[1:]:
    komoditi = i.text.replace(' - ', ' ').replace(' - ', ' ').replace(' -', '')
    id_k = komoditi[:6]
    nama_k = komoditi[6:].strip()
    id_komoditi.append(id_k)
    nama_komoditi.append(nama_k)
    if hs_v == 'HS12' and id_k == '262060':
        break

    if hs_v == 'HS17' and id_k == '252610':
        break


#GET EKSPORTIR

komoditi = []
nama_perusahaan = []
alamat_perusahaan = []
email_perusahaan = []
# count = 0
url = "https://exim.kemendag.go.id/home/get_eksportir"
for i, k in zip(id_komoditi,nama_komoditi):
  form_data = {"hs" : i,"token":token}
  r = requests.post(url,data=form_data)
  data = r.json()
  # content = r.content.decode("utf-8")
  # content = ast.literal_eval(content)
  data = data['data']

  for d in data:
    komoditi.append(i + " - " + k)
    nama_perusahaan.append(d['nama_eksportir'])
    alamat_perusahaan.append(d['alamat_eksportir'])
    email_perusahaan.append(d['email_eksportir'])

    print('nama : ', nama_perusahaan)
  #   count = count + 1
  #   print(count)
  # if count > 1:
  #   break

data_dict = {'Negara':'Maroko', 'Komoditi':komoditi, 'Perusahaan':nama_perusahaan, 'Alamat':alamat_perusahaan, 'Email':email_perusahaan}
df = pd.DataFrame(data_dict,columns= ["Negara","Komoditi","Perusahaan","Alamat","Email"])

df.sort_values('Komoditi', ascending=True)
df.to_csv('Maroko.csv', sep=',', encoding='utf-8')
