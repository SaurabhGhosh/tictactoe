import random
import os
import time


class Tictactoe:
    """ This class contains all the methods and attributes for the popular board game - Tic Tac Toe!!
        This rendition of the game is played by one player against the computer.
        When the game is started, player will need to pick a symbol - 'X'/'O' and choose the position number to
        place the symbol on the Tic Tac Toe board.
        The player to position three symbols in a line will win. If no winner emerges, game will be tied."""
    # Chosen symbol ('X'/'O') for the computer player
    computer_symbol = ''
    # Chosen symbol ('X'/'O') for the human player
    player_symbol = ''
    # Board grid as list - each element contains the position number and the symbol at that position
    grid = []
    # List of all the position numbers
    all_places = []
    # Position numbers of player's symbol
    player_filled_places = []
    # Position numbers of computer's symbol
    computer_filled_places = []
    # Empty positions that will complete the sequence for player if filled
    player_winning_places = []
    # Empty positions that will complete the sequence for computer if filled
    computer_winning_places = []
    # List of sequences for winning placement in the grid e.g. [1, 2, 3] for the first row
    winning_sequences = []

    def __init__(self):
        """Initiates the Tictactoe object. This method sets the initial values of the class attributes."""
        # Board grid as list - each element contains the position number and the symbol at that position
        self.grid = [[[1, ' '], [2, ' '], [3, ' ']],
                     [[4, ' '], [5, ' '], [6, ' ']],
                     [[7, ' '], [8, ' '], [9, ' ']]]
        # Another way of initializing using list comprehension
        # grid = [[[j, ' '] for j in range(i + 3, i + 6)] for i in range(-2, 5, 3)]
        # List of all the position numbers
        self.all_places = list(range(1, 10))
        # List of sequences for winning placement in the grid e.g. [1, 2, 3] for the first row
        self.winning_sequences = [[1, 2, 3],
                                 [4, 5, 6],
                                 [7, 8, 9],
                                 [1, 4, 7],
                                 [2, 5, 8],
                                 [3, 6, 9],
                                 [1, 5, 9],
                                 [3, 5, 7]]

    def get_symbol_at_place(self, place):
        """Retrieves the symbol present at the position"""
        # Iterate through the rows
        for x in self.grid:
            # Iterate through each item in the row
            for y in x:
                # Return the symbol for the matching position number
                if y[0] == place:
                    return y[1]

    def set_symbol_at_place(self, place, chosen_symbol):
        """Sets the symbol into the provided position number"""
        # Iterate through the rows
        for x in self.grid:
            # Iterate through each item in the row
            for y in x:
                # Set the symbol into the matching position number
                if y[0] == place:
                    y[1] = chosen_symbol
        # Update the list of filled positions for computer or player as per the passed symbol
        self.computer_filled_places.append(place) \
            if chosen_symbol == self.computer_symbol else self.player_filled_places.append(place)

    def draw_board(self):
        """Draws the grid. If the position is blank, prints the position number otherwise shows the position
        number."""
        # Iterate through the rows
        for x in self.grid:
            # Draw the line separator
            print('----------')
            # Show the position number if blank or show the symbol at place
            # Separate with '|' symbol
            print((x[0][0] if x[0][1] == ' ' else x[0][1]), '|', (x[1][0] if x[1][1] == ' ' else x[1][1]), '|',
                  (x[2][0] if x[2][1] == ' ' else x[2][1]))
        # Print the last border after the rows
        print('----------')

    def check_for_winning_places(self):
        """Checks the current positions of the players and calculates if there is an available position
        for winning move.
        The winning move(s) are then noted for both players."""
        # Reset the queues of winning moves for player and computer as the queues are going to be rebuilt
        # in this method.
        self.player_winning_places.clear()
        self.computer_winning_places.clear()
        # Iterate through the winning sequences for game
        for x in self.winning_sequences:
            # Check if two positions of a winning position are filled already by player
            # It is done by checking the overlap between two sets
            if len(set(x) & set(self.player_filled_places)) == 2:
                # Verify that the remaining gap place is blank by removing all filled places from sequence
                player_gap_place = set(x) - set(self.player_filled_places) - set(self.computer_filled_places)
                # Add the gap place as possible winning move for player
                if len(player_gap_place) == 1:
                    self.player_winning_places.append(list(player_gap_place)[0])
            # Check if two positions of a winning position are filled already by computer
            # It is done by checking the overlap between two sets
            if len(set(x) & set(self.computer_filled_places)) == 2:
                # Verifies that the remaining gap place is blank by removing all filled places from sequence
                computer_gap_place = set(x) - set(self.computer_filled_places) - set(self.player_filled_places)
                # Add the gap place as possible winning move for computer
                if len(computer_gap_place) == 1:
                    self.computer_winning_places.append(list(computer_gap_place)[0])

    def choose_next_placement(self):
        """Decides the next placement for computer player.
        First it tries to fill one of the winning chances for computer player.
        If there is no winning chance, then it fills one of the winning chances for human player to block.
        If there is no winning chance for either players, it fills any available place."""
        # Select a winning place for computer if available
        if len(self.computer_winning_places) > 0:
            next_place = random.choice(self.computer_winning_places)
        # Select a winning place for human player if available - to block opponent
        elif len(self.player_winning_places) > 0:
            next_place = random.choice(self.player_winning_places)
        # Select any available place
        else:
            next_place = random.choice(
                list(set(self.all_places) - set(self.computer_filled_places) - set(self.player_filled_places)))
        # Place computer's symbol at selected place
        self.set_symbol_at_place(int(next_place), self.computer_symbol)

    def check_winner(self):
        """Checks outcome of game based on current position of the symbols.
        Returns 'player'/'computer'/'tied' or 'continue' when the game is still on."""
        # Iterate through the winning sequences
        for x in self.winning_sequences:
            # Check if the winning sequence is a subset or same as the player's filled positions
            if set(x) <= set(self.player_filled_places):
                # Declare 'player' as winner
                return 'player'
            # Check if the winning sequence is a subset or same as the computer's filled positions
            elif set(x) <= set(self.computer_filled_places):
                # Declare 'computer' as winner
                return 'computer'
        # It is 'tied' if all the places are filled and there was no winner
        if len(self.player_filled_places) + len(self.computer_filled_places) == 9:
            return 'tied'
        # Return 'continue' if no winner and there are still available places
        return 'continue'

    def play_tictactoe(self):
        """This method controls the game steps.
        It prompts for input, updates player's position and updates computer's position.
        It lets user exit with specific exit key."""
        # Clear the screen
        os.system('cls')
        # Prompt player to select a symbol between 'X'/'O'
        self.player_symbol = input('Select your symbol (X/O)\nPress Z to exit\n')
        # Loop till user gives correct input
        while self.player_symbol not in ['X', 'O']:
            # Exit if user chooses exit key
            if self.player_symbol == 'Z':
                return
            # Prompt to enter correct key for player's symbol
            elif self.player_symbol not in ['X', 'O']:
                self.player_symbol = input('Invalid input!!\nSelect your symbol (X/O)\nPress Z to exit\n')
        # Update the computer's symbol with the other key of 'X'/'O'
        self.computer_symbol = list({'X', 'O'} - set(self.player_symbol)).pop()

        # Starting with the game after player's symbol is selected
        input_char = ''
        winning_candidate = 'none'
        # Continue until player exits
        while input_char != 'Z':
            # Clear screen to render at same place
            os.system('cls')
            # Show the player and computer symbol on screen
            print('Player -', self.player_symbol, ', Computer -', self.computer_symbol)
            # Draw the board before any symbol is placed
            self.draw_board()
            # Take player's input for position number
            input_char = input('Choose a position number to place your symbol\nPress Z to exit\n')
            # Verify that a valid position number is entered
            if input_char.isnumeric() and int(input_char) in range(1, 10):
                # Check if the selected position is empty
                if self.get_symbol_at_place(int(input_char)) == ' ':
                    # Set player's symbol in the selected position
                    self.set_symbol_at_place(int(input_char), self.player_symbol)
                # Check if player's selection makes him winner already or the game is tied
                winning_candidate = self.check_winner()
                if winning_candidate == 'player' or winning_candidate == 'tied':
                    input_char = 'Z'
                else:
                    # If player is not winner or game is not tied, continue for computer player's placement
                    # Update the possible winning places for both players
                    self.check_for_winning_places()
                    # Make next move for computer player
                    self.choose_next_placement()
                    # Check if computer player becomes winner after the move
                    winning_candidate = self.check_winner()
                    if winning_candidate == 'computer':
                        input_char = 'Z'
        # After game is concluded in any manner, redraw the board and show the final outcome
        # Clear screen
        os.system('cls')
        # Show the player and computer symbol on screen
        print('Player -', self.player_symbol, ', Computer -', self.computer_symbol)
        # Redraw the board
        self.draw_board()
        # Show the winning candidate or tied or abandoned
        if winning_candidate == 'computer' or winning_candidate == 'player':
            print(f'Winner -- {winning_candidate}')
        elif winning_candidate == 'tied':
            print('Match tied')
        else:
            print('Match abandoned')


# Check whether the game is executed from command
if __name__ == '__main__':
    # Create instance of game
    ttt = Tictactoe()
    # Start of play
    ttt.play_tictactoe()
