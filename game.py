import requests
import io
import matplotlib.pyplot as plt
from PIL import Image
import base64
from collections import OrderedDict


class Deck:

    def __init__(self, deck_count=1):
        self.BASE_URL = 'http://deckofcardsapi.com/api/'
        endpoint = 'deck/new/shuffle/'
        parameters = '?deck_count=' + str(deck_count)
        final_url = self.BASE_URL + endpoint + parameters
        response = requests.get(final_url).json()
        self.remaining = response['remaining']
        self.deck_id = response['deck_id']

    def draw_a_card(self, count=1):
        endpoint = f'/deck/{self.deck_id}/draw/'
        parameters = '?' + 'count=' + str(count)
        final_url = self.BASE_URL + endpoint + parameters
        response = requests.get(final_url).json()
        self.remaining = response['remaining']
        return response['cards']


class Player:

    def __init__(self, name='Banca'):
        self.name = name
        self.game_score = 0
        self.ace_counter = 0
        self.hand = []
        self.matches = []
        self.win = 0
        self.turn_over = False

    def show_hand(self, text = False, mock = False, audible = False):
        if text and not audible:
            card_codes = [('10' if card[0]['code'][0] == '0' else card[0]['code'][0]) +
                          self.get_card_suit(card[0]['code'][1]) for card in self.hand]
            if mock and self.name == "Banca":
                card_codes[-1] = '?'
            ret = ", ".join(card for card in card_codes)

        elif audible:
            card_codes = [('10' if card[0]['code'][0] == '0' else self.get_card_name(card[0]['code'][0])) +
                          self.get_audible_suit(card[0]['code'][1]) for card in self.hand]
            if mock and self.name == "Banca":
                card_codes[-1] = 'carta fechada'
            ret = ", ".join(card for card in card_codes)
            ret += '.'
        else:
            count = len(self.hand)
            imgs_loader = [Image.open(requests.get(card[0]['image'], stream=True).raw).convert("RGB") for card in self.hand]
            card_labels = [self.get_value(card_value=card[0]['value']) for card in self.hand]
            score = str(self.get_game_score())
            if mock and self.name == "Banca":
                imgs_loader[-1] = Image.open('b0C.png').convert("RGB")
                card_labels[-1] = '?'
                score = '?'
            fig = plt.figure(figsize=(count, 1.5))
            for idx in range(len(card_labels)):
                ax = fig.add_subplot(1, count, idx+1, xticks=[], yticks=[])
                ax.axis('off')
                plt.imshow(imgs_loader[idx])
            fig.suptitle(f'{self.name}: {score} Pontos')
            plt.tight_layout(pad=0.1)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            ret = buf
        return ret

    def set_game_score(self, card_code):
        if card_code == "ACE":
            self.ace_counter += 1
        else:
            self.game_score += self.get_value(card_code)

    def get_value(self, card_value = None):
        values = {"2": 2,  "3": 3 , "4":4, "5":5,
                  "6":6, "7": 7,"8": 8, "9" : 9, "10": 10,
                  "JACK": 10, "QUEEN": 10, "KING": 10, "ACE": 11}
        return values[card_value]

    def get_card_suit(self, card_suit = None):
        if card_suit == 'S':
            return '♠'
        if card_suit == 'H':
            return '♥'
        if card_suit == 'C':
            return '♣'
        if card_suit == 'D':
            return '♦'

    def get_card_name(self, card = None):
        if card == 'A':
            return 'Ás'
        if card == 'J':
            return 'Valete'
        elif card == 'Q':
            return 'Dãma'
        elif card == 'K':
            return 'Rei'
        else:
            return card

    def get_audible_suit(self, card_suit = None):
        if card_suit == 'S':
            return ' de espadas'
        if card_suit == 'H':
            return ' de copas'
        if card_suit == 'C':
            return ' de paus'
        if card_suit == 'D':
            return ' de ouros'

    def get_game_score(self):
        if self.ace_counter == 0:
            return self.game_score
        possible_values = set()

        # We now calculate all the possible values combinations of the cards + aces
        for i in range(self.ace_counter + 1):
            possible_values.add(self.game_score + (i * 11) + ((self.ace_counter - i) * 1))

        possible_values_list = list(possible_values)
        # Sort the list so that we can later on work with returning the first/last element of a list without checking actual values again
        possible_values_list.sort()

        # Split up the results into two list for easier handling
        lower_21 = [i for i in possible_values_list if i <= 21]
        bigger_21 = [i for i in possible_values_list if i > 21]

        # If we have an ace, we want to return the biggest value below 21 (is possible).
        if len(lower_21) >= 1:
            return lower_21[-1]

        # If there is no such value we want to return the lowest value above 21
        if len(bigger_21) >= 1:
            return bigger_21[0]

    def draw_from_deck(self, deck:Deck()):
        card = deck.draw_a_card(1)
        self.hand.append(card)
        self.set_game_score(card[0]['value'])

    def busted(self):
        score = self.get_game_score()
        return score > 21

    def new_hand(self):
        self.game_score = 0
        self.ace_counter = 0
        self.hand = []
        self.turn_over = False


    def amount_of_cards(self):
        return len(self.hand)

    def has_blackjack(self):
        return self.get_game_score() == 21 and self.amount_of_cards == 2

    def has_21(self):
        return self.get_game_score() == 21


    def stats(self, audible=False):

        if len(self.matches) > 0:
            win_percent = self.win/len(self.matches)
            bar = generate_bar_chart(win_percent*100)
            if audible:
                template = 'Estatísticas do jogador.\n{}.\nQuantidade de Jogos: {}.\nNúmero de Vitórias: {}.\nPorcentagem de vitórias: {} por cento.'

                template = template.format(self.name.strip(), len(self.matches), self.win, int(win_percent*100))
            else:
                template = 'Estatísticas do jogador <b>{}</b> 📊:\n\n<b>Jogos:</b> {}\n<b>Vitórias:</b> {}\n\n{}\n\n<b>Porcentagem de vitórias:</b> {:.2%}\n'
                template = template.format(self.name, len(self.matches), self.win, bar, win_percent)
            return template
        else:
            return "Sem estatísticas. \nNenhuma partida concluída."

    def list_matches(self):
        ret = ''
        for idx, match in enumerate(self.matches):
            ret = ret + str(idx+1) + 'º - '
            if match['win'] == 1:
                ret = ret + "Vitória - "
            elif match['win'] == 0:
                ret = ret + "Derrota - "
            else:
                ret = ret + "Empate - "
            ret = ret + str(match['score']) + " Pontos.\n"
        return ret

class BlackJackGame:
    def __init__(self):
        self.list_won = []
        self.list_tie = []
        self.list_lost = []
        self._current_player = 0
        self.players = []
        self.running = False
        self.dealer = Player("Banca")
        self.players.append(self.dealer)
        self.players.append(Player("Você "))
        self.deck = Deck()
        self.evaluated = False

    def start(self, audible):

        if self.deck.remaining < 4:
            self.deck = Deck()
        self.running = True
        #enable audible conversation
        self.audible = audible
        #empty piles
        for player in (self.players):
            player.new_hand()

        # Give every player and the dealer 2 cards
        for player in (self.players) * 2:
            player.draw_from_deck(self.deck)
        self._current_player = 1
        resp = "Cartas na mesa: \n"
        for player in self.players:
            score = " " + str(player.get_game_score()) if not audible else " está com " + str(player.get_game_score())
            if player.has_blackjack() :
                score = "<b>BlackJack! </b>" + score if not audible else "BlequeJeque!" + score
            if player.name == "Banca":
                score = " ?? " if not audible else " está com "
            if audible:
                resp = resp + player.name + score + (" Pontos. Suas cartas são " if player.name != 'Banca' else "") + player.show_hand(text=True, mock=True, audible=audible) + '\n'
            else:
                resp = resp + player.name + score + (" Pontos. " if player.name != 'Banca' else "") + '\n\n'
        resp = resp + "Mais uma carta ou parar?"
        self.evaluated = False
        
        if self.get_current_player().has_blackjack():
            self.dealers_turn(audible)
            return self.evaluate(audible=audible)
        else:
            return resp, self.table(mock=True, text=None)

    def get_current_player(self):
        return self.players[self._current_player]

    def draw_card(self, audible):
        # Players turn
        player = self.players[self._current_player]
        if player.name == "Banca":
            self.dealers_turn(audible)
        else:
            player.draw_from_deck(self.deck)
            if player.busted() or player.has_21():
                player.turn_over = True
                self._current_player = 0
                self.dealers_turn(audible)
                return self.evaluate(audible)
            else:
                resp = "Seu Turno: \n\n"
                for player in self.players:
                    score = ": " + str(player.get_game_score()) if not audible else " está com " + str(player.get_game_score())
                    if player.name == "Banca":
                        score = " ??" if not audible else " está com "
                    else:
                        if player.has_blackjack() :
                            score = "<b>BlackJack! </b>" + score if not audible else "BlequeJeque!" + score
                        if player.busted():
                            score = "<b>Estourou! </b>" + score if not audible else "Estourou com " + score 
                    if audible:
                        resp = resp + player.name + score + (" Pontos. " if player.name != 'Banca' else "") + player.show_hand(text=True, mock=True, audible=audible) + '\n'
                    else:
                        resp = resp + player.name + score + (" Pontos. " if player.name != 'Banca' else "") + '\n\n'
        resp = resp + "Mais uma carta ou parar?"
        return resp, self.table(mock = True, text=None)


    def dealers_turn(self, audible):
        if not self.running:
            return "O Jogo deve iniciar antes da vez da Banca"


        while self.dealer.get_game_score() <= 16:
            self.dealer.draw_from_deck(self.deck)

        self.dealer.turn_over = True
        self.evaluate(audible)
        self.running = False



    def stop(self):
        """
        Marks the next player as active player. If all players are finished, go to dealer's turn
        :return:
        """
        if not self.running:
            return "O Jogo não foi iniciado"
        self.get_current_player().turn_over = True
        
        self.running = False



    def evaluate(self, audible): # TODO: adaptar textos para áudio neste método
        """
        Check which player won and which lost.
        :return:
        """
        list_busted = [player for player in self.players if player.busted()]
        list_not_busted = [player for player in self.players if not player.busted()]
        ret = ''

        if self.dealer.busted():
            if len(list_busted) > 1:
                for player in list_busted:
                    if not self.evaluated: player.matches.append({"win": 0, "score": player.get_game_score() })
                    ret = f'Ambos Estouraram! Ninguém venceu!\nVocê: {player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} pontos'
            for player in list_not_busted:
                if not self.evaluated:
                    player.win += 1
                    player.matches.append({"win": 1, "score": player.get_game_score() })
                ret = f'O Vencedor foi você!\nVocê: {player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} pontos. Estourou!'

        elif self.dealer.has_blackjack():
            for player in list_not_busted:
                if player.has_blackjack():
                    if not self.evaluated:
                        player.win += 1
                        player.matches.append({"win": 1, "score": player.get_game_score() })
                    bj = "<b>Blackjack</b> - " if player.has_blackjack() else ""
                    ret =  f'Empatou com {bj}{player.get_game_score()} pontos!'
                else:
                    if not self.evaluated: player.matches.append({"win": 0, "score": player.get_game_score() })
                    ret = f'Você perdeu!\nVocê: {player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} = BlackJack!'
        elif self.dealer.get_game_score() <= 21:
            for player in list_not_busted:
                if player.get_game_score() > self.dealer.get_game_score():
                    if not self.evaluated:
                        player.win += 1
                        player.matches.append({"win": 1, "score": player.get_game_score() })
                    bj = "<b>Blackjack</b> - " if player.has_blackjack() else ""
                    ret = f'O Vencedor foi você!\nVocê: {bj}{player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} pontos.'
                elif player.get_game_score() == self.dealer.get_game_score():
                    if not self.evaluated:
                        player.matches.append({"win": 1, "score": player.get_game_score() })
                        player.win += 1
                    ret = f'Empatou com {player.get_game_score()} pontos!'
                elif player.get_game_score() < self.dealer.get_game_score():
                    if not self.evaluated: player.matches.append({"win": 0, "score": player.get_game_score() })
                    ret = f'Você perdeu!\nVocê: {player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} pontos.'
            for player in list_busted:
                    if not self.evaluated: player.matches.append({"win": 0, "score": player.get_game_score() })
                    ret = f'Você estourou e perdeu!\nVocê: {player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} pontos.'

        self.evaluated = True
        return "Fim da partida. Peça para jogar novamente.", self.table(text=ret)

    def terminate (self):
        #return to same state as a new instance of BlackJackGame
        self.list_won = []
        self.list_tie = []
        self.list_lost = []
        self._current_player = 0
        self.players = []
        self.running = False
        self.dealer = Player("Banca")
        self.players.append(self.dealer)
        self.players.append(Player("Você"))
        self.deck = Deck()

    def table(self, mock = False, text = None):
        imgs_loader = [player.show_hand(mock=mock) for player in self.players]
        size = len(imgs_loader) if not text else len(imgs_loader)+1
        max_hand_count = min(max([len(player.hand) for player in self.players]), 4)
        if max_hand_count < 3:
            dpi = 100
        else:
            dpi = 75

        fig = plt.figure(figsize=(max_hand_count, max_hand_count*size*0.65))
        for idx in range(len(imgs_loader)):
            ax = fig.add_subplot(size, 1, idx+1, xticks=[], yticks=[])
            ax.axis('off')
            plt.imshow(Image.open(imgs_loader[idx]), aspect='auto')
        # fig.suptitle('Cartas na Mesa:')
        if text:
          props = dict(boxstyle='round', facecolor='green', alpha=0.2)
          ax = fig.add_subplot(size, 1, size)
          # place a text box in upper left in axes coords
          ax.text(0.5, 0.5, text, transform=ax.transAxes, fontsize=14,
                  verticalalignment='center', horizontalalignment='center', bbox=props)
          ax.axis('off')
        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=dpi)
        plt.close()
        buf.seek(0)
        ret = base64.b64encode(buf.read()).decode('utf-8')
        return ret

def generate_bar_chart(win_percentage):
    """
    Generate a string of emojis representing a bar (10 chars) that indicates wins vs. losses
    :param win_percentage: The percentage of wins
    :return: Example (55.0%-64.9%) '🏆🏆🏆🏆🏆🏆🔴🔴🔴🔴'
    """
    win_portion = round(win_percentage / 10)
    loss_portion = 10 - win_portion
    return "🏆" * win_portion + "🔴" * loss_portion

class FixSizeOrderedDict(OrderedDict):
    def __init__(self, *args, maxlen=0, **kwargs):
        self._maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        if self._maxlen > 0:
            if len(self) > self._maxlen:
                self.popitem(False)




