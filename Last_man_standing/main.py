 # 100 people are sat in order around a table.
 # Person 1 is given a gun and is going to kill the first living person on its left (person2).
 # Then he passes the gun to the next living person on the right.
 # It continues until only one person is alive.
 # Who is it ?

inital_candidates = int(input("How many players in the game?"))
people_alive = [x for x in range(1,inital_candidates+1)]
x = 0
num_rounds = 1
# x is the shooter

while len(people_alive) > 1: 
    # While we have more than one person alive, we keep going
    if people_alive[x] == people_alive[-1]:
        # If the shooter is the one with the last number of those alive before the shoot, 
        # he needs to shoot the first person alive in the list
        del people_alive[0]
        # The shooter becomes the first person alive in the list
        x = 0
        num_rounds = num_rounds + 1
    else: 
        del people_alive[x+1]
        if people_alive[x] == people_alive[-1]:
            # If the shooter is the one with the last number of those alive after the shoot, 
            # He needs to pass the gun to the first person in the list
            x = 0
            num_rounds = num_rounds + 1
        else:
            x = x + 1

print(f"Out of {inital_candidates} initial candidates, {people_alive} is the last person standing after {num_rounds} rounds")
