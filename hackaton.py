import requests
from bs4 import BeautifulSoup as BS

data = []

def get_html(url):
    return requests.get(url).text

def get_data(html):
    page_html = BS(html, "lxml")
    all_news = page_html.find_all('div', class_="Tag--article")
    for news in all_news:
        title = news.find('a', class_="ArticleItem--name").text
        image = news.find('img').get('src')
        data.append((title, image))

def main():
    url = "https://kaktus.media/?lable=8&date=2022-01-24&order=time"
    html = get_html(url)
    get_data(html)
    return data

import telebot
from MyToken import token

bot = telebot.TeleBot(token)
kaktus = main()
@bot.message_handler(commands=['start'])
def start(message):

    chat_id = message.chat.id
    i = 1
    for news in kaktus[0:20]:
        bot.send_message(chat_id, f"{i} {news[0]}")
        i += 1
    msg = bot.send_message(chat_id, "Номер желаемой новости:")
    bot.register_next_step_handler(msg, get_title)

def get_title(message):
    chat_id = message.chat.id
    ind = int(message.text) - 1
    bot.send_message(chat_id, kaktus[ind])

    msg = bot.send_message(chat_id, "Номер желаемой иллюстрации:")
    bot.register_next_step_handler(msg, get_image)

def get_image(message):
    chat_id = message.chat.id
    ind = int(message.text) - 1
    bot.send_message(chat_id, kaktus[ind][1])

@bot.message_handler(commands=['quit'])
def quit(message):
    bot.send_message(message.chat.id, "До свидания!")
bot.polling()


