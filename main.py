import json
import os
import random
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

HIGH_SCORE_FILE = "score.txt"
LEADERBOARD_FILE = "leaderboard.txt"
QUESTION_FILE = "questions.json"


# ----------------------------
# Load Questions
# ----------------------------
def load_questions():
    try:
        with open(QUESTION_FILE, "r") as file:
            questions = json.load(file)
            random.shuffle(questions)
            return questions

    except FileNotFoundError:
        print(Fore.RED + "questions.json not found!")
        return []


# ----------------------------
# Read High Score
# ----------------------------
def get_high_score():

    if os.path.exists(HIGH_SCORE_FILE):

        with open(HIGH_SCORE_FILE, "r") as file:

            score = file.read().strip()

            if score.isdigit():
                return int(score)

    return 0


# ----------------------------
# Save High Score
# ----------------------------
def save_high_score(score):

    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


# ----------------------------
# Save Leaderboard
# ----------------------------
def save_leaderboard(name, score):

    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"{name},{score}\n")


# ----------------------------
# Show Leaderboard
# ----------------------------
def show_leaderboard():

    if not os.path.exists(LEADERBOARD_FILE):
        print(Fore.RED + "\nLeaderboard is empty!")
        return

    scores = []

    with open(LEADERBOARD_FILE, "r") as file:

        for line in file:

            if "," in line:

                name, marks = line.strip().split(",")

                scores.append((name, int(marks)))

    scores.sort(key=lambda x: x[1], reverse=True)

    print("\n" + "=" * 50)
    print(Fore.YELLOW + "🏆 TOP 5 LEADERBOARD")
    print("=" * 50)

    if len(scores) == 0:
        print("No Scores Available")
    else:

        for i, (name, marks) in enumerate(scores[:5], start=1):
            print(f"{i}. {name:<20} {marks}")

    print("=" * 50)


# ----------------------------
# Play Quiz
# ----------------------------
def play_quiz():

    questions = load_questions()

    if len(questions) == 0:
        return

    score = 0

    print("\n" + "=" * 60)
    print(Fore.CYAN + "        PYTHON QUIZ GAME")
    print(Fore.CYAN + "     Upskill Campus Internship Project")
    print(Fore.CYAN + "       Developed by Viral Patel")
    print("=" * 60)

    difficulty_color = {
        "Easy": Fore.GREEN,
        "Medium": Fore.YELLOW,
        "Hard": Fore.RED
    }

    for index, question in enumerate(questions, start=1):

        progress = int(((index - 1) / len(questions)) * 20)

        print(
            Fore.CYAN +
            f"\nProgress : [{'█'*progress}{'-'*(20-progress)}] {index}/{len(questions)}"
        )

        print("\n" + "-" * 60)

        print(Fore.WHITE + f"Question {index}")

        print(
            difficulty_color.get(
                question["difficulty"],
                Fore.WHITE
            )
            + f"Difficulty : {question['difficulty']}"
        )

        print(Fore.MAGENTA + question["question"])

        print()

        for i, option in enumerate(question["options"], start=1):
            print(f"{i}. {option}")
                # ----------------------------
        # Input Validation
        # ----------------------------
        while True:

            try:

                choice = int(input("\nEnter your choice (1-4): "))

                if 1 <= choice <= 4:
                    break

                else:
                    print(Fore.YELLOW + "⚠ Please enter a number between 1 and 4.")

            except ValueError:
                print(Fore.RED + "⚠ Invalid input! Please enter a valid number.")

        # ----------------------------
        # Check Answer
        # ----------------------------
        if question["options"][choice - 1] == question["answer"]:

            print(Fore.GREEN + "\n✅ Correct Answer!")

            score += 1

        else:

            print(Fore.RED + "\n❌ Wrong Answer!")

            correct_index = question["options"].index(question["answer"]) + 1

            print(
                Fore.YELLOW +
                f"Correct Answer : {correct_index}. {question['answer']}"
            )

    # ----------------------------
    # Quiz Finished
    # ----------------------------
    total = len(questions)

    percentage = (score / total) * 100

    now = datetime.now()

    print("\n" + "=" * 60)
    print(Fore.CYAN + "              QUIZ SUMMARY")
    print("=" * 60)

    print(f"📅 Date                : {now.strftime('%d-%m-%Y')}")
    print(f"🕒 Time                : {now.strftime('%I:%M:%S %p')}")

    print(f"\n📚 Questions Attempted : {total}")
    print(Fore.GREEN + f"✅ Correct Answers     : {score}")
    print(Fore.RED + f"❌ Wrong Answers       : {total-score}")
    print(Fore.CYAN + f"📊 Percentage          : {percentage:.2f}%")

    print("=" * 60)

    # ----------------------------
    # Performance Message
    # ----------------------------
    if percentage == 100:

        print(Fore.GREEN + "🏆 Outstanding! Perfect Score!")

    elif percentage >= 80:

        print(Fore.GREEN + "🎉 Excellent Performance!")

    elif percentage >= 60:

        print(Fore.CYAN + "👍 Good Job!")

    elif percentage >= 40:

        print(Fore.YELLOW + "🙂 Nice Try! Keep Practicing.")

    else:

        print(Fore.RED + "📚 Don't Give Up! Practice More.")

    # ----------------------------
    # High Score
    # ----------------------------
    high_score = get_high_score()

    if score > high_score:

        save_high_score(score)

        high_score = score

        print(Fore.YELLOW + "\n🏆 Congratulations!")
        print(Fore.YELLOW + "New High Score Created!")

    print(Fore.MAGENTA + f"\nHighest Score : {high_score}")

    # ----------------------------
    # Save Leaderboard
    # ----------------------------
    player = input("\nEnter your name for Leaderboard : ")

    if player.strip() == "":
        player = "Guest"

    save_leaderboard(player, score)

    print(Fore.BLUE + "\n✔ Score saved successfully!")

    print(Fore.BLUE + "\nThank you for playing the Python Quiz Game!")
    print(Fore.BLUE + "Developed for Upskill Campus Internship 2026")

# ----------------------------
# Main Menu
# ----------------------------
def main():

    while True:

        print("\n" + "=" * 60)
        print(Fore.CYAN + "          PYTHON QUIZ GAME")
        print(Fore.CYAN + "     Upskill Campus Internship Project")
        print("=" * 60)

        print("1. ▶ Start Quiz")
        print("2. 🏆 View High Score")
        print("3. 📈 View Leaderboard")
        print("4. ℹ About Project")
        print("5. 🚪 Exit")

        menu = input("\nEnter your choice (1-5): ")

        # ----------------------------
        # Start Quiz
        # ----------------------------
        if menu == "1":

            while True:

                play_quiz()

                again = input("\nDo you want to play again? (Y/N): ").strip().lower()

                if again == "y":
                    continue
                else:
                    break

        # ----------------------------
        # High Score
        # ----------------------------
        elif menu == "2":

            print("\n" + "=" * 40)
            print(Fore.YELLOW + "🏆 HIGHEST SCORE")
            print("=" * 40)

            print(Fore.GREEN + f"Highest Score : {get_high_score()}")

            print("=" * 40)

        # ----------------------------
        # Leaderboard
        # ----------------------------
        elif menu == "3":

            show_leaderboard()

        # ----------------------------
        # About Project
        # ----------------------------
        elif menu == "4":

            print("\n" + "=" * 60)
            print(Fore.CYAN + "ABOUT PROJECT")
            print("=" * 60)

            print("""
Project Name :
Python Quiz Game

Description :
A console-based quiz application developed in Python
as part of the Upskill Campus Summer Internship.

Features :
✔ Random Questions
✔ Difficulty Levels
✔ High Score
✔ Leaderboard
✔ Colored Output
✔ Input Validation
✔ Performance Report
✔ JSON Question Database

Technologies Used :
• Python
• JSON
• Colorama
• File Handling

Developer :
Viral Patel
B.Tech Information Technology

Internship :
Upskill Campus Summer Internship 2026
            """)

            print("=" * 60)

        # ----------------------------
        # Exit
        # ----------------------------
        elif menu == "5":

            print("\n" + "=" * 60)
            print(Fore.GREEN + "Thank you for using Python Quiz Game!")
            print(Fore.CYAN + "Have a Nice Day 😊")
            print("=" * 60)

            break

        else:

            print(Fore.RED + "\nInvalid Choice! Please enter 1-5.")


# ----------------------------
# Program Starts Here
# ----------------------------
if __name__ == "__main__":
    main()   