from urllib import response
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

options = Options()
#options.add_argument('--headless')
options.add_argument('window-size=1920,1080')

navegador = webdriver.Chrome(options=options)
navegador.implicitly_wait(8)

navegador.get('https://www.airbnb.com')

sleep(5)
wait = WebDriverWait(navegador, 10)
input_element = wait.until(EC.presence_of_element_located((By.NAME, 'query')))
input_element.send_keys('Rio de Janeiro')
sleep(2)
input_element.submit()
sleep(2)

button = navegador.find_element_by_class_name('_l6n8jt')
button.click()
sleep(2)
button_checkin = navegador.find_element_by_class_name('_suql0c')
button_checkin.click()
sleep(2)
button_hospedes = navegador.find_element_by_class_name('_1f3kvcqz')
button_hospedes.click()
sleep(2)

buttonAdulto = navegador.find_elements_by_css_selector('button > span > svg > path[d="m2 16h28m-14-14v28"]')[0]
buttonAdulto.click()
sleep(1)
buttonAdulto.click()
sleep(1)

buttonBuscar = navegador.find_element_by_class_name('_1dbgthhp')
buttonBuscar.click()
sleep(4)


page_contet = navegador.page_source
site = BeautifulSoup(page_contet, 'html.parser')
dados_hospedagem = []
    
hospedagens = site.findAll('div', attrs={'itemprop': 'itemListElement'})
    
for hospedagem in hospedagens:

    hospedagem_descricao = hospedagem.find('meta', attrs={'itemprop': 'name'})
    hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})

    hospedagem_descricao = hospedagem_descricao['content']
    hospedagem_url = hospedagem_url['content']

    print('Descrição: ', hospedagem_descricao)
    print('URL: ', hospedagem_url)

    hospedagem_detalhes = hospedagem.find('div', attrs={'style': '--margin-bottom:var(--h-x-sf-jw);'})
    print('Detalhes da hospedagem: ', hospedagem_detalhes.text)

    preço = hospedagem.findAll('span')[-1].text
    print('Preço da hospedagem: ', preço)

    print()

    dados_hospedagem.append([hospedagem_descricao, hospedagem_url, hospedagem_detalhes.text, preço])

    dados = pd.DataFrame(dados_hospedagem, columns=['Descrição', 'URL', 'Detalhes', 'Preço'])

    dados.to_csv('hospedagens.xlsx', index=False)



