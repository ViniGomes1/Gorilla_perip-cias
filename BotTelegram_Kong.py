####KONG ALPHA 0.O.2####
from flask import Flask, request

from urllib.parse import urlparse

import telebot
from telebot import formatting

import time
import threading

from MercadoLivreScraping import ScrapingML
from AmazonScraping import ScrapingAmazon

##INICIALIZAR BOT##
CHAVE_API = "8009230244:AAHcHJL3L65eQDg22BnESWjrfl_7uvtdPXg"
bot = telebot.TeleBot(CHAVE_API)
#bot.set_webhook()

##PARAMETROS GLOBAIS##
LINK_PARAMETRO = ""
NOME_PARAMETRO = ""
TERMINADO = False
CHAT_ID = 0
CAPTION_ID = ""

###VARIAVEIS CONDICIONAIS####
#INICIADO = False
INICIADO_LINK = False
INICIADO_FOTO = False
INICIADO_NOME = False
#######

#flask
app = Flask(__name__)

####PARA INSERIR UM LINK####
@bot.message_handler(commands=["link"], func=lambda message : INICIADO_LINK)
def link(mensagem):
    global LINK_PARAMETRO, INICIADO_LINK, INICIADO_FOTO
    mensagem_resposta = ""
    texto = mensagem.text
    link = texto.replace('/link ', '')

    if mensagem_resposta == "":
        mensagem_resposta = """Insira um link válido"""

    if urlparse(link).scheme:
        LINK_PARAMETRO = link
        mensagem_resposta = """Ok agora mande uma foto com /foto na descrição da mesma"""
        INICIADO_LINK = False
        INICIADO_FOTO = True

    bot.send_message(mensagem.chat.id, mensagem_resposta)


####PARA INSERIR UMA FOTO####
@bot.message_handler(content_types=['photo'], func=lambda message : INICIADO_FOTO)
def foto(mensagem):
    global CAPTION_ID, INICIADO_FOTO, INICIADO_NOME

    if mensagem.caption == "/foto":
        CAPTION_ID = mensagem.photo[0].file_id
        mensagem_resposta = "Foto upada, agora escolha um nome com /nome"
        print("enviada")
        INICIADO_FOTO = False
        INICIADO_NOME = True
    else:
        mensagem_resposta = "Mande uma imagem válida"
    bot.send_message(mensagem.chat.id, mensagem_resposta)


####PARA COLOCAR UM NOME####
@bot.message_handler(commands=["nome"], func=lambda message : INICIADO_NOME)
def nome(mensagem):
    global NOME_PARAMETRO, TERMINADO, INICIADO_NOME
    texto = mensagem.text
    nome_texto = texto.replace('/nome ', '')

    if nome_texto != "":
        NOME_PARAMETRO = nome_texto
        bot.send_message(mensagem.chat.id, """Ok, irei preparar o anuncio""")
        TERMINADO = True
    else:
        INICIADO_NOME = True

    print(nome_texto)


####ANUNCIO FINALIZADO####
@bot.message_handler(commands=["novo_anuncio"])
def novo_anuncio(mensagem):
    global INICIADO_LINK
    INICIADO_LINK = True
    texto = """ Ok, me passe os seguintes parâmetros em sequencia

    /link {coloque o link do anuncio}
    /foto {coloque a foto que quer para o anuncio}
    /nome {coloque o nome que quer no anuncio}
    """
    bot.send_message(mensagem.chat.id, texto)

#####AMAZON####
@bot.message_handler(commands=["amazon"])
def amazon(mensagem):
    valid_url = "https://amzn.to/"
    texto = mensagem.text
    url_ML = texto.replace('/amazon ', '')
    if valid_url in url_ML:
        bot.send_message(mensagem.chat.id, "Ok irei preparar")
        amazon_scraping(url_ML, mensagem.chat.id)
    else:
        bot.send_message(mensagem.chat.id, "Insira um link do mercado livre o link deve iniciar com 'https://amzn.to/'")

def amazon_scraping(link, chat):
    gorilla = u'\U0001F98D'
    top = u'\U0001F51D'
    white_check = u'\U00002705'

    scraping = ScrapingAmazon(link=link)

    soup = scraping.requestSelenium()
    core_price = scraping.corePrice(soup)

    total_price = scraping.totalPrice(core_price)
    discount_verify = scraping.discountVerify(core_price)

    discount_price = []
    percentage_discount = ""

    image_source = scraping.image_source(soup)

    if discount_verify:
        discount_price = scraping.discountPrice(core_price)
        percentage_discount = scraping.percentageDiscount(core_price)

    titulo = scraping.title(soup)

    if discount_verify:
        final_text = formatting.hbold(titulo.replace("        ", "") + """
    
DE: """ ) + formatting.hstrikethrough(discount_price[0]) + formatting.hbold("""
POR: """ + total_price[1] + " " + percentage_discount + """ """ + top + white_check + """

Só abrir o link abaixo! 
""") + link + """

!!""" + gorilla + """Promoção sujeita a alteração, aproveite""" + gorilla + """!!"""
    else:
        final_text = formatting.hbold(titulo.replace("        ", "") + """

POR APENAS: """ + total_price[1] + """ """ + top + white_check + """

Só abrir o link abaixo! 
""") + link + """

!!""" + gorilla + """Promoção sujeita a alteração, aproveite""" + gorilla + """!!"""
    bot.send_photo(chat, image_source, final_text, parse_mode='HTML')



#####MERCADOLIVRE####
@bot.message_handler(commands=["mercado_livre"])
def mercado_livre(mensagem):
    valid_url = "https://mercadolivre.com/"
    texto = mensagem.text
    url_ML = texto.replace('/mercado_livre ', '')
    if valid_url in url_ML:
        bot.send_message(mensagem.chat.id, "Ok irei preparar")
        mercado_livre_scraping(url_ML, mensagem.chat.id)
    else:
        bot.send_message(mensagem.chat.id, "Insira um link do mercado livre o link deve iniciar com 'https://mercadolivre.com/'")

def mercado_livre_scraping(link, chat):
#    global CHAT_ID, TERMINADO

    gorilla = u'\U0001F98D'
    top = u'\U0001F51D'
    white_check = u'\U00002705'


    scraping = ScrapingML(link)
    requesting = scraping.request()

    money_fractions = scraping.find_children(requesting, 'andes-money-amount__fraction', True)
    discount = scraping.find_children(requesting, 'poly-price__installments', False)

    image_link = scraping.link
    product_title = scraping.title(requesting)
    amount_discount = scraping.amount_discount(requesting)

    if len(money_fractions) <= 2:
        anuncio_ML = formatting.hbold(product_title + """
        
POR: R$ """ + money_fractions[0] + " " + amount_discount + """ """ + top + white_check + """
""" + discount[0].text + """ 

Só abrir o link abaixo! 
""") + link + """

!!""" + gorilla + """Promoção sujeita a alteração, aproveite""" + gorilla + """!!"""

    else:
        anuncio_ML = formatting.hbold(product_title + """
    
DE: """ ) + formatting.hstrikethrough("R$ " + money_fractions[0]) + formatting.hbold("""
POR: R$ """ + money_fractions[1] + " " + amount_discount + """ """ + top + white_check + """
""" + discount[0].text + """ 

Só abrir o link abaixo! 
""") + link + """

!!""" + gorilla + """Promoção sujeita a alteração, aproveite""" + gorilla + """!!"""



    bot.send_photo(chat, image_link, anuncio_ML, parse_mode='HTML')


####SAIR DO BOT####
@bot.message_handler(commands=["sair"])
def sair(mensagem):
    bot.reply_to(mensagem, "Tchau porra")


def anuncio_verificar(mensagem):
    global TERMINADO
    if TERMINADO:
        return True
    return False

####SAIDA FINAL DO ANUNCIO FEITO####
def anuncio_feito():
    global CHAT_ID, TERMINADO
    while not TERMINADO:
        time.sleep(1)
    mensagem_feita = (formatting.hbold(NOME_PARAMETRO) + """
    
    
""" + LINK_PARAMETRO)
    bot.send_photo(CHAT_ID, CAPTION_ID, mensagem_feita , parse_mode='HTML')


threading.Thread(target=anuncio_feito).start()


#FUNÇÃO PARA LIDAR COM O INICIO DAS MENSAGENS###
@bot.message_handler(func=lambda message: INICIADO_LINK)
def iniciado_link(message):
    bot.reply_to(message, "Esta mensagem não é um link, coloque /link + seu_link para prosseguir")


@bot.message_handler(func=lambda message: INICIADO_FOTO)
def iniciado_foto(message):
    bot.reply_to(message, "Esta mensagem não é uma foto, coloque uma foto com /foto para prosseguir")


@bot.message_handler(func=lambda message: INICIADO_NOME)
def iniciado_nome(message):
    bot.reply_to(message, "Esta mensagem não é um nome válido coloque um nome válido para prosseguir")


def verificar(mensagem):
    return True

####MENSAGEM GENÉRICA SEM CONDIÇÕES####
@bot.message_handler(func=verificar)
def responder_generico(mensagem):
    global CHAT_ID
    texto_generico = """ Primeiramente saiba que o bot tem apenas UMA funcionalidade, escolha ela abaixo
    /novo_anuncio para fazer um anuncio personalizado
    /mercado_livre {link} para fazer um anuncio mercado livre a partir de um link
    /amazon {link} para fazer um anuncio amazon a partir de um link
    /sair para sair
    """
    bot.reply_to(mensagem, texto_generico)
    CHAT_ID = mensagem.chat.id
@app.route('/' + CHAVE_API, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='http://172.17.0.2:5000' + CHAVE_API)
    return 'Webhook configurado', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

#https://gorilla-peripecias.onrender.com
