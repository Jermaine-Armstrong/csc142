import pygame
import pygwidgets
from Constants import *
from Deck import *


class Game:
    DEALER_TOP = 90
    PLAYER_TOP = 320
    CARD_LEFT = 90
    CARD_OFFSET = 110
    BLACKJACK_VALUES = {
        'Ace': 11,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10
    }

    def __init__(self, window):
        self.window = window
        self.oDeck = Deck(window, Game.BLACKJACK_VALUES)
        self.messageText = pygwidgets.DisplayText(
            window, (40, 510), '', width=920, justified='center',
            fontSize=32, textColor=WHITE
        )
        self.dealerLabel = pygwidgets.DisplayText(
            window, (40, 25), '', fontSize=30, textColor=WHITE
        )
        self.playerLabel = pygwidgets.DisplayText(
            window, (40, 255), '', fontSize=30, textColor=WHITE
        )
        self.resultLabel = pygwidgets.DisplayText(
            window, (360, 25), '', width=600, justified='center',
            fontSize=34, textColor=WHITE
        )
        self.winnerSound = pygame.mixer.Sound('sounds/ding.wav')
        self.loserSound = pygame.mixer.Sound('sounds/loser.wav')
        self.pushSound = pygame.mixer.Sound('sounds/push.wav')
        self.cardShuffleSound = pygame.mixer.Sound('sounds/cardShuffle.wav')
        self.cardFlipSound = pygame.mixer.Sound('sounds/cardFlip.wav')
        self.reset()

    def reset(self):
        self.oDeck.shuffle()
        self.cardShuffleSound.play()
        self.playerCards = []
        self.dealerCards = []
        self.roundOver = False
        self.result = ''
        self.deal_card(self.playerCards, True)
        self.deal_card(self.dealerCards, False)
        self.deal_card(self.playerCards, True)
        self.deal_card(self.dealerCards, True)
        self.messageText.setValue('Hit to take another card or Stay to hold.')
        self.update_display_text()

    def deal_card(self, hand, reveal):
        card = self.oDeck.getCard()
        if reveal:
            card.reveal()
        else:
            card.conceal()
        hand.append(card)
        self.position_cards()
        self.cardFlipSound.play()
        return card

    def position_cards(self):
        for index, card in enumerate(self.dealerCards):
            card.setLoc((Game.CARD_LEFT + (index * Game.CARD_OFFSET), Game.DEALER_TOP))
        for index, card in enumerate(self.playerCards):
            card.setLoc((Game.CARD_LEFT + (index * Game.CARD_OFFSET), Game.PLAYER_TOP))

    def get_hand_value(self, hand):
        total = 0
        aces = 0
        for card in hand:
            total += card.getValue()
            if card.getRank() == 'Ace':
                aces += 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def update_display_text(self):
        player_total = self.get_hand_value(self.playerCards)
        self.playerLabel.setValue('Player: ' + str(player_total))
        if self.roundOver:
            dealer_text = 'Dealer: ' + str(self.get_hand_value(self.dealerCards))
        else:
            dealer_text = 'Dealer: ?'
            if len(self.dealerCards) > 1:
                dealer_text = 'Dealer shows: ' + str(self.dealerCards[1].getValue())
        self.dealerLabel.setValue(dealer_text)
        self.resultLabel.setValue(self.result)

    def reveal_dealer_cards(self):
        for card in self.dealerCards:
            card.reveal()

    def finish_round(self):
        self.roundOver = True
        self.reveal_dealer_cards()
        player_total = self.get_hand_value(self.playerCards)
        dealer_total = self.get_hand_value(self.dealerCards)
        if player_total > 21:
            self.result = 'Dealer wins'
            self.messageText.setValue('You busted.')
            self.loserSound.play()
        elif dealer_total > 21:
            self.result = 'Player wins'
            self.messageText.setValue('Dealer busted.')
            self.winnerSound.play()
        elif player_total > dealer_total:
            self.result = 'Player wins'
            self.messageText.setValue('Your hand was closer to 21.')
            self.winnerSound.play()
        elif dealer_total > player_total:
            self.result = 'Dealer wins'
            self.messageText.setValue('Dealer had the better hand.')
            self.loserSound.play()
        else:
            self.result = 'Tie game'
            self.messageText.setValue('Both hands had the same total.')
            self.pushSound.play()
        self.update_display_text()

    def hit(self):
        if self.roundOver:
            return True
        self.deal_card(self.playerCards, True)
        if self.get_hand_value(self.playerCards) > 21:
            self.finish_round()
        else:
            self.update_display_text()
        return self.roundOver

    def stay(self):
        if self.roundOver:
            return True
        self.reveal_dealer_cards()
        while self.get_hand_value(self.dealerCards) < 17:
            self.deal_card(self.dealerCards, True)
        self.finish_round()
        return True

    def draw(self):
        for card in self.dealerCards:
            card.draw()
        for card in self.playerCards:
            card.draw()
        self.dealerLabel.draw()
        self.playerLabel.draw()
        self.resultLabel.draw()
        self.messageText.draw()
