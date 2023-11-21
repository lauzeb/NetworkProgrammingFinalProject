# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 01:36:10 2023

@author: rabih
"""

import socket
import threading
import sys
import json

# Define the server details
Port = 1234
Host = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, Port))
print("Connected to the server")

message = ""

def send_message(message):
    s.sendall(message.encode())
    print("Sent message to server")

def recieve_message():
    return s.recv(2048).decode()

def print_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
   
def play_game():
    print("Welcome to Connect Four!")
    print("Type 'JOIN' to join an existing game or 'CREATE' to create a new game.")

    while True: # Application loop
        choice = input("> ").upper()
        if choice == "JOIN":
            
            enteringPassword = True
            
            while enteringPassword:
                password = input("Type in a valid password: ")
                send_message(f"PASSWORD {password}")
                response = recieve_message()
                
                if response == "PASSWORD_ACCEPTED":
                    enteringPassword = False
                    #start the actual game
                    
                    #Doesn't reconize when password is correct on server
                else:
                    print(response)
            
        elif choice == "CREATE":
            send_message("STARTGAME")
            message = s.recv(2048).decode()
            print(f"Game created Password: {message}")
            #wait for someone to join
            
            waiting = True
            while waiting:
                response = recieve_message()

                if response == "PASSWORD_ACCEPTED":
                    waiting = False
                    #start the actial agme
                else:
                    print(response)
        
        elif choice == "LEAVE":
            send_message("EXITGAME")
            s.close()
            break
        else:
            print("Invalid input. Please type 'JOIN' or 'CREATE'.")
            
        
        game_board = [[0 for _ in range(7)] for _ in range(6)]
        print("Connect Four Game")
        
        # SHIFT TO ACTUAL GAME  
        while choice in ["JOIN", "CREATE"]:
            game_active = True  
            turn_active = False
        
            while game_active:
                # Receive server messages indicating player turn,  game state
                print("wait for server response... ")
                server_message = recieve_message()
                board_state = server_message.split(" ", 1)[1]
                board_state = json.loads(board_state)
                server_message = server_message.split()
                
                turn_message = server_message[0]
                #board_state = server_message[1]
                
                #print("Turn message", turn_message)
        
                if turn_message == "YOUR_TURN":
                    turn_active = True
                    
                    print("Your Turn!")
                    
                    print_board(board_state)  # Update with server-sent game board
                    
                    while turn_active:
                        move = input("Enter column number (0-6) to make a move or 'LEAVE' to exit: ").upper()
                        
                        # look into below
                        #TODO either modify or remove ablity 
                        if move == "LEAVE":
                            send_message("LEAVE")
                            s.close()
                            break
            
                        try:
                            col = int(move)
                            if 0 <= col <= 6:
                                # Send the move to the server
                                send_message(f"MOVE {col}")
                                break
                            else:
                                print("Invalid column number. Please enter a number between 0 and 6.")
                    
                        except ValueError:
                            print("Invalid input. Please enter a valid column number or 'LEAVE' to exit.")
                            
                    turn_active = False
        
                elif turn_message == "WAITING_TURN":
                    print("Waiting for opponent's move...")
                    print_board(board_state)         
                    # Continue waiting for server updates indicating the player's turn
        
                elif turn_message == "HOST_PLAYER_WON":
                    print("Host player won!")
                    game_active = False  # Breaks the inner loop, ending the game
        
                elif turn_message == "JOINING_PLAYER_WON":
                    print("Joining player won!")
                    game_active = False  # Breaks the inner loop, ending the game
        
                # Add more conditions based on the server messages for other game states
        
            # IMPLEMENT AGAIN FUNCTIONALITY
            
            endGameResponse = input("AGAIN or LEAVE, either leave the other will also ")
            
            send_message(endGameResponse)
            
            response = recieve_message()
            
            if(response == "RESET"):
                pass
            elif(response == "FORCED_CANCEL"):
                pass
            
            break

    

# Start the game
play_game()

# Clean up when the game ends
sys.exit(0)