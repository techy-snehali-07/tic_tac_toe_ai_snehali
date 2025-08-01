import tkinter as tk
from tkinter import messagebox

# Constants
HUMAN = 'X'
AI = 'O'
EMPTY = ''

# Initialize board
board = [EMPTY] * 9
game_over = False

# Tkinter GUI setup
window = tk.Tk()
window.title("Tic Tac Toe AI (Unbeatable)")
window.geometry("400x500")
window.configure(bg="black")

title = tk.Label(window, text="🎮 Tic-Tac-Toe ", font=("Arial", 20, "bold"), fg="lightgreen", bg="black")
title.pack(pady=10)

status_label = tk.Label(window, text="", font=("Arial", 14), fg="white", bg="black")
status_label.pack(pady=5)

# Frame for buttons
frame = tk.Frame(window, bg="black")
frame.pack()

buttons = []

def draw_board():
    for i in range(9):
        buttons[i]['text'] = board[i]

def check_win(player):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(board[pos] == player for pos in combo) for combo in wins)

def minimax(new_board, is_maximizing):
    if check_win(AI):
        return {"score": 10}
    elif check_win(HUMAN):
        return {"score": -10}
    elif EMPTY not in new_board:
        return {"score": 0}

    moves = []

    for i in range(9):
        if new_board[i] == EMPTY:
            move = {"index": i}
            new_board[i] = AI if is_maximizing else HUMAN
            result = minimax(new_board, not is_maximizing)
            move["score"] = result["score"]
            new_board[i] = EMPTY
            moves.append(move)

    if is_maximizing:
        return max(moves, key=lambda x: x['score'])
    else:
        return min(moves, key=lambda x: x['score'])

def ai_move():
    global game_over
    if game_over:
        return
    move = minimax(board, True)
    board[move["index"]] = AI
    draw_board()
    if check_win(AI):
        status_label.config(text="AI wins!")
        game_over = True
    elif EMPTY not in board:
        status_label.config(text="It's a draw!")
        game_over = True

def on_click(index):
    global game_over
    if game_over or board[index] != EMPTY:
        return
    board[index] = HUMAN
    draw_board()
    if check_win(HUMAN):
        status_label.config(text="You win!")
        game_over = True
    elif EMPTY not in board:
        status_label.config(text="It's a draw!")
        game_over = True
    else:
        window.after(300, ai_move)

def reset_game():
    global board, game_over
    board = [EMPTY] * 9
    game_over = False
    draw_board()
    status_label.config(text="")

# Create 3x3 buttons
for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 24, "bold"), width=5, height=2,
                    bg="#111", fg="cyan", activebackground="#333",
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Reset Button
reset_btn = tk.Button(window, text="🔁 Restart", font=("Arial", 12), bg="#444", fg="white", command=reset_game)
reset_btn.pack(pady=10)

# Start the game
draw_board()
window.mainloop()
