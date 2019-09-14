from bs4 import BeautifulSoup
import requests

url =
reponse = requests.get(url, timeout=5)
contnent = BeautifulSoup(response.content, 'html.parser')
