import random

def game_rules():
    print("GAMEPLAY RULES:")
    print("1. Turns:")
    print("   - The player taking the first turn is chosen at random")
    print("   - The active player chooses a movement chit, advancing the expedition marker")
    print("   - The used movement chit is discarded")
    print("   - Players collect gems or glass beads for each space landed on")
    print("\n2. End of the Game:")
    print("   - Game concludes when the expedition marker exits the board")
    print("   - Player not exiting the temple gets a bonus gem or glass bead randomly")
    print("\n3. Scoring:")
    print("   - Get points for gems; the more collected of one type, the higher the score")
    print("     - 1 gem of a single type = 1 point")
    print("     - 2 gems of a single type = 3 points")
    print("     - 3 gems of a single type = 6 points")
    print("     - 4 gems of a single type = 10 points")
    print("     - 5 gems of a single type = 15 points")
    print("     - 6 gems of a single type = 18 points")
    print("     - 7 gems of a single type = 21 points")
    print("   - Each glass bead collected removes a point from the total player score")
    print("\n4. Winner:")
    print("   - The player with the highest total score wins the game.")
    print('-' * 40)
    input("Press Enter to return to the Main Menu")
    main()
    
def generate_items():
    # Defines the collectable items in the temple and shuffles them
    gems = ('R' * 7) + ('E' * 7) + ('D' * 7) + ('S' * 7)
    
    beads = ('G' * 11)
    
    all_items = list(gems + beads)
    
    random.shuffle(all_items)
    
    return all_items

def new_game():
    # Initialise the temple list and visual temple space
    temple = []
    space = '[ ] '
    
    # Initialise the temple marker with unicode 'running man'
    marker = str("[" + chr(127939) + "] ")
    
    # Initialise the movement chit list
    movement = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]

    # Creation of the temple with 40 spaces
    for i in range(40):
        temple.append(space)

    # Allow the user input of player names and store in a variable    
    player_1 = input("Player 1, Please enter your name: ")
    
    # Error handling if user doesn't input anything
    while not player_1:
        print("Please enter a valid name for Player 1.")
        player_1 = input("Player 1, Please enter your name: ")
        
    player_2 = input("Player 2, Please enter your name: ")
    
    # Error handling if user doesn't input anything
    while not player_2:
        print("Please enter a valid name for Player 2.")
        player_2 = input("Player 2, Please enter your name: ")

    # Place temple marker at the beginning of temple
    temple[0] = marker
    
    print('-' * 80)
    
    return player_1, player_2, marker, temple, movement

def display_temple(temple):
    # Print the current state of the temple
    # Changed from 'for space in temple:' print(space) due to slow printing
    temple_str = ''.join(temple)
    print(temple_str + "\n")
    

def movement_picker(movement):
    # Allow players to choose their movement from the movement chit list
    i = 0 # Initialise 'i' when function called for consistent menu options

    # Display the available movement options
    for move in movement:
        # Align 'i' with displayed options
        i += 1 
        print(i, ":", move)
        
    while True:
        # Prompt the player to input their chosen movement
        player_input = input("Choose your movement with the number on the left: ")
        
        # Error handling in case user enters non-numeric input
        if player_input.isdigit():
            
            # Initialise player_move as an integer from player_input
            player_move = int(player_input)
            
            # Error handling to ensure valid movement selected
            if 1 <= player_move <= len(movement):
                
                # Adjust player_move to 0-based index
                player_move -= 1
                
                # Retrieve chosen move value from movement list using index
                chosen_move = movement[player_move]

                # Remove the chosen movement chit from the movement list
                del movement[player_move]
                
                print('-' * 49)
                
                return chosen_move
            
            else:
                
                print("Invalid movement number. Please try again.")
        else:
            
            print("Please enter a valid number.")


def count_scores(inv):
    # Initialise player score and glass bead count
    score = 0
    bead_count = 0

    # Check if glass beads are in inventory
    if 'G' in inv:
        
        # Store amount in variable
        bead_count = inv['G']
        
        # Remove glass bead key to allow calculation of gems only
        del inv['G']
        
    else:
        # Initialise bead count if none present to error handle calculation
        bead_count = 0

    # Iterate through given player inventory  
    for gem, count in inv.items():
        
        # Calculate player score based on triangular number sequence
        score += count * (count + 1) // 2

    # Update score variable negatively based on bead count above    
    score -= bead_count

    # Error handling if more glass beads than gems to prevent negative score
    if score < 0:
        score = 0
        
    return score, bead_count

def play_game(player_1, player_2, marker, temple, items, movement):
    # Initialise space variable to update temple when marker moved
    space = '[ ] '
    
    # Initialise gem name dictionary to display gem names in full when required
    gem_names = {'R': 'Ruby', 'E': 'Emerald',
                 'D': 'Diamond', 'S': 'Sapphire',
                 'G': 'Glass Bead'}

    # Initialise variable to determine which player goes first randomly
    player_turn = random.choice([True, False])

    # Initialise the location of marker at the start of the temple
    marker_loc = 0

    # Initialise the previous marker location for consistency
    prev_marker_loc = 0

    # Initialise Player 1's inventory dictionary
    player_1_inv = {}

    # Initialise Player 2's inventory dictionary
    player_2_inv = {}

    # Prints the temple with marker before any turns are taken
    display_temple(temple)

    # Main Game Loop
    while True:
        
        # Introduces the turns by using the user input player name
        if player_turn:
            print(player_1 + "'s turn")
            print('-' * 8)
            
        else:
            
            print(player_2 + "'s turn")
            print('-' * 8)
            
        while True:
            # Current player calls the movement_picker function
            
            # Movement chit chosen is stored in variable
            chosen_move = movement_picker(movement)

            # Marker location variable is updated by movement chit chosen
            marker_loc += chosen_move

            # Ensure gramatically correct prompt if chosen move is singular
            if chosen_move == 1:

                # Check player turn and print appropriate movement message
                if player_turn:
                    print(player_1, "traversed", chosen_move, "space.\n")
                else:
                    print(player_2, "traversed", chosen_move, "space.\n")
                    
                # Print current location of the marker if within temple bounds
                if marker_loc < 40:
                    print("Marker is now at position " + str(marker_loc + 1) + "/40 in the temple.\n")

            #  Handle when chosen movement chit is greater than 1
            elif chosen_move > 1:
                
                # Check player turn and print appropriate movement message
                if player_turn:
                    print(player_1, "traverses", chosen_move, "spaces.\n")
                else:
                    print(player_2, "traverses", chosen_move, "spaces.\n")

                # Print current location of the marker if within temple bounds    
                if marker_loc < 40:
                    print("Marker is now at position " + str(marker_loc + 1) + "/40 in the temple.\n")

            # Handle when chosen movement chit is 0       
            if chosen_move == 0:

                # Check player turn and print appropriate skip message
                if player_turn:
                    print(player_1, "skipped their turn.\n")
                else:
                    print(player_2, "skipped their turn.\n")

                # Switch player turn boolean value
                player_turn = not player_turn

                # Display current state of temple after turn skipped
                display_temple(temple)

                # Break loop for player who skipped their turn
                break
            
            else:
                # Update and store previous marker location using calculation
                prev_marker_loc = marker_loc - chosen_move

                # Check if marker has reached or surpassed the length of temple
                if marker_loc >= 39:

                    # Initialise bonus item variable for player not exiting
                    bonus_item = random.choice(items)

                    # Check player turn to ensure correct actions taken
                    if player_turn:

                        # Print appropriate message for player exiting temple
                        print(player_1, "exited the temple.\n")

                        # Print appropriate message for player recieving bonus item
                        print(player_2, "collected bonus item:", gem_names.get(bonus_item))

                        # Check if bonus item is already in player inventory
                        if bonus_item in player_2_inv:
                            
                            # Update item amount by 1 if already present
                            player_2_inv[bonus_item] += 1
                            
                        else:
                            # Add item into inventory if not present
                            player_2_inv[bonus_item] = 1
                            
                    else:
                        # Print appropriate message for player exiting temple
                        print(player_2, "exited the temple.\n")
                        
                        # Print appropriate message for player recieving bonus item
                        print(player_1, "collected bonus item:", gem_names.get(bonus_item))

                        # Check if bonus item is already in player inventory
                        if bonus_item in player_1_inv:
                            
                            # Update item amount by 1 if already present
                            player_1_inv[bonus_item] += 1
                            
                        else:
                            # Add item into inventory if not present
                            player_1_inv[bonus_item] = 1

                    # Call count_scores function and assign return variables        
                    score_player_1, bead_count_p1 = count_scores(player_1_inv)
                    score_player_2, bead_count_p2 = count_scores(player_2_inv)

                    # Print appropriate message due to game ending
                    print('-' * 40)
                    print("Game Over!".center(40))
                    print('-' * 40)
                    
                    print(player_1 + "'s Inventory")
                    print('-' * (len(player_1) + 12))
                    
                    # Iterate through player 1 inventory by key and count
                    for item, count in player_1_inv.items():

                        # Print inventory items using gem_names dict and count
                        print(gem_names.get(item) + ": " + str(count))

                    # Print glass bead amount underneath inventory items
                    print("Glass Beads:", bead_count_p1)
                    
                    print('-' * 40,"")
                    
                    print(player_2 + "'s Inventory")
                    print('-' * (len(player_2) + 12))

                    # Iterate through player 2 inventory by key and count
                    for item, count in player_2_inv.items():

                        # Print inventory items using gem_names dict and count
                        print(gem_names.get(item) + ": " + str(count))

                    # Print glass bead amount underneath inventory items
                    print("Glass Beads:", bead_count_p2)
                    
                    print('-' * 40)

                    # Print player scores with calculated score variables
                    print(player_1 + "'s Score:", score_player_1)
                    print(player_2 + "'s Score:", score_player_2)
                    print('-' * 40,"")

                    # Check winner based on score amount
                    if score_player_1 > score_player_2:
                        
                        # Print appropriate win message
                        print(str("*** " + player_1 + " wins!" + " ***").center(40))
                        print('-' * 40)
                    else:
                        # Print appropriate win message
                        print(str("*** " + player_2 + " wins!" + " ***").center(40))
                        print('-' * 40)

                    # Require user input to prevent main() from running
                    input("Press Enter to return to the Main Menu")
                    return

                # Update temple with marker based on calculated marker location
                temple[marker_loc] = marker

                # Update previously occupied temple space with an empty one
                temple[prev_marker_loc] = space

                # Choose item from randomised item list based on previous marker location
                item = items[prev_marker_loc]

                # Check player turn to ensure correct inventory is updated
                if player_turn:
                    
                    # Initialise player_inv variable based on turn
                    player_inv = player_1_inv
                    
                    # Print appropriate message of collected item
                    print(player_1 + " collected item: " + gem_names.get(item) + "\n")
                    
                else:

                    # Initialise player_inv variable based on turn
                    player_inv = player_2_inv

                    # Print appropriate message of collected item
                    print(player_2 + " collected item: " + gem_names.get(item) + "\n")

                # Iterate through player_inv to check if item already present
                if item in player_inv:

                    # Update item amount by key if item already present in dictionary
                    player_inv[item] += 1
                    
                else:

                    # Add item into player_inv dictionary by key if item not present
                    player_inv[item] = 1
                    
            # Display updated state of temple after movement       
            display_temple(temple)

            # Switch player turn boolean value
            player_turn = not player_turn
            
            break

def main():
    # Main Menu Loop
    
    while True:

        # Print welcome message and menu options
        print('-' * 40)
        print("Welcome to Sun Temple".center(40))
        print('-' * 40)
        print("1: New Game")
        print("2: Game Rules")
        print("3: Quit")

        # Allow user input of menu option choice and store in variable
        menu_choice = input("Select an menu option: ")
        
        print('-' * 40)

        # Initialises the players, marker, temple, movement chits
        # Initialises a random item list
        # Starts the main game loop
        if menu_choice == '1':
            player_1, player_2, marker, temple, movement = new_game()
            items = generate_items()
            play_game(player_1, player_2, marker, temple, items, movement)
            
        # Displays game rules and objectives
        elif menu_choice == '2':
            game_rules()

        # Exit game with goodbye message    
        elif menu_choice == '3':
            print("Thank you for playing, Goodbye!")
            break

        # Error handling if invalid menu options input
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
