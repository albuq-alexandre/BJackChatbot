# bjack-chat-app-demo
Single Blackjack Telegram Chatbot School Project using IBM Cloud  
  
![Badge](https://img.shields.io/badge/license-MIT-green) 
![Badge](https://img.shields.io/badge/python-v3.8-blue) 
![Badge](https://img.shields.io/badge/ibm_watson-v5.2.2-blue) 
![Badge](https://img.shields.io/badge/ibm_cloud_sdk_core-v3.10.1-blue) 
[![Heroku App Status](http://heroku-shields.herokuapp.com/bjack-chat-app-demo)](https://bjack-chat-app-demo.herokuapp.com)
  
<!--ts-->  Tabela de Conteúdo:
 * [Identificação](#stt_tts_iesb2020)  
 * [Autores](#disciplina)    
 * [Sobre](#sobre)    
 * [Instalação](#instalação-local)  
 * [Como Usar](#como-usar)  
 * [Requisitos](#pré-requisitos)  
 * [Help](#help)  
 * [Créditos Adicionais](#Créditos-adicionais-para-os-projetos)
<!--te-->  
  
  
###  Disciplina 

> *P8902-IANA-Chatbot*  
>**Professor**: Rafael Brasileiro de Araujo  
###  Alunos  
>- **Alexandre de Sousa Albuquerque**
>- **Celso de Melo**
>- **Juliano Ortigoso Gaspar**

## Sobre  

 BJackChatbot é um Chatbot que joga Single BlackJack no telegram. Utiliza o Watson Assistant como gerenciador e a API do Deck of Cards para consultas.

## Instalação local

``pip install -r requirements.txt``

A seguir as variáveis que devem ser configuradas no Heroku, ou no ambiente local(ngrok):

* WATSON_ASSISTANT_TOKEN: token IAM do Watson Assistant
* WATSON_ASSISTANT_URL: URL do Watson Assistant
* ASSISTANT_ID: ID do Assistant criado no Watson Assistant
* S2T_TOKEN: token IAM da API Watson SpeechToText
* S2T_URL: URL da API Watson SpeechToText
* T2S_TOKEN: token IAM da API Watson TextToSpeech
* T2S_URL: URL da API Watson TExtToSpeech
* TELEGRAM_BOT_TOKEN: token do bot criado no Telegram
* TELEGRAM_WEBHOOK: url da aplicação do heroku (https://\<appname\>.herokuapp.com)

## Run app

``python main.py``

## Help

Utilize linguagem natural, via texto ou áudio para usar uma das funcionalidades. Use a palavra ***Menu*** pra ver:

- **Iniciar:** Inicia o  Jogo ***BlackJack!***;
  - **Mais uma:** durante o jogo, para receber uma carta;
  - **Parar:** para finalizar seu turno.
- **Listar:** Lista suas partidas de BlackJack no jogo atual;
- **Estatística:** Mostra seu percentual de vitórias;
- **Créditos:** Mostra os créditos do projeto;
- **Encerrar:** Quando estiver perdido, diga ***Tchau*** que a gente começa de novo!</i>


## Créditos adicionais para os projetos:
* https://github.com/crobertsbmw/deckofcards
* https://github.com/rafaelbr/MovieBot
* https://github.com/d-Rickyy-b/Python-BlackJackBot
* https://github.com/python-telegram-bot/python-telegram-bot
