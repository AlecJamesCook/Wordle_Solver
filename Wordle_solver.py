##########################################
#~~~~~~~~~~ AUXILIARY FUNCTIONS ~~~~~~~~~#
##########################################

# The following functions were created in support of the next three applications

def file_opener(filename):

    """
    Opens a file and adds the contents to a list. Each item in the list has been split by the occurence of a '\n'
    """

    fin = open(filename)
    words_list = []

    for line in fin:
        word = line.strip("\n")
        words_list.append(word)
        
    return words_list

def green_position_builder(string):

    """ 
    Creates a dictionary with the string's letter's position as keys and the letters as values
    """

    position_dictionary = dict()
        
    for position, letter in enumerate(string):
        position_dictionary[position] = letter

    return position_dictionary

def yellow_position_builder(string):

    """ 
    Creates a dictionary with the string's letter's as keys and their positions as values
    """

    position_dictionary = dict()
        
    for position, letter in enumerate(string):
        if letter in position_dictionary:
            position_dictionary[letter].add(position)
        else:
            position_dictionary[letter] = {position}

    return position_dictionary

def gray_entries(dictionary, gray_set):

    """
    Compares the letters stored in a dictionary to letters in a set of gray letters. Returns false if gray letters are found in the dictionary, true if otherwise.
    """
    for key in dictionary:
        if dictionary[key] in gray_set:
            return False

    return True

def green_entries(dictionary, green_letters):

    """
    Compares the positions(keys) and letters(values) stored in the input dictionary and the green letters dictionary. If the exact number of both the keys and values matches it returns true. False otherwise.
    """
    
    total = 0

    # Checks whether the input dictionary shares the same keys and values as the green letters dictionary.
    for key in dictionary:
        if key in green_letters:
            if dictionary[key] == green_letters[key]:
                total += 1

    # Checks if the input dictionary contains the right amount of positions and letters
    if total == len(green_letters):
        return True
    else:
        return False
    
def yellow_entries(word, yellow_letters):

    """
    Checks if the letters of a word is in the yellow_letters dictionary. It then checks that the letters are not in a restricted position. If the letters are in the yellow dictionary, and they are not in a restricted position, returns true. False otherwise.
    """
        
    res = 0

    # Quick check to make sure the word contains all of the yellow letters
    for key in yellow_letters:
        res = word.find(key)
        if res < 0:
            return False

    # Goes through each letter in the word.
    #  Checks that the letter is in the dictionary, but is not in the restricted position.
    for i in range(0, len(word)):
        if word[i] in yellow_letters:
            for element in yellow_letters[word[i]]:
                if word[element] == word[i]:
                    return False
            
    return True

def wordle_set_generator(words_list, green, yellow, gray):

    """

    Returns a list of all words that meet certain criteria regarding their what letters are in the word and what position they are in.
 
    :param words_list: a list of words.
    :type: list

    :param green: A dictionary of positions (keys) and letters (values). A word should have the same letter in the same position to pass this criteria.
    :type: dictionary (keys are integers, values are strings)

    :param yellow: A dictionary of letters (keys) and positions (values). A word should have the same letters as this dictionary but NOT in the specified position to pass this criteria.
    :type: dictionary (keys are strings, values are sets of integers)

    :param Gray: A set of letters. A word should not have any of these letters in it to pass this criteria.
    :type: set

    :rtype: list
    :return: Contains a list of all the words that pass the criterion.

    """

    wordle_list = []
    for word in words_list:

        # Each word from the wordle list is broken into a dictionary as outlined above.
        word_position_dictionary = green_position_builder(word)

        # If the word passes the below functions, the no_of_matching_words variable is incremented.
        if gray_entries(word_position_dictionary, gray):
            if green_entries(word_position_dictionary, green):
                if yellow_entries(word, yellow):
                    wordle_list.append(word)

    return wordle_list

#################################################
#~~~~~~~~~~ END OF AUXILIARY FUNCTIONS ~~~~~~~~~#
#################################################


# Exercise 8 - Five Letter Unscramble
def word_assembler(s):
    """
    
    When given a string, this function determines how many unique five-letter words can be made out of
    the letters in the string. Uses a set of wordle words as the source of these five-letter words.

    :param s: Contains the letters to be used when looking for unique five-letter words. Each letter can only be used once.
    :type: string

    :rtype: int
    :return: The number of unique five-letter words found in the wordle list that contain only the letters given in the parameter s.

    """

    def histogram_builder(string):

        """ 
        Creates a dictionary with the letters of the string as keys and the number of times the letters appear in the string as their values. This function appeared in the lecture notes from the Python course, namely the dictionary lesson. Many thanks to Federico!
        """
        
        histogram_dictionary = dict()
        
        for letter in string:
            if letter not in histogram_dictionary:
                histogram_dictionary[letter] = 1
            else:
                histogram_dictionary[letter] += 1     
                
        return histogram_dictionary
    
    input_word_histogram = histogram_builder(s)
    words_list = file_opener("wordle.txt")
    counter = 0
    no_of_matching_words = 0

    for word in words_list:
        words_list_histogram = histogram_builder(word) 
        for letter in word:

            # This loop creates a histogram dictionary out of each word in the wordle list. 
            # It then compares it's keys to the input string histogram's keys.
            # If the keys are in both of the dictionary and the value the other value,the counter is incremented.
            if letter in input_word_histogram and words_list_histogram[letter] <= input_word_histogram[letter]:
                counter += 1
            
            # If the counter reaches 5, it has found a unique five-letter word.
            if counter == 5:
                no_of_matching_words += 1
                
        counter = 0

    return no_of_matching_words

# Exercise 9 - Wordle Set
def wordle_set(green,yellow,gray):

    """

    The function is given three parameters which are different classes of letters and positions. The function checks whether a word contains letters in the correct specified position (green), contains letters but NOT in a specified position (yellow), and doesn't contain a specified group of letters (gray). Returns the number of words that match these parameters.

    :param green: A dictionary of positions (keys) and letters (values). The word must contain the letters in the specified position.
    :type: dictionary (keys are integers, values are strings)

    :param yellow: A dictionary of letters (keys) and positions (values). The word must contain the letters, but NOT at the specified position.
    :type: dictionary (keys are strings, values are sets of integers)

    :param gray: Letters that must not be in the word.
    :type: set

    :rtype: int
    :return: The number of words found in the wordle list that match the conditions set by the three parameters.

    """

    words_list = file_opener("wordle.txt")
    no_of_matching_words = len(wordle_set_generator(words_list, green, yellow, gray))
    return no_of_matching_words

# Exercise 10 - One Step of Wordle
def wordle_best_match(green,yellow,gray):

    """

    The function further reduces the words obtained from exercise9 to find which of these words get the lowest scores (lowest scores indicating the best words or words that will return the smallest amount of other words from wordle.txt).

    :param green: A dictionary of positions (keys) and letters (values). The word must contain the letters in the specified position.
    :type: dictionary (keys are integers, values are strings)

    :param yellow: A dictionary of letters (keys) and positions (values). The word must contain the letters, but NOT at the specified position.
    :type: dictionary (keys are strings, values are sets of integers)

    :param gray: Letters that must not be in the word.
    :type: string

    :rtype: set
    :return: The set of words with the best score.

    """

    def wordle_score(candidate, reduced_set, green, yellow, gray):

        """

       Compares each word (candidate) against the other words in the reduced_set parameter in turn. The word being compared against the candidate is assumed to be correct. The values of green, yellow, and gray are updated accordingly. Using these updated values, a new search is done through the wordle list. The candidate that returns the lowest number of words is deemed to be the 'best' word (score = the amount of words returned). Returns a set of word/s that has/have the lowest score. 

        :param candidate: Word that is being compared against the rest of the reduced set. Is drawn from the reduced set one at a time.
        :type: string

        :param reduced_set: A list of words drawn from the criteria set in exercise9
        :type: list (each element is a string)

        :param green: A dictionary of positions (keys) and letters (values). The word must contain the letters in the specified position.
        :type: dictionary (keys are integers, values are strings)

        :param yellow: A dictionary of letters (keys) and positions (values). The word must contain the letters, but NOT at the specified position.
        :type: dictionary (keys are strings, values are sets of integers)

        :param gray: Letters that must not be in the word.
        :type: string

        :rtype: set
        :return: The set of words with the best score.

        """
            
        new_set = []

        for word in reduced_set:
            if word != candidate:
                new_set.append(word)

        # This will be used to store the score of each candidate word
        score_dictionary[candidate] = 0

        for word in new_set:

            # Creates deep copies of the original green, yellow, and gray            
            updated_green = copy.deepcopy(green)
            updated_yellow = copy.deepcopy(yellow)
            updated_gray = copy.deepcopy(gray)

            # Converts candidate into a dictionary for comparison (positions are keys, letters are values)
            green_candidate = copy.copy(green_position_builder(candidate))
            green_word = copy.copy(green_position_builder(word))

            # Adds new values to green by comparing candidate against a word from the reduced_set
            for key in green_word:
                if green_candidate[key] == green_word[key]:
                    updated_green[key] = green_word[key]

            # Converts candidate into a dictionary for comparison (letters are keys, positions are values)
            yellow_candidate = copy.copy(yellow_position_builder(candidate))
            yellow_word = copy.copy(yellow_position_builder(word))

            # Adds new values to yellow by comparing positions of letters in candidate and a word from the reduced_set
            for key in yellow_word:
                if key in yellow_candidate:
                    for candidate_value in yellow_candidate[key]:

                        # Checks if the key and value is in the green dictionary. If it is, we don't want to add it to the yellow dictionary
                        if candidate_value in updated_green and updated_green[candidate_value] == key:
                            continue
                        
                        # Updates the yellow dictionary by adding the letters and their positions that are in the word from the reduced_set, but are in the wrong position.
                        for word_value in yellow_word[key]:
                            if candidate_value != word_value:
                                if key in updated_yellow:
                                    updated_yellow[key].add(candidate_value)
                                else:
                                    updated_yellow[key] = {candidate_value}

            # If candidate has a letter that isn't in the word, place the word in the gray set
            for key in yellow_candidate:
                if key not in yellow_word:
                    updated_gray.add(key)

            # Passes the new green, yellow, and gray values into wordle_set_generator
            # The size of the list is the score of the candidate from this round of the loop
            # The score for each candidate is store in score_dictionary
            redux_list = (wordle_set_generator(new_set, updated_green, updated_yellow, updated_gray))
            set_size = 0
            set_size += len(redux_list)
            score_dictionary[candidate] += set_size

        # Finds the lowest score(s) in the dictionary
        baseline_score = min(score_dictionary.values())

        best_words = {}
        best_words = set()

        # Candidates have the lowest score, they are added to a new set of lowest scoring words
        for key in score_dictionary:
            if score_dictionary[key] == baseline_score:
                best_words.add(key)

        # Returns a set of the lowest scoring words from the entirety of the wordle list
        return best_words

    words_list = file_opener("wordle.txt")
    reduced_set = wordle_set_generator(words_list, green, yellow, gray)
    score_dictionary = {}
    
    # Loops through the function passing each word in turn into the candidate parameter
    for word in reduced_set:
        lowest_scoring_word_set =(wordle_score(word, reduced_set, green, yellow, gray))
    
    return lowest_scoring_word_set