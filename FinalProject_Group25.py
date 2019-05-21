# Colin Clarke, Kyle Kulsakdinun, Victoria Pusung
import random, string

helper_grid = []
for num in range(65, 75):
    r = []
    r.append(chr(num)+' ')
    for n in range(10):
        r.append('-')
    helper_grid.append(r)  # creating a blank helper_grid
final_grid = []
guessed_hits = []
ship_coordinates = []
column_coordinates = [chr(x) for x in range(65, 75)]


def battleship():
    name = input('Enter your name: ')
    print('Welcome to Battleship, {}!'.format(name))
    play_game()


def play_game():
    global helper_grid, final_grid, guessed_hits, ship_coordinates, result
    ship_coordinates = place_ships()   # stores 2-D list of ship coordinates into a variable. each element is a ship
    while True:
        print('-' * 30)
        cleaned_guess = clean_guess(input('Enter a guess: '))
        if cleaned_guess == "Show":
            print_grid(final_grid)
        elif cleaned_guess in guessed_hits:  # double hits
            print('You have already hit ship with this coordinate! Please try again')
        else:
            result = check_guess(cleaned_guess)  # if the guess is a hit... # 1 = hit
            if result > 1:  # if you sink a ship...
                print('Hit at {}!'.format(cleaned_guess))
                print('You sunk ship {}!'.format(chr(result)))
                guessed_hits.append(cleaned_guess)  # append coord into guessed_hits
            elif result == 0:
                print('Miss at {}'.format(cleaned_guess))
            else:
                print('Hit at {}!'.format(cleaned_guess))
                guessed_hits.append(cleaned_guess)
            if len(guessed_hits) == 17:  # if the user wins. 17 elements = 17 coordinates all 5 ships take up
                print('You have won! Thank you for playing! Here is the final board: ')
                print_grid(final_grid)
                quit()
            else:
                make_helper_grid(cleaned_guess)  # pass coordinate into function then print after modification
                print_grid(helper_grid)


def clean_guess(guess):
    if guess == "show" or guess == "Show":
        return "Show"   # returns the string Show if user enters the show
    else:
        cleaned_guess = ''  # creates empty string for the cleaned guess
        upper_guess = guess.upper()
        trip = 0
        for i in upper_guess:
            if i in column_coordinates and trip == 0:
                # takes letters from possible column_coordinates into cleaned_guess, converts to uppercase
                cleaned_guess += i
                trip += 1
            elif i in string.digits:
                cleaned_guess += i  # takes numbers into cleaned_guess
    return cleaned_guess


def check_guess(cguess):
    for ship in ship_coordinates:
        if cguess in ship:
            if len(ship) == 1:  # this is the last coordinate of the ship which means we sunk it.
                return ship_coordinates.index(ship) + 65    # returns ASCII code of the ship if guess sinks the ship
            ship.pop(ship.index(cguess))  # if guess is a hit, pop from the list ship_coordinates
            return 1    # returns 1 if guess is a hit
    return 0    # returns false if guess is a miss


def make_helper_grid(coord):  # modifying helper grid. Does not return anything. X for every hit O for every miss
    global helper_grid, result  # coord is a cleaned_guess
    if result > 0:
        for rows in helper_grid:  # rows are ['A', '-', '-', etc.]
            if coord[0] == rows[0][0]:  # finding guessed row. rows[0][0] removes space from letter
                helper_grid[ord(coord[0])-65][int(coord[1:])] = 'X'  # finding guessed column and replacing '-' with hit
    else:   # if it's a miss
        for rows in helper_grid:
            if coord[0] == rows[0][0]:
                helper_grid[ord(coord[0]) - 65][int(coord[1:])] = 'O' # finding guessed column and replacing '-' with miss


def place_ships():  # Returns a 2d list of the coordinates and calls function make_final_grid
    global final_grid
    # First we make a 2d list of the coordinates of each ship. We start by randomly picking a starting point, and 2
    # direction elements. One direction element determines vertical or horizontal and the other determines whether we
    # move up or down for vertical or move left or right for horizontal. For each coordinate we check that it's within
    # the board space and that it's not already taken by another ship. If either of these checks fail, we restart the
    # process until we get a full valid ship. Then we increment the ship length and do the same thing for a longer ship.
    ship_list = []
    ship_length = 2
    second_three = 0
    while ship_length < 6:
        restart = ''
        ship = []
        direction = [random.randint(0, 1), random.randrange(-1, 2, 2)]
        point = [random.randint(65, 74), random.randint(1, 10)]
        for length in range(ship_length):
            coord = point[direction[0]] + direction[1]
            if coord in range(1, 11) or coord in range(65, 75):
                point.pop(direction[0])
                point.insert(direction[0], coord)
                coord = '{}{}'.format(chr(int(point[0])), point[1])
                if sum([x.count(coord) for x in ship_list]) == 0:
                    ship.append(coord)
                else:
                    restart = 1
                    break
            else:
                restart = 1
                break
        if restart:
            continue
        ship_list.append(ship)
        # This if statement allows us to generate another 3-length ship
        if ship_length == 3 and second_three == 0:
            second_three = 1
            continue
        ship_length += 1
    make_final_grid(ship_list)
    return ship_list


def make_final_grid(s_list):
    # This function uses the position of the ships as given by place_ships() to create the final grid that comes up when
    # the user types 'show' or when the game ends. To do this, first we make a list where the first 2 numbers are the
    # ascii position of the letter followed by the number of the coordinate minus 1. We subtract 1 so that when using
    # the "in" operator, coordinates with number 10 won't be flagged as 1. We then make the grid normally but checking
    # if we need to add in a ship letter each time instead of a dash. The letter of the ship is determined by the index
    # it was found at. This function modifies a global variable and doesn't return anything.
    global final_grid
    num_list = []
    for ship in s_list:
        for coord in ship:
            num_list.append(str(ord(coord[0]))+str(int(coord[1:])-1))
    for row in range(65, 75):
        r = []
        r.append(chr(row) + ' ')
        for column in range(10):
            num_coord = '{}{}'.format(row, column)
            if num_coord in num_list:
                index = num_list.index(num_coord)
                if index in range(2):
                    r.append('A')
                elif index in range(2, 5):
                    r.append('B')
                elif index in range(5, 8):
                    r.append('C')
                elif index in range(8, 12):
                    r.append('D')
                elif index in range(12, 17):
                    r.append('E')
            else:
                r.append('-')
        final_grid.append(r)


def print_grid(grid):
    # The grid that this function takes as an argument must be a 2d list, where the lists are the rows of the grid. The
    # top row of 1 2 3... is automatically added. This function prints out the grid that was passed to it as an
    # argument. In practice, it prints both the helper grid and final grid.
    first_row = [x for x in range(1, 11)]
    print('   ', end='')
    for coord in first_row:
        print(coord, end=' ')
    print()
    for row in grid:
        for coord in row:
            print(coord, end=' ')
        print()


if __name__ == "__main__":
    battleship()
