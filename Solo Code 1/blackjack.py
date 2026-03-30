import random
def draw_card(hand, deck):
    hand.append(deck.pop()) 


def get_value(hand):
    total = 0
    aces = 0
    for card in hand:
        if card in ["J", "Q", "K"]:
            total += 10
        elif card == "A":
            total += 11
            aces += 1
        else:
            total += int(card)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def show_hands(player_hand, dealer_hand, hide_dealer=False):
    if hide_dealer:
        hidden = ["?"] + dealer_hand[1:]
        print(f"Dealer hand: {hidden}")
    else:
        print(f"Dealer hand: {dealer_hand} (value: {get_value(dealer_hand)})")
    print(f"Player hand: {player_hand} (value: {get_value(player_hand)})")


def player_turn(deck, player_hand):
    while True:
        if get_value(player_hand) > 21:
            break
        choice = input("Hit or stay? ").strip().lower()
        if choice in ["stay", "s"]:
            break
        if choice in ["hit", "h"]:
            draw_card(player_hand, deck)
            print(f"You drew: {player_hand[-1]}")
            print(f"Player hand: {player_hand} (value: {get_value(player_hand)})")
        else:
            print("Please type hit or stay.")
    return player_hand


def dealer_turn(deck, dealer_hand):
    while get_value(dealer_hand) < 17:
        draw_card(dealer_hand, deck)
    return dealer_hand


def determine_winner(player_hand, dealer_hand):
    player_total = get_value(player_hand)
    dealer_total = get_value(dealer_hand)

    if player_total > 21:
        return "Player busts. Dealer wins."
    if dealer_total > 21:
        return "Dealer busts. Player wins."
    if player_total > dealer_total:
        return "Player wins."
    if dealer_total > player_total:
        return "Dealer wins."
    return "Tie game."


def main():
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    player_hand = []
    dealer_hand = []

    random.shuffle(deck)

    draw_card(dealer_hand, deck)
    draw_card(player_hand, deck)
    draw_card(player_hand, deck)

    show_hands(player_hand, dealer_hand, hide_dealer=True)
    player_turn(deck, player_hand)

    if get_value(player_hand) <= 21:
        dealer_turn(deck, dealer_hand)

    print("Final hands:")
    show_hands(player_hand, dealer_hand, hide_dealer=False)
    print(determine_winner(player_hand, dealer_hand))


if __name__ == "__main__":
    main()
