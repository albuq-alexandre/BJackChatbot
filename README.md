# BJackChatbot

Chatbot que joga Single BlackJack no telegram. Utiliza o Watson Assistant como gerenciador e a API do Deck of Cards para consultas.

## Configurações

``pip install -r requirements.txt``

A seguir as variáveis que devem ser configuradas no Heroku:

* WATSON_ASSISTANT_TOKEN: token IAM do Watson Assistant
* WATSON_ASSISTANT_URL: URL do Watson Assistant
* ASSISTANT_ID: ID do Assistant criado no Watson Assistant
* S2T_TOKEN: token IAM da API Watson SpeechToText
* S2T_URL: URL da API Watson SpeechToText
* T2S_TOKEN: token IAM da API Watson TextToSpeech
* T2S_URL: URL da API Watson TExtToSpeech
* TELEGRAM_BOT_TOKEN: token do bot criado no Telegram
* TELEGRAM_WEBHOOK: url da aplicação do heroku (https://\<appname\>.herokuapp.com)


## Bugs conhecidos

* TODO
