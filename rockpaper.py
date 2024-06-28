import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Rock, Paper, Scissors")
root.geometry("400x300")

# Add labels to display choices and results
user_choice_label = tk.Label(root, text="Your choice: ")
user_choice_label.pack()

computer_choice_label = tk.Label(root, text="Computer's choice: ")
computer_choice_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Add score labels
user_score_label = tk.Label(root, text="Your score: 0")
user_score_label.pack()

computer_score_label = tk.Label(root, text="Computer's score: 0")
computer_score_label.pack()

# Add buttons for Rock, Paper, and Scissors
rock_button = tk.Button(root, text="Rock", command=lambda: play_game("rock"))
rock_button.pack(side=tk.LEFT, padx=20)

paper_button = tk.Button(root, text="Paper", command=lambda: play_game("paper"))
paper_button.pack(side=tk.LEFT, padx=20)

scissors_button = tk.Button(root, text="Scissors", command=lambda: play_game("scissors"))
scissors_button.pack(side=tk.LEFT, padx=20)

# Initialize scores
user_score = 0
computer_score = 0

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "user"
    else:
        return "computer"

def play_game(user_choice):
    global user_score, computer_score
    computer_choice = get_computer_choice()
    winner = determine_winner(user_choice, computer_choice)
    
    user_choice_label.config(text=f"Your choice: {user_choice}")
    computer_choice_label.config(text=f"Computer's choice: {computer_choice}")
    
    if winner == "tie":
        result_label.config(text="It's a tie!")
    elif winner == "user":
        result_label.config(text="You win!")
        user_score += 1
    else:
        result_label.config(text="You lose!")
        computer_score += 1
    
    user_score_label.config(text=f"Your score: {user_score}")
    computer_score_label.config(text=f"Computer's score: {computer_score}")

# Run the main event loop
root.mainloop()