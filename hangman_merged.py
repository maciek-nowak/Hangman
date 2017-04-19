from random import randint
import time
import datetime


def loading_files():
    database = open('countries_and_capitals.txt')   # loading capitals database
    databaseContent = database.read()
    database.close()
    listOfFileLines = databaseContent.splitlines()

    asciiFile = open('ascii1.txt')   # loading ascii graphic
    asciiGraphic = asciiFile.read()
    asciiGraphic = asciiGraphic.split('break')

    return listOfFileLines, asciiGraphic


def intro(asciiGraphic):
    """Animation of game title

    Args:
        asciiGraphic (list): List of strings (asciiGraphics).
    """

    for iterator in range(7):   # Game Intro
        print(chr(27) + "[2J")  # clear terminal screen
        print('\033[32m' + "Welcome in Nowak's Hangman!")
        print(asciiGraphic[iterator])
        time.sleep(0.6)
    input('\033[31m' + 'Hit enter to continue')


def print_lastgame_info(capital, country, attempt, life, timer):
    """Printing information about last game parameters.

    Args:
        capital (str): our chosen capital name
        country (str): name od country of chosen capital
        attempt (int): number of user guess attempts
        life (int): number of user lifes
        timer (float): duration of last game in seconds
    """

    print('Hidden capital name was: ' + '\033[33m', end='')
    for letter in capital:
        print(letter, end=" ")
    print('\033[31m' + 'of' + '\033[33m', country)
    print('\n' + '\033[31m')
    print("It took you" + '\033[33m', int(timer), '\033[31m' + "s.")
    if life > 0:
        print("You guessed after" + '\033[33m', attempt, '\033[31m' + "attempts" + '\n')


def guess_word(capital, life, wrongWords, numbUnguessed, hiddenCapital):
    """Check if user input is the same as our chosen capital and prints the information.

    Args:
        capital (str): our chosen capital name
        life (int): number of user lifes
        wrongWords (list): list of previous user wrong guessed capital names
        numbUnguessed (int): number of still unguessed letters in capital name

    Return:
        life (int): number of user lifes after guessing word
        numbUnguessed (int): number of still unguessed letters in capital name
        hiddenCapital (list): list of guessed letters in chosen capital with '_' in place of unguessed letter
    """

    guess = input('Guess a word: ' + '\033[34m')
    print('\033[31m')
    guess = guess.upper()
    if guess == capital:    # checking if word is correct
        print('correct')
        hiddenCapital = list(capital)
        numbUnguessed = 0
    else:
        print('not correct')    # loosing life
        life -= 2
        wrongWords.append(guess)
    return life, numbUnguessed, hiddenCapital


def guess_letter(capital, life, wrongLetters, hiddenCapital, numbUnguessed):
    """Check if user input is a letter included chosen capital and prints the information.

    Args:
        capital (str): our chosen capital name
        life (int): number of user lifes
        wrongLetters (list): list of previous user wrong guessed letters in capital name
        hiddenCapital (list): list of guessed letters in chosen capital with '_' in place of unguessed letter
        numbUnguessed (int): number of still unguessed letters in capital name

    Return:
        life (int): number of user lifes after guessing word
        numbUnguessed (int): number of still unguessed letters in capital name
        hiddenCapital (list): list of guessed letters in chosen capital with '_' in place of unguessed letter
    """

    guess = ''
    while len(guess) != 1:
        guess = input('Guess a letter: ' + '\033[34m')
        print('\033[31m')
        if len(guess) != 1:
            print('You have to type a letter!')
    guess = guess.upper()
    if guess not in capital:    # checking if letter is in capital
        life -= 1
        wrongLetters.append(guess)
        print("You haven't guessed a letter!")
    else:
        print("You guessed a letter!")
        indexOfLetter = 0
        for letter in capital:
            if guess == letter:
                if hiddenCapital[indexOfLetter] == '_':
                    numbUnguessed -= 1
                hiddenCapital[indexOfLetter] = letter
            indexOfLetter += 1
    return life, numbUnguessed, hiddenCapital


def single_game(numbUnguessed, capital, asciiGraphic, hiddenCapital, country):
    """Function continues until user correctly guess name of capital or user looses all lifes.
    Prints whole current game status and asks user what does he want to guess (letter or word).
    Starts proper function for guessing word or guessing letter.

    Args:
        numbUnguessed (int): number of still unguessed letters in capital name
        capital (str): our chosen capital name
        asciiGraphic (list): List of strings (asciiGraphics)
        hiddenCapital (list): list of guessed letters in chosen capital with '_' in place of unguessed letter
        country (str): name od country of chosen capital

    Return:
        life (int): number of user lifes after guessing word
        attempt (int): number of user guess attempts
    """

    attempt = 0
    life = 5
    wrongWords = []
    wrongLetters = []
    # secondary loop repeating guessing until user has got lives and capital is unhidden
    while life > 0 and numbUnguessed > 0:
        print(chr(27) + "[2J")  # clear terminal screen
        print(capital)  # only for developers
        print('\033[32m' + asciiGraphic[life + 7] + '\033[31m')
        print('You have:' + '\033[33m', life, 'lives' + '\033[31m' + '\n')
        print('Unguessed letters left:' + '\033[33m', numbUnguessed, '\033[31m' + '\n')

        print('Hidden capital name is: ' + '\033[33m', end='')  # prints hidden capital as letters (instead of list)
        for letter in hiddenCapital:
            print(letter, end=" ")
        print('\n' + '\033[31m')
        if life == 1:
            print("Hint: the capital of" + '\033[33m', country, '\033[31m')

        # prints unguessed letters as letters (instead of list)
        print('Previous unguessed letters: ' + '\033[33m', end='')
        for letter in wrongLetters:
            print("'" + letter + "'", end=" ")
        print('\n' + '\033[31m')

        print('Previous unguessed words: ' + '\033[33m', end='')  # prints unguessed words as words (instead of list)
        for word in wrongWords:
            print(word, end=" ")
        print('\n' + '\033[31m')
        letterOrWord = ''
        while letterOrWord != 'l' and letterOrWord != 'w':  # user chooses type of input (word or letter)
            letterOrWord = input('What do you want to type? Letter (l) or word (w): ')
        attempt += 1
        if letterOrWord == 'w':
            life, numbUnguessed, hiddenCapital = guess_word(capital, life, wrongWords, numbUnguessed, hiddenCapital)
        else:
            life, numbUnguessed, hiddenCapital = guess_letter(capital, life, wrongLetters, hiddenCapital, numbUnguessed)
    return life, attempt


def new_highscore_add(start, attempt, capital, timer):
    """Function which loads an existing highscore.txt as a list, turns it into a string and adds
        new score to that string.

    Args:
        start (float) : time of game start
        attempt (int) : stores information about in how many tries we guessed the capital
        capital (str) : a string of a capital to guess
        timer (float) : duration of a single game from start to finish

    Returns:
        highscoreContent (str) : string composed of highscore loaded from a txt file and new
                                score information

    """

    name = input('Type your name: ' + '\033[33m')    # loading highscore and merging with new highscore
    print('\033[31m')
    highscore = open('highscore.txt')
    highscoreContent = highscore.read()
    highscoreContent = highscoreContent.splitlines()
    highscore.close()
    for line in range(len(highscoreContent)):   # split highscoreContent string into list elements
        highscoreContent[line] = highscoreContent[line].split(' | ')
    date = str(datetime.date.today())
    newHighscore = name + ' | ' + date + ' | ' + str(int(timer)) + ' | ' + str(attempt) + ' | ' + capital + ' '
    newHighscore = newHighscore.split(' | ')
    highscoreContent.append(newHighscore)
    return highscoreContent


def highscore_sort_and_save(highscoreContent):
    """Function which sorts highscore list by time of a game, turns highscore list into
        string and then writes that string into a file.

    Args:
        highscoreContent (list) : a list of single game highscore lines (each line is a list of elements)

    Returns:
        highscoreReconstruct (str) : a string containing the same data as list highscoreContent, but sorted
                                        and turned into string
    """

    swaps = 1   # sorting highscore list by time
    while swaps > 0:
        swaps = 0
        for i in range(len(highscoreContent)-1):
            if float(highscoreContent[i][2]) > float(highscoreContent[i+1][2]):
                highscoreContent[i], highscoreContent[i+1] = highscoreContent[i+1], highscoreContent[i]
                swaps += 1
    if len(highscoreContent) > 10:
        highscoreContent = highscoreContent[:10]

    highscoreReconstruct = ''   # reconstructing string from list
    for line in highscoreContent:
        iterator = 0
        for word in line:
            highscoreReconstruct = highscoreReconstruct + word
            if iterator < len(line) - 1:
                highscoreReconstruct += ' | '
            iterator += 1
        highscoreReconstruct = highscoreReconstruct + '\n'

    highscore = open('highscore.txt', 'w')  # writing highscore to the file
    highscore.write(highscoreReconstruct)
    highscore.close()
    return highscoreReconstruct


def endgame(life, asciiGraphic, start, attempt, capital, country):
    """Function which checks winning conditions and prints information abt winning/losing and a highscore.

    Args:
        life (int):
        asciiGraphic (list): contains graphics loaded from a file
        start (float) : time of game start
        attempt (int) : stores information about in how many tries we guessed the capital
        country (str) : a string with a name of a country of capital we want to guess
        capital (str) : a string of a capital to guess
    """

    print(chr(27) + "[2J")  # clear terminal screen
    end = time.time()  # finish counting game time
    timer = end - start
    if life <= 0:       # checking winning conditions
        print('You have lost!')
        print('\033[32m' + asciiGraphic[7] + '\033[31m')
        highscore = open('highscore.txt')
        highscoreReconstruct = highscore.read()
        highscore.close()
    if life > 0:
        print('You won!')
        highscoreContent = new_highscore_add(start, attempt, capital, timer)
        highscoreReconstruct = highscore_sort_and_save(highscoreContent)

    print_lastgame_info(capital, country, attempt, life, timer)
    print_highscore(highscoreReconstruct)


def print_highscore(highscoreReconstruct):
    """Function which prints highscore.

    Args:
        highscoreReconstruct (str) : a reconstructed string containing whole highscore data.
    """

    print('\033[36m' + 'HIGHSCORE:' + '\n'*2)    # printing HIGHSCORE
    highscorelines = highscoreReconstruct.splitlines()
    print(6 * ' ' + 'USER NAME' + 12 * ' ' + 'DATE' + 5 * ' ' + 'T[s]' + ' ' + 'GUESSED CAPITAL')
    for hsline in range(len(highscorelines)):
            part = highscorelines[hsline].split(' | ')
            if hsline < 9:
                part[0] = ' ' * (20 - len(part[0])) + part[0]
            else:
                part[0] = ' ' * (19 - len(part[0])) + part[0]
            print(hsline + 1, end='')
            for element in part:
                print(element, end=' | ')
            print('')
    print('\n'*2 + '\033[31m')


def set_capital(listOfFileLines):
    """Function which chooses a random country&capital pair from loaded earlier file.

    Args:
        listOfFileLines (list) : a list made by opening our file with capitals and countries using splitlines(),
                                where each line consist of a country&capital pair

    Returns:
        country (str) : a string with a name of a country of capital we want to guess
        capital (str) : a string of a capital to guess
        hiddenCapital (list) : a list consisting of '_' strings, length of this list equals to length of capital
        numbUnguessed (int) : an int containing an information about a number of letters we need to guess
    """

    randomLine = listOfFileLines[randint(0, len(listOfFileLines)-1)]    # randomizing capital
    randomLineSplitted = randomLine.split(' | ')
    country = randomLineSplitted[0].upper()
    capital = randomLineSplitted[1].upper()
    hiddenCapital = ''
    numbUnguessed = 0
    for letter in capital:  # ' ' in capital name is always unhidden
        if letter != ' ':
            hiddenCapital += "_"
            numbUnguessed += 1
        else:
            hiddenCapital += ' '
    hiddenCapital = list(hiddenCapital)
    return country, capital, hiddenCapital, numbUnguessed


def main():
    listOfFileLines, asciiGraphic = loading_files()
    intro(asciiGraphic)

    again = 'yes'
    while again == 'yes':   # main loop repeating whole game until user requests
        country, capital, hiddenCapital, numbUnguessed = set_capital(listOfFileLines)
        print(chr(27) + "[2J")  # clear terminal screen
        print("Try to guess what capital I've got on my mind.")
        input('Hit enter to continue')
        start = time.time()  # start counting game time
        life, attempt = single_game(numbUnguessed, capital, asciiGraphic, hiddenCapital, country)
        endgame(life, asciiGraphic, start, attempt, capital, country)
        again = ''  # user decides if he want to play again
        while again != 'yes' and again != 'no':
            again = input("Do you want to play again? [yes / no]: ")


main()
