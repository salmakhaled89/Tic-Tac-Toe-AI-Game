from tkinter import*  # Import all components from the tkinter library

# Create the main application window
root = Tk()
root.title("TIC TAC TOE AI")  # Set the title of the window

# Create a frame to display messages (like win/tie)
message_frame = Frame(root)
message_frame.pack()  # Add the message frame to the window

# Create a frame to hold the buttons (game board)
button_frame = Frame(root)
button_frame.pack()  # Add the button frame to the window

board = []  # List to hold the 9 game buttons (cells)
player = "X"  # Start with player X
end_game = False  # Flag to track if the game is over

# Function to check if the given player has won
def winningcheck(player):
    win_combos = [
        (0,1,2), (3,4,5), (6,7,8),  # Horizontal lines
        (0,3,6), (1,4,7), (2,5,8),  # Vertical lines
        (0,4,8), (2,4,6)            # Diagonals
    ]
    for a, b, c in win_combos:  # Iterate through all winning combinations
        if board[a]["text"] == player and board[b]["text"] == player and board[c]["text"] == player:
            return True  # Player has won
    return False  # No winning condition met

# Function to check for a tie
def tiecheck():
    if winningcheck('X') or winningcheck('O'):
        return False  # A win exists, so it's not a tie
    for i in range(9): 
        if board[i]["text"] == " ":  # If there's at least one empty cell
            return False  # Game not tied yet
    return True  # All cells filled and no winner: it's a tie

# Minimax algorithm with alpha-beta pruning for the AI decision-making
def minimax(board, depth, alpha, beta, is_maximizing):
    if winningcheck('X'):
        return depth - 10  # X wins: bad for AI
    if winningcheck('O'):
        return 10 - depth  # O wins: good for AI
    if tiecheck():
        return 0  # It's a tie

    if is_maximizing:
        best_value = -float('inf')  # Worst-case start for maximizer
        for i in range(9):
            if board[i]["text"] == " ":  # Try empty cells
                board[i]["text"] = 'O'  # AI makes a move
                value = minimax(board, depth + 1, alpha, beta, False)  # Recursive call
                board[i]["text"] = " "  # Undo move
                best_value = max(best_value, value)  # Update best value
                alpha = max(alpha, value)  # Update alpha
                if beta <= alpha:  # Beta cutoff
                    break
        return best_value
    else:
        best_value = float('inf')  # Worst-case start for minimizer
        for i in range(9):
            if board[i]["text"] == " ":  # Try empty cells
                board[i]["text"] = 'X'  # Player makes a move
                value = minimax(board, depth + 1, alpha, beta, True)  # Recursive call
                board[i]["text"] = " "  # Undo move
                best_value = min(best_value, value)  # Update best value
                beta = min(beta, value)  # Update beta
                if beta <= alpha:  # Alpha cutoff
                    break
        return best_value

# Function to perform the AI's move
def computer():
    global player, board, end_game
    if end_game:
        return  # Do nothing if the game has ended

    best_score = -float('inf')  # Initialize best score
    best_move = None  # Track best move

    for spot in range(9):
        if board[spot]["text"] == " ":  # If cell is empty
            board[spot].config(text="O")  # Simulate move
            score = minimax(board, 0, -float('inf'), float('inf'), False)  # Evaluate move
            board[spot].config(text=" ")  # Undo move
            if score > best_score:
                best_score = score  # Update best score
                best_move = spot  # Update best move

    if best_move is not None:
        board[best_move].config(text="O")  # Make the move
        if winningcheck("O"):
            winning_message = Label(message_frame, text=" O won", background="maroon", font=("arial", 20), width=7)
            winning_message.grid(row=3, column=0)  # Display win message
            end_game = True  # End game
        elif tiecheck():
            winning_message = Label(message_frame, text="Tied", background="SlateBlue1", font=("arial", 20), width=7)
            winning_message.grid(row=3, column=0)  # Display tie message
            end_game = True  # End game

# Function to reset the game
def restart():
    global player, end_game
    end_game = False  # Resume game
    for b in board:
        b.config(text=" ", state=NORMAL)  # Clear board
    winning_message = Label(message_frame, text=" ", font=("arial", 20), background="white", width=7)
    winning_message.grid(row=3, column=0)  # Clear message

# Main function triggered when a button is clicked
def main(button):
    global player, end_game
    if button["text"] == " " and not end_game:  # If button is empty and game not over
        button.config(text=player)  # Set player's mark

        if winningcheck(player):
            winning_message = Label(message_frame, text=" X won", background="green", font=("arial", 20), width=7)
            winning_message.grid(row=3, column=0)  # Display win message
            end_game = True
            return

        if tiecheck():
            winning_message = Label(message_frame, text="Tied", background="SlateBlue1", font=("arial", 20), width=7)
            winning_message.grid(row=3, column=0)  # Display tie message
            end_game = True
            return
        else:
            player = "O"  # Switch to AI
            root.after(100,computer())  #AI runs after 1ms
            player = "X"  # Switch back to player

# Create 9 buttons for the game board and place them in a 3x3 grid
button1 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button1),
                 background="SkyBlue2", foreground="white", width=3)
button1.grid(column=1, row=1)
board.append(button1)

button2 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button2),
                 background="SkyBlue2", foreground="white", width=3)
button2.grid(column=2, row=1)
board.append(button2)

button3 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button3),
                 background="SkyBlue2", foreground="white", width=3)
button3.grid(column=3, row=1)
board.append(button3)

button4 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button4),
                 background="SkyBlue2", foreground="white", width=3)
button4.grid(column=1, row=2)
board.append(button4)

button5 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button5),
                 background="SkyBlue2", foreground="white", width=3)
button5.grid(column=2, row=2)
board.append(button5)

button6 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button6),
                 background="SkyBlue2", foreground="white", width=3)
button6.grid(column=3, row=2)
board.append(button6)

button7 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button7),
                 background="SkyBlue2", foreground="white", width=3)
button7.grid(column=1, row=3)
board.append(button7)

button8 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button8),
                 background="SkyBlue2", foreground="white", width=3)
button8.grid(column=2, row=3)
board.append(button8)

button9 = Button(button_frame, text=" ", font=("arial", 40), command=lambda: main(button9),
                 background="SkyBlue2", foreground="white", width=3)
button9.grid(column=3, row=3)
board.append(button9)

# Add a restart button to reset the game
restart_button = Button(button_frame, text="restart", font=("arial", 15),
                        background="gray", foreground="white", width=9, command=restart)
restart_button.grid(column=2, row=4)

# Run the GUI event loop
root.mainloop()
