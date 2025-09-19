"""
Have a look at the script called 'human-guess-a-number.py' (in the same folder as this one).

Your task is to invert it: You should think of a number between 1 and 100, and the computer 
should be programmed to keep guessing at it until it finds the number you are thinking of.

At every step, add comments reflecting the logic of what the particular line of code is (supposed 
to be) doing. 
"""

def guess_my_number():
    # I set up the lowest and highest possible values
    low_bound = 1
    low_bound = 1
    high_bound = 100
    guess = (low_bound + high_bound) // 2   # starting with midpoint
    print(f"My first attempt is: {guess}\n")
    
    # Keep looping until I actually guess the right number
    while True:
        feedback = input("Is my guess too low (L), too high (H), or correct (C)? ").lower()

        if feedback in ('l', 'low', 'too low'):
            # If I’m too low, I know the number must be higher,
            # so I bump the lower bound up and guess the new middle
            low_bound = guess + 1
            guess = (low_bound + high_bound) // 2
            print(f"Okay, let me try a higher number: {guess}")
        elif feedback in ('h', 'high', 'too high'):
            # If I’m too high, I lower the upper bound
            # and again go for the new middle
            high_bound = guess - 1
            guess = (low_bound + high_bound) // 2
            # If the user says I got it right, I can stop
            print(f"Got it, I’ll try a lower number: {guess}")
        elif feedback in ('c', 'correct'):
            print(f"Nice! I figured it out — your number is {guess}.")
            break
        else:
            # If the user types something else, I remind them of valid options
            print("Please answer with L, H, or C.")

guess_my_number()