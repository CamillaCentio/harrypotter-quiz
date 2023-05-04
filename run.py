import random
import re
import json
import gspread
from google.oauth2.service_account import Credentials

# Define the questions and answers
categories = {
    "1": {"name": "General Knowledge", "questions": [
        "What is the name of Harry Potter's owl?",
        "What is the name of the Hogwarts gamekeeper?",
        "What is the name of the magical creature that can transform into a person's worst fear?",
        "Who killed Dumbledore?",
        "What is the name of the Weasley family's pet rat?",
        "What is the name of the ghost who haunts the girls' bathroom?",
        "What is the name of the werewolf who teaches Defense Against the Dark Arts in Harry's third year?",
        "What is the name of the house elf who serves the Malfoy family?",
        "What is the name of Harry's godfather?",
        "What is the name of the wizarding prison where Sirius Black was held?"
    ], "answers": [
        "Hedwig",
        "Hagrid",
        "Boggart",
        "Severus Snape",
        "Scabbers",
        "Moaning Myrtle",
        "Remus Lupin",
        "Dobby",
        "Sirius Black",
        "Azkaban"
    ]},
    "2": {"name": "Hogwarts Houses", "questions": [
        "What is the animal mascot of Hufflepuff house?",
        "What is the ghost mascot of Ravenclaw house?",
        "What is the common room password for Gryffindor house in Harry's first year?",
        "What is the founder of Slytherin house's first name?",
        "What is the animal mascot of Ravenclaw house?",
        "What is the animal mascot of Gryffindor house?",
        "What is the ghost mascot of Hufflepuff house?",
        "What is the founder of Hufflepuff house's first name?",
        "What is the common room password for Slytherin house in Harry's second year?",
        "What is the animal mascot of Slytherin house?"
    ], "answers": [
        "Badger",
        "Grey Lady",
        "Caput Draconis",
        "Salazar",
        "Eagle",
        "Lion",
        "Fat Friar",
        "Helga",
        "Pureblood",
        "Serpent"
    ]},
    "3": {"name": "Magical Creatures", "questions": [
        "What is the name of Hagrid's three-headed dog?",
        "What is the name of the half-eagle, half-horse creature that serves as the Hogwarts gamekeeper?",
        "What is the name of the magical creature that can transform into a person's worst fear?",
        "What is the name of the giant spider that lives in the Forbidden Forest?",
        "What is the name of the snake that Harry can speak to?",
        "What is the name of the dragon that Hagrid hatches from an egg?",
        "What is the name of the giant squid that lives in the Hogwarts lake?",
        "What is the name of the ghost who haunts the Hogwarts castle and is also known as the Bloody Baron?",
        "What is the name of the creature that is half-man, half-goat and is known for its love of wine and parties?",
        "What is the name of the creature that is a small, furry ball with wings that can fly?"
    ], "answers": [
        "Fluffy",
        "Fang",
        "Boggart",
        "Aragog",
        "Nagini",
        "Norbert",
        "The Giant Squid",
        "The Bloody Baron",
        "The Satyr",
        "The Golden Snidget"
    ]},
    "4": {"name": "Spells", "questions": [
        "What spell does Harry use to disarm opponents?",
        "What spell does Ron use to levitate objects?",
        "What spell does Hermione use to create a Patronus?",
        "What spell does Voldemort use to kill?",
        "What spell does Snape use to prevent Harry from talking during his detention?",
        "What spell does Harry use to summon his broomstick in his first year at Hogwarts?",
        "What spell does Professor McGonagall use to bring the Hogwarts statues to life during the Battle of Hogwarts?",
        "What spell does Hermione use to repair Harry's glasses in the Sorcerer's Stone?",
        "What spell does Snape use to clear up Neville's potion in the Sorcerer's Stone?",
        "What spell does Harry use to make his wand emit a light in the Sorcerer's Stone?"
    ], "answers": [
        "Expelliarmus",
        "Wingardium Leviosa",
        "Expecto Patronum",
        "Avada Kedavra",
        "Silencio",
        "Accio",
        "Piertotum Locomotor",
        "Oculus Reparo",
        "Wingardium Leviosa",
        "Lumos"
    ]}
}


# Function to get the player's name and age
def get_player_info():
    while True:
        name = input("What is your name? ")
        if not re.match("^[A-Za-z]*$", name):
            print("Sorry, only letters are allowed in the name. Please try again.")
        else:
            break

    while True:
        age = input("What is your age? ")
        if not age.isdigit() or int(age) < 1 or int(age) > 105:
            print("Sorry, only numbers between 1 and 105 are allowed in the age. Please try again.")
        else:
            break

    return name, int(age)


# Function to play the game
def play_game(category):
    # Shuffle the questions for the chosen category
    questions = categories[str(category)]["questions"]
    answers = categories[str(category)]["answers"]
    questions_and_answers = list(zip(questions, answers))
    random.shuffle(questions_and_answers)

    # Ask the questions and keep score
    score = 0
    for i, (question, answer) in enumerate(questions_and_answers[:10]):
        print(f"\nQuestion {i+1}: {question}")
        player_answer = input("Your answer: ")
        if player_answer.lower() == answer.lower():
            print("Correct!")
            score += 10
        else:
            print(f"Sorry, the correct answer is {answer}.")

    return score


# Define the scoreboard
scoreboard = []


# Authenticate with the Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("creds.json", scopes=scope)
client = gspread.authorize(creds)

# Open the scoreboard sheet
sheet_name = "Harry Potter Quiz Scoreboard"
sheet = client.open(sheet_name).sheet1

# Read the scoreboard data
header_row = sheet.row_values(1)
scoreboard = []
for row in sheet.get_all_values()[1:]:
    scoreboard.append(dict(zip(header_row, row)))

# Sort the scoreboard by score
scoreboard.sort(key=lambda x: x["Score"], reverse=True)

# Display the scoreboard
print("\nTop 5 Scores:")
for i, row in enumerate(scoreboard[:5]):
    print(f"{i+1}. {row['Name']} ({row['Age']}): {row['Score']}")

# Main loop
while True:
    print("""
 _  _    __    ___   ___  __   __   ___    __    _____   _____   ___   ___  
| || |  /  \  | _ \ | _ \ \ `v' /  | _,\  /__\  |_   _| |_   _| | __| | _ \ 
| >< | | /\ | | v / | v /  `. .'   | v_/ | \/ |   | |     | |   | _|  | v / 
|_||_| |_||_| |_|_\ |_|_\   !_!    |_|    \__/    |_|     |_|   |___| |_|_\ 

    """)
    print("\nWelcome to the Harry Potter Quiz!")
    print("Answer 10 questions to test your knowledge of the Harry Potter books and movies.")
    print("Each correct answer is worth 10 points.")
    print("\nYou can choose from the following categories:")
    for category in categories:
        print(f"{category}. {categories[category]['name']}")
    category = input("\nEnter the category number you want to play (1-4): ")

    if category in categories:
        name, age = get_player_info()
        print(f"\nWelcome, {name}!")
        score = play_game(category)

        print(f"\nThank you for playing, {name}!")
        print(f"Your final score is {score} out of 100.")

        # Update the scoreboard4
        scoreboard.append({"Name": name, "Age": age, "Score": score})
        scoreboard.sort(key=lambda x: int(x["Score"]), reverse=True)
        scoreboard = scoreboard[:5]

        # Display the scoreboard
        print("\nTop 5 Scores:")
        for i, row in enumerate(scoreboard[:5]):
            print(f"{i+1}. {row['Name']} ({row['Age']}): {row['Score']}")

        # Write the scoreboard data to the Google Sheet
        sheet.clear()
        sheet.append_row(header_row)
        for row in scoreboard:
            sheet.append_row([row["Name"], row["Age"], row["Score"]])

    else:
        print("Invalid input. Please enter a number from 1 to 4.")

    # Ask the player if they want to play again
    while True:
        play_again = input("Do you want to play again? (Y/N) ")
        if play_again.lower() == "y":
            break
        elif play_again.lower() == "n":
            print("Thanks for playing!")
            quit()
        else:
            print("Invalid input. Please enter Y or N.")
