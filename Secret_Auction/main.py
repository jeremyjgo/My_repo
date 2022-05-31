import os

more_players = True
bidders = []

def add_new_bidder(name, bid):
    bidders.append({
        'name':name,
        'bid':bid
    })
    more_bidders = input('Any new players? "yes or "no"')
    if more_bidders == 'yes':
        os.system('cls')
        return True
    else:
        return False


def check_bid(bid):
    if bid is int:
        return True
    else:
        return False

def check_winner(players):
    max_bid = 0
    winner = ''
    player_idx = 0
    for player in players:
        if players[player_idx]['bid'] > max_bid:
            max_bid = players[player_idx]['bid']
            winner = players[player_idx]['name']
        player_idx +=1
    return winner, max_bid


while more_players:
    bidder = input('Enter your name ')
    #https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
    while True:
        try:
            bid_entered = int(input('Place your bid € '))
        except ValueError:
            print("Enter only a number")
            continue    
        else:
            break
    more_players = add_new_bidder(name=bidder,bid=bid_entered)
winner, max_bid = check_winner(bidders)
print(f"The winner is {winner} with a bid of €{max_bid} ")