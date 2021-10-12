import sys


def main(dict):

    acao = dict['acao']
    
    if acao == 'iniciar':
        resposta = 'Cartas do Dealer:\n[8♥] [?]\nSuas cartas:\n[Q♣] [2♠]'
    elif acao == 'mais1carta':
        resposta = 'Cartas do Dealer:\n[8♥] [?]\nSuas cartas:\n[Q♣] [2♠] [7♦]'
    elif acao == 'parar':
        resposta = 'Fim de jogo!\nCartas do Dealer:\n[8♥] [K♥] - 18 pontos\nSuas cartas:\n[Q♣] [2♠] [7♦] - 19 pontos.\nVocê venceu!!!'
    elif acao == 'estatistica':
        resposta = 'Você ganhou 25 jogos e perdeu 15.\nAproveitamento de 62,5%.'
    else:
        resposta = 'Opção inválida!'
    
    return { 'resposta': resposta }
