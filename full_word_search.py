"""
File: full_word_search.py
Author: Ethan Holley
Purpose: This program uses File I/O operations and produces a word search gameplay.
"""


import random

def create_grid(height, length):
    """
    This function creates a grid of user inputs size and length.
    Parameters:
        height - integer
        length - integer
    Returns:
        grid - 2D Grid List
    """
    length = int(length)
    height = int(height)
    grid = []
    for i in range(height):
        row = []
        for j in range(length):
            row.append(chr(random.randint(97,122)))
        grid.append(row)
    return grid

def transpose_grid(grid):
    """
    This function inverts the grid for to make searching easier.
    Parameters:
        grid - the 2D grid
    Returns:
        new_grid - the inverted 2D grid
    """
    new_grid = []
    for i in range(len(grid[0])):
        row = []
        for j in range(len(grid)):
            row.append(grid[j][i])
        new_grid.append(row)
    return new_grid

def read_file(file_name, height, length):
    """
    This function reads the dictionary file and puts all words >= len of 3
    into a list.
    Parameters:
        file_name - the inputed txt file
        height - user entered integer
        length - user entered integer
    Returns: 
        words_list - list of all the valid words for word search
    """
    words_list = []
    f = open(file_name, "r")
    for line in f:
        word = line.strip()
        word = word.lower()
        if int(height) >= 10 and int(length) >= 10:
            if len(word) >= 3:
                words_list.append(word)
        elif len(word) >= 3:
            words_list.append(word)
    return words_list

def search_helper(grid, word):
    """
    This function is a helper function for searching words horizontal and vertically.
    Parameters:
        grid - 2D grid of letters
        word - word to search for in grid
    Returns:
        final_pos - index of the the pos the word begins in the grid
    """
    final_pos = None
    for i in range(len(grid)):
        word_string = ""
        for char in grid[i]:
            word_string += char
        pos = word_string.find(word)
        if pos != -1:
            final_pos = (i + 1, pos + 1)
    return final_pos

def search_diagonal(grid, word):
    """
    This function searches for a word diagonally in the grid.
    Parameters:
        grid - 2D grid of letters
        word - word to search for in grid
    Returns:
        None or a tuple of the coordinates if the word is found.
    """
    height = len(grid)
    length = len(grid[0])
    for i in range(height):
        for j in range(length):
            if i + len(word) <= height and j + len(word) <= length:
                found = True
                for letter in range(len(word)):
                    if grid[i + letter][j + letter] != word[letter]:
                        found = False
                        break
                if found:
                    return (i + 1, j + 1)
                
            if i + len(word) <= height and j - len(word) >= 1:
                found = True
                for letter in range(len(word)):
                    if grid[i + letter][j - letter] != word[letter]:
                        found = False
                        break
                if found:
                    return (i + 1, j + 1)
    return None
    
def search(words_list, grid):
    """
    This function searches for all the possible words in the grid and creates a
    dictionary of all its correct positions.
    Parameters:
        words_list - list of all valid words in the dictionary
        grid - 2D grid of letters
    Returns:
        words_found - dictionary of all the words found in the grid and their positions
    """
    words_found = {}
    transpose = transpose_grid(grid)
    for word in words_list:
        horizontal_search = search_helper(grid, word)
        backwards_horizontal = search_helper(grid, word[::-1])
        if horizontal_search != None:
            if word not in words_found:
                words_found[word] = str((horizontal_search))
        if backwards_horizontal != None:
            if word not in words_found:
                words_found[word] = str((backwards_horizontal[0], backwards_horizontal[1] + len(word) - 1))
        
        vertical_search = search_helper(transpose, word)
        upside_down = search_helper(transpose, word[::-1])
        if vertical_search != None:
            if word not in words_found:
                words_found[word] = str((vertical_search[1], vertical_search[0]))
        if upside_down != None:
            if word not in words_found:
                words_found[word] =str((upside_down[1] + len(word) - 1, upside_down[0]))

        diagonal_search = search_diagonal(grid, word)
        if diagonal_search != None:
            if word not in words_found:
                words_found[word] = str(diagonal_search)
    return words_found

def check_validity(answer, word_bank):
    """
    This function makes sure the word inputed by user is valid.
    Parameters: 
        answer - user inputed word
        word_bank - list of all valid words
    Returns:
        boolean value T or F
    """
    if answer in word_bank:
        return True
    return False

def check_coordinate(coordinate, answer, word_bank):
    """
    This function checks to see if the coordinates for the user's answer
    when searching a word are correct.
    Parameters:
        coordinate - user inputed coordinate value
        answer - user inputed word to search
        word_bank - dictionary of correct words and their positions
    Returns
        boolean value T or F
    """
    for word in word_bank:
        if answer == word and coordinate == word_bank[answer]:
            return True
    return False

def print_grid(grid):
    """
    This function prints the 2D grid of letters.
    Parameters:
        grid - 2D list of letters
    Returns:
        None
    """
    for row in grid:
        print(' '.join(row))

def play_game():
    """
    This function carries out the gameplay, calls all the other functions necessary,
    and does complex error checking for the user.
    Parameters:
        None
    Returns:
        None
    """
    play_again = True
    while play_again == True:
        height = input("Enter a height for the grid: ")
        length = input("Enter a length for the grid: ")
        grid = create_grid(height, length)
        words_list = read_file("words.txt", height, length)
        print("Here is your letter grid:\n")
        print_grid(grid)
        word_bank = search(words_list, grid)
        if len(word_bank) == 0:
            print("No words found. Please enter new dimensions.")
        else:
            print("\nHere is your word bank:")
            for key in word_bank:
                print(key)

            num_guesses = 0
            num_words = len(word_bank)
            guessed_words = []
            word_bank_keys = list(word_bank.keys())
            while num_guesses < len(word_bank):
                answer = input("\nEnter a word from the bank when found: ")
                if answer in guessed_words:
                    print("Word already guessed. Please guess a new word")
                elif check_validity(answer, word_bank):
                    coordinate = input("Enter the starting coordinate of the word: ")
                    if check_coordinate(coordinate, answer, word_bank):
                        guessed_words.append(answer)
                        print("Correct! You found " + str(answer) + ". Good job!\n")
                        num_words -= 1
                        if num_words > 1:
                            print("You have " + str(num_words) + " more words to go!\n")
                            print("Grid:")
                            print_grid(grid)
                        elif num_words == 1:
                            print_grid(grid)
                            print("You have " + str(num_words) + " more word to go!\n")

                        remaining_words = []
                        for word in word_bank_keys:
                            if word not in guessed_words:
                                remaining_words.append(word)
                        if len(remaining_words) > 0:
                            print("\nWords left to find: ")
                            for word in remaining_words:
                                print(word)
                        num_guesses += 1
                    else:
                        print("Sorry, position incorrect. Please try again.\n")
                else:
                    print("Not a word in the grid. Please enter a valid word.\n")
            if len(remaining_words) == 0:
                print("\nGOOD JOB, you found all the words. YOU WIN!\n")
                user_answer = input("Do you want to play again? Answer yes or no: ")
                if user_answer == "no":
                    play_again = False
                    print("\nThanks for playing!\n")


def main():
    print("\nLets play WORD SEARCH!\n")
    print("DIRECTIONS:")
    print("Given the word bank, find the starting positions of the words by")
    print("entering the coordintes in the form: (row #, column #)")
    print("You will be asked to enter the word once you found one and")
    print("then to provide the position of where it is on the grid.")
    print("Words can be found on the grid horizontally, backwards, vertically,")
    print("upside down and diagonally. You will create the dimensions of your")
    print("letter grid by entering a height and width.\n")
    play_game()
main()
