import requests
import io
import matplotlib.pyplot as plt
from PIL import Image
import base64


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
        count = len(self.hand)
        imgs_loader = [Image.open(requests.get(card[0]['image'], stream=True).raw).convert("RGB") for card in self.hand]
        card_labels = [self.get_value(card_value=card[0]['value']) for card in self.hand]
        score = str(self.get_game_score())
        if mock and self.name == "Banca":
            imgs_loader[-1] = Image.open('b0C.png').convert("RGB")
            card_labels[-1] = '?'
            score = '?'

        fig = plt.figure(figsize=(count, 2))
        for idx in range(len(card_labels)):
            ax = fig.add_subplot(1, count, idx+1, xticks=[], yticks=[])
            ax.set_title(card_labels[idx])
            fig.suptitle(f'{self.name}: {score}', horizontalalignment='right')
            plt.imshow(imgs_loader[idx])
        buf = io.BytesIO()
        # alternative buf = StringIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        ret = base64.b64encode(buf.read()).decode('utf-8')
        # alternative: ret = send_file(img, mimetype='image/png')
        if text:
            card_codes = [('10' if card[0]['code'][0] == '0' else card[0]['code'][0]) +
                          self.get_card_suit(card[0]['code'][1]) for card in self.hand]
            if mock and self.name == "Banca":
                card_codes[-1] = '?'
            ret = ", ".join(card for card in card_codes)
        if audible:
            card_codes = [('10' if card[0]['code'][0] == '0' else self.get_card_name(card[0]['code'][0])) +
                          self.get_audible_suit(card[0]['code'][1]) for card in self.hand]
            if mock and self.name == "Banca":
                card_codes[-1] = 'carta fechada'
            ret = ", ".join(card for card in card_codes)
            ret += '.'
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
        labels = {"2": 2,  "3": 3 , "4":4, "5":5,
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
            return 'As'
        if card == 'J':
            return 'Valete'
        elif card == 'Q':
            return 'Dama'
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

    def stats(self):
        if len(self.matches) > 0:
            win_percent = self.win/len(self.matches)
            bar = generate_bar_chart(win_percent*100)
            template = 'Aqui estão suas estatísticas 📊:\n\n<b>Jogos:</b> {}\n<b>Vitórias:</b> {}\n\n{}\n\n<b>Porcentagem de vitórias:</b> {:.2%}\n'
            template = template.format(len(self.matches), self.win, bar, win_percent)
            return template
        else:
            return "Sem estatísticas. \nNenhuma partida concluída."

    def list_matches(self):
        ret = ''
        for idx, match in enumerate(self.matches):
            ret = ret + str(idx+1) + 'º - '
            ret = ret + "Vitória - " if match['win'] == 1 else ret + "Derrota - "
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

        if self.running:
            raise Exception('O Jogo já foi iniciado anteriormente')
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

        resp = "Cartas na mesa: \n" + "\n".join("<b>"+player.name +": </b> "+ player.show_hand(text=True, mock=True, audible=audible) for player in self.players) + "\n"
        self.evaluated = False
        if self.get_current_player().has_blackjack():
            self.dealers_turn()
        return resp

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
                resp = self.dealers_turn(audible)
            else:
                resp = "Seu Turno: \n"
                for player in self.players:
                    score = " " + str(player.get_game_score())
                    if player.has_blackjack() :
                        score = "<b>BlackJack!</b>" + score
                    if player.busted():
                        score = "<b>Estourou!</b>" + score
                    if player.name == "Banca":
                        score = " xx"
                    resp = resp + player.name + " está com " + score + " Pontos. " + player.show_hand(text=True, mock=True, audible=audible) + '\n'
                resp = resp + "Mais uma carta ou parar?"
        return resp

    def dealers_turn(self, audible):
        if not self.running:
            raise Exception("O Jogo deve iniciar antes da vez da Banca")

        while self.dealer.get_game_score() <= 16:
            self.dealer.draw_from_deck(self.deck)

        self.dealer.turn_over = True
        # self.dealer.show_hand(text=True)

        resp = "Turno da Banca: \n"
        for player in self.players:
            score = " " + str(player.get_game_score())
            if player.has_blackjack():
                score = " <b>BlackJack!</b>" + score
            if player.busted():
                score = " <b>Estourou!</b>" + score
            resp = resp + player.name + score + " Pontos. " + player.show_hand(text=True, audible=audible) + '\n'
        self.evaluate(audible)
        self.running = False
        return resp + "\n\n" + self.players[1].stats()

    def stop(self):
        """
        Marks the next player as active player. If all players are finished, go to dealer's turn
        :return:
        """
        if not self.running:
            raise Exception("O Jogo não foi iniciado")
        self.get_current_player().turn_over = True
        # self.evaluate()
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
                ret = f'Vencedor foi você!\nVocê: {player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} pontos. Estourou!'

        elif self.dealer.has_blackjack():
            for player in list_not_busted:
                if player.has_blackjack():
                    if not self.evaluated:
                        player.win += 1
                        player.matches.append({"win": 1, "score": player.get_game_score() })
                    bj = "<b>Blackjac</b> - " if player.has_blackjack() else ""
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
                    ret = f'Vencedor foi você!\nVocê: {bj}{player.get_game_score()} pontos.\nBanca: {self.dealer.get_game_score()} pontos.'
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

        ret = ret + '\n\n' + self.players[1].stats() +  "\n\nJogo Parado. Peça para jogar novamente."
        self.evaluated = True
        return ret

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

def generate_bar_chart(win_percentage):
    """
    Generate a string of emojis representing a bar (10 chars) that indicates wins vs. losses
    :param win_percentage: The percentage of wins
    :return: Example (55.0%-64.9%) '🏆🏆🏆🏆🏆🏆🔴🔴🔴🔴'
    """
    win_portion = round(win_percentage / 10)
    loss_portion = 10 - win_portion
    return "🏆" * win_portion + "🔴" * loss_portion





