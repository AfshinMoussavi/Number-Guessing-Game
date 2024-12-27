from colorama import Fore, Back, Style
import random, sqlite3, time
from datetime import datetime

# Database
conn = sqlite3.connect("game.db")
cursor = conn.cursor()
    
cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        attempts INTEGER NOT NULL,
        time_taken REAL NOT NULL, 
        date_played TEXT NOT NULL
    )
    """)
conn.commit()
    
def add_record(username, difficulty, attempts, time_taken):
    """Adds a new record to the database.

    Args:
        username (str): Name of the user playing the game.
        difficulty (str): Difficulty level (Easy, Medium, Hard).
        attempts (int): Number of attempts taken to guess the number.
        time_taken (float): Time taken to guess the number in seconds.
    """
    
    date_played = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO records (username, difficulty, attempts, time_taken, date_played)
    VALUES (?, ?, ?, ?, ?)
    """, (username, difficulty, attempts, time_taken,date_played))
    conn.commit()
    
def get_best_record(difficulty):
    """Fetches the best record for a specific difficulty level.

    Args:
        difficulty (str): Difficulty level (Easy, Medium, Hard).

    Returns:
        str: Information about the best record or a message if no records exist.
    """
    
    cursor.execute("""
    SELECT username, attempts, time_taken, date_played 
    FROM records 
    WHERE difficulty = ? 
    ORDER BY attempts ASC 
    LIMIT 1
    """, (difficulty,))
    record = cursor.fetchone()
    if record:
        return f"Best Record for {difficulty}: User: {record[0]}, Attempts: {record[1]}, Time: {record[2]:.2f} seconds, Date: {record[3]}"
    return f"No records found for {difficulty} difficulty."


def play_again():
    """Asks the user if they want to play the game again.

    Returns:
        bool: True if the user wants to play again, False otherwise.
    """
    
    check = input('you wanna play?('+ Fore.GREEN + 'yes' + Style.RESET_ALL + '/' + Fore.RED + 'no' + Style.RESET_ALL + '): ')
    return check.strip().lower() == 'yes'
        

if __name__ == "__main__":
    """Main game logic for the Number Guessing Game."""

    # Game Source 
    print(Back.BLUE + '==============================================' + Style.RESET_ALL)
    print("""Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.\nYou have to guess the correct number.""")
    print()
    username = input('please enter your username: ')

    while True:
        print(f'Please select the difficulty level(1,2,3):')
        print(f'1  =>  Easy (10 chances)')
        print(f'2  =>  Medium (5 chances)')
        print(f'3  =>  Hard (3 chances)')
        print(f'4  =>  show top ranking')
        try:
            difficulty_level = int(input(f'Enter your choice: '))
            if difficulty_level == 4:
                """Shows the top-ranking players for all difficulty levels."""
                print(get_best_record('Easy'))
                print(get_best_record('Medium'))
                print(get_best_record('Hard'))
                check = play_again()
                if check:
                    continue
                else:
                    print(Fore.BLUE + 'Goodbye!' + Style.RESET_ALL)
                    break
                    
            else:
                """Handles the game logic based on the selected difficulty level."""
                response = {1:['Easy',10], 2:['Medium',5], 3:['Hard',3]}
                print(f'Great! You have selected the {response[difficulty_level][0]} difficulty level.\n')
                count_guess = response[difficulty_level][1]
                random_number = random.randint(1,100)
                flag = False
                start_time = time.time()
                for attempt in range(1,count_guess+1):
                    guess_number = int(input('Enter your guess: '))
                    if guess_number == random_number:
                        end_time = time.time()
                        time_taken = end_time - start_time
                        print(Fore.GREEN + 'Congratulations!' + Style.RESET_ALL +
                              f' You guessed the correct number in {attempt} attempts.\nTime taken: {time_taken} seconds.')
                        add_record(username, response[difficulty_level][0], attempt, time_taken)
                        flag = True
                        break
                    else:
                        if guess_number > random_number:
                            print(Fore.RED + 'Incorrect!'+ Style.RESET_ALL + f' The number is less than {guess_number}.')
                        else:
                            print(Fore.RED + 'Incorrect!'+ Style.RESET_ALL + f' The number is greater than {guess_number}.')
                if flag:
                    print('You win 😀')
                else:
                    print('you lost ☹️')
                
                check = play_again()
                if check:
                    continue
                else:
                    print(f'good luck ^^')
                    break
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter a number between 1 and 4." + Style.RESET_ALL)
    conn.close()

