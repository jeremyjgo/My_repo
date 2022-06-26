### The objective is to guess a number between 1 and 100
from random import randint

DIFFICULTIES = {
    'easy':10,
    'medium':8,
    'hard':6
}

print("The objective is to guess a random number between 1 and 100")
game_on = True
still_wanna_play = True

def guess_number(number_guessed, number_to_find, lives):
    if number_guessed == number_to_find:
        print(f"Congrats, you've found the number {number_to_find}!")
        return False
    else:
        if number_guessed > number_to_find:
            print("Lower")
        else:
            print("Higher")
        lives -=1
        print(f"lives left: {lives}\n")
        if lives < 0:
            print("Sorry, you've lost")
            return False
        else:
            return True
        


while still_wanna_play:
    difficulty_input = input("Choose a difficulty : 'easy', 'medium', or 'hard' ").lower()
    while True:
        if difficulty_input in DIFFICULTIES:
            break
        else:
            continue
    
    number_to_guess = randint(1,100)
    while game_on:
        lives_left = DIFFICULTIES[difficulty_input]
        guessed_number = int(input("\nEnter a number between 1 and 100 "))
        game_on = guess_number(number_guessed=guessed_number, number_to_find=number_to_guess, lives=lives_left)
    decision_to_continue = input("Do you want to keep playing? 'yes' or 'no'? ")
    if decision_to_continue == 'yes':
        still_wanna_play = True
    else:
        still_wanna_play = False
        


print("Thank you for playing")

