import random
import time

high_score = {
    'Easy': (999, 999.99),  # (attempts, time)
    'Medium': (999, 999.99),
    'Hard': (999, 999.99)
}

def welcome_message():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

def select_difficulty():
    difficulties = {
        '1': ("Easy", 10),
        '2': ("Medium", 5),
        '3': ("Hard", 3)
    }

    print("\nPlease select the difficulty level:")
    for k, (name, chances) in difficulties.items():
        print(f"{k}. {name} ({chances} chances)")

    choice = input("\nEnter your choice: ")
    while choice not in difficulties:
        print("Invalid choice. Please select 1, 2, or 3.")
        choice = input("\nEnter your choice: ")

    return difficulties[choice][0], difficulties[choice][1]

def valid_guess():
    while True:
        raw_input = input("\nEnter your guess (or 'hint'): ").strip().lower()
        if raw_input == 'hint':
            return 'hint'
        try:
            guess = int(raw_input)
            if 1 <= guess <= 100:
                return guess
            print("Invalid guess. Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a whole number or 'hint'.")

def provide_hint(target, hints_used):
    print("\nHINT:")
    if hints_used == 0:
        parity = "even" if target % 2 == 0 else "odd"
        print(f"-> The number is {parity}.")
    elif hints_used == 1:
        if target % 3 == 0:
            print("-> The number is divisible by 3.")
        elif target % 5 == 0:
            print("-> The number is divisible by 5.")
        else:
            print("-> The number is not divisible by 3 or 5.")
    else:
        low_bound = max(1, target - random.randint(5, 10))
        high_bound = min(100, target + random.randint(5, 10))
        print(f"-> The number is between {low_bound} and {high_bound}.")

def gameplay(difficulty_level, chances):
    print(f"\nGreat! You have selected the {difficulty_level} difficulty level.")
    print("Let's start the game!")

    random_number = random.randint(1, 100)
    start_time = time.perf_counter()
    attempts = 0
    hints_used = 0

    while attempts < chances:
        user_input = valid_guess()

        if user_input == 'hint':
            provide_hint(random_number, hints_used)
            hints_used += 1
            continue

        attempts += 1
        guess = user_input

        if guess < random_number:
            print(f"Incorrect! The number is greater than {guess}.")
        elif guess > random_number:
            print(f"Incorrect! The number is less than {guess}.")
        else:
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            print("\n" + "="*61)
            print(f"Congratulations! You guessed the correct number in {attempts} attempt(s)!")
            print(f"Time taken: {elapsed_time:.2f} seconds")
            print("="*61 + "\n")

            return elapsed_time, attempts

    print("\n" + "="*61)
    print(f"Better luck next time! The correct number was {random_number}.")
    print("Game Over")
    print("="*61 + "\n")
    return 999.99, 999  # Fixed return order (elapsed_time, attempts)

def show_high_score(elapsed_time, attempts, difficulty_level):
    if attempts == 999:
        return  # Skip score update on loss

    best_attempts, best_time = high_score[difficulty_level]
    new_high_score = (attempts < best_attempts) or (attempts == best_attempts and elapsed_time < best_time)

    if new_high_score:
        print("="*22, "NEW HIGH SCORE", "="*22)
        high_score[difficulty_level] = (attempts, elapsed_time)
        if attempts == best_attempts:
            print(f"New record! You beat the time: {best_time:.2f}s -> {elapsed_time:.2f}s with {attempts} attempt(s)!")
        else:
            print(f"New high score on {difficulty_level}! Only {attempts} attempt(s) in {elapsed_time:.2f} seconds!")
        print("="*61 + "\n")

def main():
    while True:
        welcome_message()
        difficulty_level, chances = select_difficulty()
        elapsed_time, attempts = gameplay(difficulty_level, chances)
        show_high_score(elapsed_time, attempts, difficulty_level)

        print("="*20, "CURRENT HIGH SCORES", "="*20)
        for k, (best_attempts, best_time) in high_score.items():
            if best_attempts == 999:
                print(f"{k} difficulty: No record yet")
            else:
                print(f"{k} difficulty: {best_attempts} attempt(s) in {best_time:.2f}s")
        print("="*61)

        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again not in ('y', 'yes'):
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()