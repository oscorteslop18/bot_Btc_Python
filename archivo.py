from bs4 import BeautifulSoup
import requests
import schedule
from datetime import date
from datetime import datetime


def bot_send_text(bot_message):
    
    bot_token = '1720650081:AAE4tzG7QQp2Vc6fdfTJGdgPs81GSjfGPok'
    bot_chatID= '518332547'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def btc_scraping():
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
    format_result = result.text
    return format_result

def btc_scraping_dolar():
    url = requests.get('https://www.banxico.org.mx/tipcamb/llenarTiposCambioAction.do?idioma=sp')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('div', {'id': 'tdSF43718'})
    format_result = result.text
    return format_result.replace('$','')


def report():
    today = date.today()
    fl_str = today.strftime('%d/%m/%Y')
    btc_price =  'El dia de hoy : ' + fl_str + ' El precio del Dolar es de '+ btc_scraping_dolar() + '\n'
    btc_price +='El dia de hoy : ' + fl_str + ' El precio del Bitcoin es de '+ btc_scraping()  + '\n'
    btc_price +='El dia de hoy : ' + fl_str + ' El precio del Bitcoin en pesos MX  es de '+ str((float(btc_scraping_dolar()) * float(btc_scraping().replace('$','').replace(',',''))))


    bot_send_text(btc_price)


if __name__ == '__main__':
    print("Se esta ejecutando el bot")
    schedule.every().day.at("13:44").do(report)

    while True:
        schedule.run_pending()