# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
my_hand = None
house_hand = None
my_deck = None
question = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_cards = []
               
    def __str__(self):
        hand_card = ""
        for index in range(len(self.hand_cards)):
            hand_card += str(self.hand_cards[index]) + ' '
        return hand_card
               
    def add_card(self, card):
        return self.hand_cards.append(card)
        
    def get_value(self):
        hand_value = 0
        aces = 0
        for cards in self.hand_cards:
            if cards.get_rank() == 'A':
                aces += 1
            hand_value += VALUES[cards.get_rank()]
            
        if aces > 0 and hand_value + 10 <= 21:
            return hand_value + 10
        else:
            return hand_value
   
    def draw(self, canvas, pos):
        for card in self.hand_cards:
            pos[0] += CARD_CENTER[0] + 40
            card.draw(canvas,pos)
            
        
# define deck class 
class Deck:
    def __init__(self):
        self.game_cards = []
        for suit in SUITS: 
            for rank in RANKS:
                card = Card(suit,rank)
                self.game_cards.append(card)
                
    def shuffle(self):
        random.shuffle(self.game_cards)

    def deal_card(self):
        return self.game_cards.pop()
    
    def __str__(self):
        deck = "" 
        for index in self.game_cards:
            deck += str(index) + ' ' 
        return deck

#define event handlers for buttons
def deal():
    global outcome, in_play
    global my_hand , house_hand , my_deck
    my_hand = Hand()
    house_hand = Hand()
    my_deck = Deck()
    my_deck.shuffle()
    
    my_hand.add_card(my_deck.deal_card())
    my_hand.add_card(my_deck.deal_card())
        
    house_hand.add_card(my_deck.deal_card())
    house_hand.add_card(my_deck.deal_card())
    
    in_play = True
    outcome = ""

def hit():
    global my_hand , my_deck , score , outcome , question , in_play
    
    if in_play == True:
        my_hand.add_card(my_deck.deal_card())
        
        if my_hand.get_value() > 21:
            in_play = False
            outcome = 'You Busted'
            score -= 1

def stand():
    global my_hand , my_deck , outcome
    global house_hand , my_hand , score , in_play
    
    if not in_play:
        return
    
    while house_hand.get_value() < 17:
        house_hand.add_card(my_deck.deal_card())
    
    if house_hand.get_value() > 21:
        in_play = False
        outcome = 'Dealer busted'
        score += 1
    
    elif my_hand.get_value() == house_hand.get_value():
        in_play = False
        outcome = 'Dealer wins'
        score -= 1
        
    elif my_hand.get_value() < house_hand.get_value():
        in_play = False
        outcome = 'Dealer wins'
        score -= 1
        
    elif my_hand.get_value() > house_hand.get_value():
        in_play = False
        outcome = 'Player wins'
        score += 1
               
# draw handler    
def draw(canvas):
    global score , card_hand , outcome , in_play , house_hand 
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (75, 75), 45, 'white')
    canvas.draw_text('Dealer' , (50, 175), 35, 'black')
    canvas.draw_text('Player', (50, 375), 35, 'black')
    canvas.draw_text('Score' + '   ' + str(score), (400, 75), 35, 'black')
    canvas.draw_text(outcome, (250, 175), 30, 'black')
    canvas.draw_text(str(my_hand.get_value()), (150, 375), 30, 'black') 

    if in_play == False:
        canvas.draw_text(str(house_hand.get_value()), (180, 175), 35, 'black')
# draw of the dealer and player cards
    my_hand.draw(canvas,[0,400])
    house_hand.draw(canvas, [0,200])
    
# draw of the facedow card of the  dealer
    if in_play == True:
        canvas.draw_text("Hit or Stand?", [300, 375], 30, 'black')
    else:
        canvas.draw_text("New deal?", [300, 375], 30, 'black')


# draw dealer card down
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [40 + CARD_BACK_SIZE[0], 152 + CARD_BACK_SIZE[1]], CARD_SIZE)
    else:
        house_hand.draw(canvas, [0,200])		
                
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
