import string
import random

valid_caracters = []
for l in string.ascii_lowercase:
    valid_caracters.append(l)
for d in string.digits:
    valid_caracters.append(d)
for p in string.punctuation:
    valid_caracters.append(p)
valid_caracters.append(' ')
max_index = len(valid_caracters) - 1
still_wanna_play = True

def encode(word_to_encode):
    random.shuffle(valid_caracters)
    encoded_word = ''
    step_encode = []
    index_encode = []
    for letter in word_to_encode:
        letter_true_index = 0
        # index de ma vraie lettre ds valid caracter
        # une lettre du mot à la fois
        for l in valid_caracters:
            # une lettre de la liste de caractères à la fois
            if letter == l:
                letter_step = random.randint(0,max_index)
                step_encode.append(letter_step)
                # le décalage entre ma lettre et ma lettre encodée dans la liste
                letter_coded_index = (letter_true_index + letter_step) % max_index
                # dans la liste de valid_caracters, la place de ma lettre encodée
                index_encode.append(letter_coded_index)
                encoded_word += valid_caracters[letter_coded_index]
            letter_true_index +=1
    print(f"The encoded word is {encoded_word}")
    return encoded_word, index_encode, step_encode

def decode(word_to_decode,index,step):
    decoded_word = ''
    letter_pos = -1
    for letter in word_to_decode:
        letter_pos +=1
        letter_coded_index = index[letter_pos]
        letter_step = step[letter_pos]
        letter_true_index = (letter_coded_index - letter_step + max_index)%max_index
        decoded_word += valid_caracters[letter_true_index]
    print(f"\nThe decoded word is {decoded_word}")

while still_wanna_play:
    print('\n\nWelcome to the Cypher Project !!\n')
    encoding_word = input("Type the word you want to encode? ").lower()


    encoded_word, index_encode, step_encode = encode(word_to_encode=encoding_word)

    decode(word_to_decode=encoded_word, index=index_encode, step=step_encode)
    decision_to_continue = input("Do you want to keep playing? 'y' or 'n' ")
    if decision_to_continue == 'n':
        still_wanna_play = False

