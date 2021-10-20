import telegram
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters
from session_manager import SessionManager
from io import BytesIO
from queue import Queue
from threading import Thread
import os
import assistant
import voice
import os
import logging
# from pyngrok import ngrok
import base64
from game import BlackJackGame, FixSizeOrderedDict

from collections import OrderedDict

#Variaveis de ambiente de configuracao
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
WEBHOOK_URL = os.environ.get('TELEGRAM_WEBHOOK')

# if not WEBHOOK_URL:
#     http_tunnel = ngrok.connect(PORT, bind_tls=True)
#     WEBHOOK_URL = http_tunnel.public_url



# PORT = 8443

#configura logging e config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger('TelegramBot')

#Cria a Pilha de games

games = FixSizeOrderedDict(maxlen=20)


def setup():

    #cria updater e dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #define handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text, message)
    dispatcher.add_handler(message_handler)

    voice_handler = MessageHandler(Filters.voice, receive_voice)
    dispatcher.add_handler(voice_handler)

    #inicia webhook com a porta configurada pelo heroku
    #o heroku cuida automaticamente do proxy reverso, portanto a porta deve ser a fornecida pelo heroku
    #nas variáveis de ambiente
    updater.start_webhook(listen='0.0.0.0',
                             port=int(PORT),
                             url_path=TOKEN,
                            webhook_url=WEBHOOK_URL + '/' + TOKEN)

    #configura webhook
    # updater.bot.set_webhook(WEBHOOK_URL + '/' + TOKEN)

    #para a aplicacao nao terminar, eh necessario chamar o idle para que ela fique sempre rodando
    updater.idle()

    return (updater, dispatcher)

def start(update, context):
    assistant.validate_session(update.effective_chat.id)
    games[update.effective_chat.id] = BlackJackGame()
    response_text = assistant.send_message(SessionManager.getInstance().getSession(update.effective_chat.id), '', games[update.effective_chat.id])
    if 'text' in response_text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_text['text'])
    if 'img' in response_text:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=response_text['img'])

def message(update, context):
    message_received = update.message.text

    assistant.validate_session(update.effective_chat.id)

    if not update.effective_chat.id in games:
        games[update.effective_chat.id] = BlackJackGame()

    response_text = assistant.send_message(SessionManager.getInstance().getSession(update.effective_chat.id), update.message.text, games[update.effective_chat.id])

    if 'text' in response_text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_text['text'], parse_mode=telegram.ParseMode.HTML)
    if 'img' in response_text:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=base64.b64decode(response_text['img']))

def receive_voice(update, context):
    assistant.validate_session(update.effective_chat.id)
    audio_file = BytesIO(update.message.voice.get_file().download_as_bytearray())
    text = voice.convert_voice(audio_file)
    response_text = assistant.send_message(SessionManager.getInstance().getSession(update.effective_chat.id), text, games[update.effective_chat.id], audible=True)
    context.bot.send_voice(chat_id=update.effective_chat.id, voice=voice.convert_text(response_text['text']))


