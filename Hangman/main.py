from random import randint
import string
import unicodedata

## WORD LIST

short_words = []
medium_words = []
long_words = []
with open(r"C:\Users\jerem\Downloads\liste_francais\liste_francais.txt","r") as file:
    lines = file.readlines()
    for word in lines:
        word = word.strip().lower()
        word = unicodedata.normalize('NFKD',word)
        word  = "".join([c for c in word if not unicodedata.combining(c)])
        if len(word) < 5:
            short_words.append(word)
        elif len(word) < 8:
            medium_words.append(word)
        else:
            long_words.append(word)

## Creates the variables we need

still_wanna_play = True

## Game
while still_wanna_play:
    game_over = False
    has_won = False
    while True:
        word_size_check = input("\nChoose your difficulty.\nType 's' for a short word, 'm' for a medium one and 'l' for a large one ").lower()
        if word_size_check in ['s','m','l'] and len(word_size_check) ==1:
            word_size = word_size_check
            break

    if word_size == 's':
        list_of_words = short_words
    elif word_size == "m":
        list_of_words = medium_words
    else:
        list_of_words = long_words


    num_possible_words = len(list_of_words)
    lives_left = 8
    chosen_word = list_of_words[randint(0,num_possible_words-1)]
    len_chosen_word = len(chosen_word)

    ##Creates the display word
    word_found = []
    for letter in chosen_word:
        word_found += '_'
    letter_guessed_total = 0

    while not game_over:
        print(f"Here's the {len_chosen_word} letter word to guess {''.join(word_found)}. \nLives left: {lives_left}")
        
        ## Checks that user inputs only a single letter
        while True:
            guess_check = (input("\nGuess a single letter. (no accents) ")).lower()
            if len(guess_check) == 1 and guess_check in string.ascii_letters:
                guess = guess_check
                break
            else:
                print('Please enter only a letter')

        is_letter_in_word = False
        letter_checked = 0
        for letter in chosen_word:
            if guess == letter:
                word_found[letter_checked] = guess
                letter_guessed_total +=1
                is_letter_in_word = True
                if letter_guessed_total == len_chosen_word:
                    game_over = True
                    has_won = True
            letter_checked +=1
        if not is_letter_in_word:
            print(f"\nNo, the letter {guess} is not in the word. Losing a life")    
            lives_left -= 1
            if lives_left == 0:
                game_over = True


    if has_won:
        print(f"\nCongrats, you've found the word {chosen_word}")
    else:
        print(f"\nSorry, you've lost. The word to find was {chosen_word} ")
    
    while True:
        decision_to_continue = input("\nDo you want to play another game? 'y' or 'n' ").lower()
        if decision_to_continue == 'n':
            still_wanna_play = False
            break
        elif decision_to_continue == 'y':
            break
        else:
            True
        