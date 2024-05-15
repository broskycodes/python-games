# A lot of different python libraries required to make this work
import random
import requests # requests takes in a url and turns the url's website to text
import bs4 # bs4 (BeautifulSoup 4) is the meat of the operation, it (web) scrapes all the data off the website text and compiles it
import pandas # Organizational tool

# To give the user some context while the code initalizes, almost like a UI
print('Guess the Population v1.2.1\n') # My attempt at software versioning
print('Initializing....')

# Dictionary contains all relavant lists   
data = {'City': [], 'State': [], 'Population': []}

# Using the wikipedia article for "List of United States cities by population"   
wiki_req = requests.get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')
soupy = bs4.BeautifulSoup(wiki_req.text, 'lxml') # Variable contains all the data ready to be parsed through

# This loop takes all 100 rows of relavant data from the list within the article, takes tha data, and adds it to the relavant lists    
for citnum in range(0, 100):
    citnum = citnum + 20
    # Parses through the 20th to 119th data point in the data [where the actual list is contained within the article]   
    citobj = soupy.select('tr')[citnum]
    objlist = citobj.select('td') # Each data point is a row within the original list

    # Takes three specific cells within each row, and assigns them as the city, state (abbv.), and population  
    cityname = objlist[0].text
    statename = objlist[1].text
    popnum = objlist[2].text

    # Formating the text in the data 
    if '[' in cityname:
        cityname = cityname[:-4]
    else:
        cityname = cityname[:-1]    
    statename = statename[:-1]
    popnum = popnum[:-1]

    # Adding each city to the list of cities   
    citylist = data['City']
    citylist.append(cityname)
    data['City'] = citylist

    # Each state to the list of states    
    statelist = data['State']
    statelist.append(statename)
    data['State'] = statelist

    # And each population to the list of populations    
    poplist = data['Population']
    poplist.append(popnum)
    data['Population'] = poplist

# And now, all the cooresponding data points within each list in the dictionary is organized    
cheatsheet = pandas.DataFrame(data)

# Defining how to calculate the score based on the guess and population
def score_calculate(guess, popnum):
    multiple = guess/popnum
    percent = abs(multiple-1)*100
    point = 100-percent
    if point < 0: # Prevents negative scoring
        point = 0
    point = round(point)
    return point    

# Defines the entire game loop, will be called at the end in while loop
def game_loop(cheatsheet):
    cityindexes = [] # Contains all previously used city indexes so there isn't a repeat
    points = 0 # Point counter

    # Marks beginning of game to player after initalization round    
    print('Welcome to guess the population!\n')

    # For each round... (There are 5)    
    for game in range(1, 6):
        print(f'Round {game}/5:\n') # Round marker

        # Picks random index and checks to see if unique    
        while True:
            index = random.randint(0, 99)
            if index in cityindexes:
                pass
            else:
                cityindexes.append(index)
                break

        # Using index picks out the correct list containing cooresponding city, state, pop.    
        guessrow = cheatsheet.iloc[index]

        # Assigns variables to each    
        cityname = guessrow['City']
        statename = guessrow['State']
        popnumb = guessrow['Population']
        popnum = popnumb.replace(',', '') # Removes commas in data
        popnum = int(popnum) # Converts population to integer

        # Asks user to guess the population (user input)    
        while True:
            # If error presents, keeps asking    
            try:
                guess = input(f'What is the population of {cityname}, {statename}?: ')
                guess = guess.replace(',', '') # Removes any user inputted commas
                guess = int(guess)
            except:
                print('Please input a valid number')
            else:
                break

        # Algorithm calculates points awarded based on how close the guess was, and adds to total    
        point = score_calculate(guess, popnum)
        points = points + point

        # Tells user results    
        print(f'The correct population of {cityname}, {statename} is {popnumb}')
        print(f'You get {point} points\n')

        # Tells user current score    
        print(f'Your current total is {points} points\n')

    # After all rounds, gives final score    
    print(f'Your final score is {points} points\n')

# Main game loop    
while True:
    # Runs every round and gives final score
    game_loop(cheatsheet)

    # Asks to repeat, if so, resets and stays in game loop        
    playmode = input('Do you want to play again y/n: ')

    # Defaults no if not yes        
    if playmode != 'y':
        break
    else:
        print('\n')    
