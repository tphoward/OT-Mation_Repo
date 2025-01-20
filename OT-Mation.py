# Author(s): Alex Laverick
# Last modified: 10:50, 16/03/2023
# Python 3.10.0 me thinks
#####################################################################################################################################

import pandas
import csv

###################################################################################
# File Names, these are the four csv files the protocol is generated from and the name of the output file. Currently these all need to be within the same working directory as the virtual environment
# The working directory is the same folder space as where this script is being run from., so this script and the four csv files will need to be in the same folder. The output script will then be output into the same folder.
Exp_parameters = "Experimental Parameters.csv"         # The csv that contains the experimental parameters (the various samples to be assembled etc.)
Stock_inventory = "Stocks.csv"            # csv file containing the details of the stock solutions to be put ino the OT-2 for the experiment
Pipette_settings = "Pipettes.csv"         # Settings for the pipettes to be used in the experiment (Which pipettes as well as attached tip boxes and trash containers)
Labware_definitions = "Labware.csv"       # Details of the labware to be included in the experiment, such as which plates are for mixing or the final location for samples
replicates = 1                                  # Declares the number of replicates for the experiment, replicates must be at least 1
                                                # Currently the replicates variable is only a place holder. Need to move this to the csv files so the user can more easily decide how many replicates they want in their protocol
Output_file = "Example_Output_Script.py"  # The name of the output script. A new file will be created, or overwrite an existing file with the same name

###################################################################################
# Function Definitions


def file_len(fname):                                                # Defines a function to calculate the total number of lines in a file
    """Calculates the number of lines in a file."""
    with open(fname) as f:                                          # Opens the file stored in the variable fname (this variable is adjustable to the input specified by the user)
        for i, l in enumerate(f):                                   # Enumerates through the file line by line
            pass                                                    # The loop does nothing other than counts the lines
    return i + 1                                                    # The enumerate counts the first line as 0 so the total needs to be increased by  to get a full iteration


def labware_sort(plate):                                            # Defines a function for determining which labware should be written into the protocol
    """Finds which labware matches the call made
    to the function (Source, Mixing or Final)."""
    global containers                                               # Calls the global dictionary containers as this is where the labware pulled form the labware csv is stored
    for key in containers:                                          # Iterate through the containers dictionary as this is where the labware is imported from the 'Labware' csv
        if containers[key][plate].lower() == 'y':                   # If a piece of labware has a key with a value y that matches the call to the function
            return key                                              # Return the variable the labware is saved under. This is so the labware can be written into the protocol


def eval_sort(string):                                              # Declares a function for writing a dictionary, to a file
    """Enables the writing of String keys as variable
    calls into the output file."""
    global containers                                               # Uses the dictionary containers from the global environment rather than a locally scoped containers
    for key in containers:                                          # Iterates through the containers dictionary, one labware at a time
        if key == string:                                           # If the key in the dictionary matches the string passed to the function as a query
            return key                                              # Returns the key so it cna be written to the file in a non-string format


def role_calc(z):                                                   # Defines a function for the calculation of what role a piece of labware fulfills (Source, Mixing, Final)
    """Iterates through the dictionary to identify any
    labware allocated for mixing samples."""
    for key in z:                                                                   # Iterates through the dictionary passed to the function key by key
        if z[key]['Mixing'].lower() == 'y' and z[key]['Source'].lower() == 'n':                                       # If the labware stored in the dictionary is marked as a container for mixing
            return "Mixing"                                                                                           # The function returns "Mixing" as this is th eidentification of the plate
        if z[key]['Mixing'].lower() == 'y' and z[key]['Source'].lower() == 'y'and z[key]['Final'].lower() == 'y':     # If the labware is marked as both a source and a mixing plate, it is probably a serial dilution
            return "Serial"                                                                                           # Returns "Serial" as the labware has been calculated as a serial dilution
        if z[key]['Mixing'].lower() == 'y' and z[key]['Source'].lower() == 'y' and z[key]['Final'].lower() == 'n':    # If the labware is for mixing and acts a source of a reagent, but is not the final destination, the labware is specified as a serial dilution needing a transfer into a plate
            return "Serial Plate"                                                                                     # Returns "Serial Plate" as the labware being calculated for a serial dilution before a transfer
    return "Final"                                                                                                    # If no labware has a special flag the function returns "Final" indicating this is the final plate for transfer

###################################################################################
# REAGENTS AND OT-2 INVENTORY

df = pandas.read_csv(Stock_inventory, header=0)       # pandas.read_csv is what finds the file, data can be parsed in specified ways, data series do not preserve data types
dictionary = {}                                       # Empty dictionary for storing other dictionaries within, will be populated with information from the csv file
columns = list(df)                                    # Columns is populated with the columns from the data frame, saved as a list that can be iterated through
n = 0                                                 # Acts as a counter for determining how many rows back the media compositions of reagents needs to refer to
df = df.fillna("True")                                # Replaces the NaN values (empty cells) with a specified entry to filter absent data

# READS THE TEMPLATE FILE THAT CONTAINS THE PHYSICAL PARAMETERS OF THE EXPERIMENT  TODO Why does the components file need multiple rows for sample in order to correctly write out the dictionary???? This is where the multiple rows being needed issue is being generated from, this or the one that automatically fills out each row on the behalf of the user
for index, row in df.iterrows():                                            # Index is not a callable counter as exceeds data-frame limits, but it is required otherwise the loop cannot iterate properly
    if row[0] == "True":                                                    # If the cell is empty ('True' is the specified entry for absent data)
        n = n+1                                                             # As the number of rows iterated through increases, the further back the reference row is, this increases the call distance
        dictionary[df.iloc[index-n][0]][row[1]] = {}                        # creates a new dictionary based on positional indexing (.iloc)
        for column in columns[2:]:                                          # For the first columns
            dictionary[df.iloc[index-n][0]][row[1]][column] = row[column]   # uses positional indexing to add entries to dictionaries
    else:                                                                   # If the first cell in a row is not 'True'
        dictionary[row[0]] = {}                                             # Generates an empty dictionary to store what reagent has been encountered
        dictionary[row[0]][row[1]] = {}                                     # Generates a dictionary for the media's found in the reagent dictionary
        n = 0                                                               # There needs to be a counter for how many rows are iterated through before a new reagent is reached. This sets the counter to 0
        for column in columns[2:]:                                          # Columns contains all the columns of the data frame in a list allowing it to be iterated through. The columns loop is inside the row loop so the columns can be iterated on a row by row basis
            dictionary[row[0]][row[1]][column] = row[column]                # A new key is created inside the sub dictionaries based on the current column, the corresponding data in that column in relation to the row is then stored as the value

####################################################################################
# JMP/CSV FILE READING LOOP (EXPERIMENTAL PARAMETERS)
JMP = pandas.read_csv(Exp_parameters, header=0)                                                                  # Creates a data-frame called JMP from the csv output from JMP
for column in JMP:                                                                                               # Iterates through the columns of the dictionary in order to read the top cell of each one. The top cell will contain what reagent parameter the column pertains to
    row_count = sum(1 for row in JMP.iterrows())                                                                 # This counts the number of rows in the csv file, as the number of rows is equal to the number of medias, skip row 0 as this is headers
    if column in dictionary.keys():                                                                              # If the header of the column is present in the dictionary that was previously generated it is one of the parameters that reagent needs to be included
        for i in range(row_count):                                                                               # Iterates through each of the rows in the csv file, each row is essentially a media
            if "Sample {}".format(i) in dictionary[column].keys():                                               # If there is already a media present in the dictionary that has a key matching the
                dictionary[column]["Sample {}".format(i)]["Target Concentration"] = JMP.iloc[i][column]          # Extract the value for the concentration of the reagent in the media for the existing media keys, this should not require back tracking
            else:                                                                                                # If a media dictionary for this media doesn't exist, create one. A dictionary for the media needs to be created before it can be populated with keys
                dictionary[column]["Sample {}".format(i)] = {}                                                   # The medias need to a have a dictionary declared before keys can be examined whether they are present or not. Otherwise a crash occurs
                for key in dictionary[column]["Sample 1"]:                                                       # Iterates through a known completed dictionary to check if any information is missing from the generated dictionary (like well location)
                    if key not in dictionary[column]["Sample {}".format(i)].keys():                              # Checks the generated dictionary against an existing dictionary to see if any of the dictionary is missing
                        dictionary[column]["Sample {}".format(i)][key] = dictionary[column]["Sample 1"][key]     # Copies the information from the known, completed dictionary into the areas
                        dictionary[column]["Sample {}".format(i)]["Target Concentration"] = JMP.iloc[i][column]  # Extracts the concentration value of the reagent for this particular well
# TODO Either the error is coming from the csv file or there is an error being introduced in this particular loop. The True is being introduced as a sample not a reagent so the issue comes from an erroneous row
###################################################################################
# TOOLS
pipettes = pandas.read_csv(Pipette_settings, header=0)  # Reads the csv named in Pipette_settings, identifying row 0 as the header row, saving data from the csv to the variable pipette (dataframe)
tools = {}                                              # Initialises a dictionary to the tools variable,data extracted from pipettes will populate the dictionary
tcolumns = list(pipettes)                               # Lists the columns in the pipette data-frame
pipettes = pipettes.fillna("True")                      # Fills the blank spaces in the data-frame pulled from the tools.csv

for index, row in pipettes.iterrows():        # Loop for iterating through the data saved into the pipettes dataframe from the Tools.csv file
    tools[row[0]] = {}                        # Creates a new dictionary using the data found on the row of the csv as a key
    for column in tcolumns[1:]:               # For each column in the csv file
        tools[row[0]][column] = row[column]   # Saves the data found in the column to the tools dictionary
# Could an If-else loop be implemented in order to circumvent the need for the user to specify a collection of two pipettes from use within the
###################################################################################
# LABWARE
labware = pandas.read_csv(Labware_definitions, header=0)  # Opens the labware csv file, saving the contents into the labware variable
containers = {}                                           # Declares a new empty dictionary into a variable containers
tcolumns = list(labware)                                  # Creates a list composed of all the column headers found within the csv file
labware = labware.fillna("True")                          # Replaces any invalid entries (NaN) with the string 'True'

for index, row in labware.iterrows():                     # Iterates through the rows stored in the labware variable
    containers[row[0]] = {}                               # Declares a new dictionary within the containers dictionary
    for column in tcolumns[1:]:                           # For each column within the .csv file
        containers[row[0]][column] = row[column]          # Add a new value to the correct key position within the dictionary

################################################################################## The below block of code is for the writing of the main code blocks into the output scrpt parsed by the OT-2
# DECLARATIONS AND PIPETTE ASSIGNMENT, Pipette assignment is sensitive to the orientation that pipettes are provided into the robot, i.e.e change the csv is probably the path of least resistance when it comes to modifications
with open(Output_file, 'a+') as file:                                                                                                 # Opens the named file, if a file with that name is not found, one is made. a opens in append mode
    file.seek(0)                                                                                                                      # Sets the position of the read and write cursor to the beginning of the file (append method starts at the end of the file
    file.write('from opentrons import protocol_api\nimport random\n\n')                                       # Writes the import statements into the script, the protocol must include the opentrons import module or the robot won't read it correctly
    file.write('metadata = {"protocolName":"My Protocol",\n   "author": "OT-Mation",\n   "description": "debugging script for OT-Mation",\n   "apiLevel": "2.10"}\n\n') # PLACEHOLDER METADATA SECTION
    file.write('def run(protocol: protocol_api.ProtocolContext):\n   ')
    for key in containers:                                                                                                            # Iterates through each key in the dictionary containers, each key is a labware that will need a declaration written into the protocol
        file.write(key + ' = protocol.load_labware("{}", location={})\n   '.format(containers[key]['Labware'], containers[key]['Slot']))              # Writes each key in the containers dictionary to the protocol as a labware declaration
    file.write('def pip_use(x):\n      ' + 'nonlocal pipette\n      ' + 'q = pipette1\n      ' + 'r = pipette2\n      ' +                           # Defines the function that selects which pipette to use for a transfer
               'if q.min_volume > r.min_volume:\n         ' + 'big = q\n         ' + 'small = r\n      ' +                                     # Checks the minimum volumes of the pipettes against each other to sort which is the large and which is the small
               'else:\n         ' + 'big = r\n         ' + 'small = q\n      ' +                                                               # Compares minimum volumes of the two mounted pipettes to determine which is the larger of the two
               'if x < big.min_volume:\n         ' +                                                                                     # If the volume to be transferred is below the minimum volume of the pipette
               'pipette = small'+'\n      ' + 'else:'+'\n         ' + 'pipette = big'+'\n   '+'\n   ' + 'def diluent_find():\n      ' +              # Assigns which pipette to use based on the volume comparison of the two pipettes
               'for key in components:\n         ' + 'for k in components[key]:\n            ' +                                            # Iterates through the components dictionary to find the reagent marked with a Diluent flag
               'if components[key][k]["Diluent"].lower() == "y":\n               ' + 'return components[key][k]["Well Location"]\n   '+     # Returns the location of the diluent to dilute down the other reagents that need it
               'def well_blacklist(x):\n      ' + 'temp_variable = x\n      ' + 'escape = 0\n      ' + 'nonlocal blacklist\n      ' +# +  ***decreased spaces by 3***              # Defines the function for checking if a well or list of wells is in the well blacklist
               'nonlocal dup_list\n      ' + 'try:\n         ' + 'for i in x:\n            ' + 'print(i)\n      ' + 'except(TypeError):\n         ' +  # Calls the global dup_list to prevent the same legal well being chosen for multiple samples
               'while escape == 0:\n            ' + 'if {}.wells(temp_variable) in blacklist or temp_variable in dup_list:\n               '.format(labware_sort("Final")) +    # Sets the escape clause and finds the final plate where samples are being transferred/assembled into
               'temp_variable = temp_variable + 1\n            ' + 'else:\n               ' + 'escape = 1\n               ' + 'dup_list.append(temp_variable)\n         ' +           # Increments temp_variable in response to the blacklist comparison
               'return(temp_variable)\n      ' + 'else:\n         ' + 'for q, i in enumerate(x):\n            ' + 'escape = 0\n            ' +             # Returns temp variable if the initial input was a single well, if the input was a list the enumeration loop is used instead
               'while escape == 0:\n               ' +                                                                                            # Starts the while loop to iterate the well values passed to the function against a known list of wells to not use
               'if {}.wells(temp_variable[q]) in blacklist or temp_variable[q] in dup_list:\n                  '.format(labware_sort("Final")) +  # Compares the passed values against the blacklist but also against dup_list which is populated during the loop, this is to prevent a well being selected for use more than once
               'temp_variable[q] = temp_variable[q] + 1\n               ' + 'else:\n                  ' +                                            # Increments the well value by 1 if it is in the blacklist or the dup_list
               'dup_list.append(temp_variable[q])\n                  ' + 'escape = 1\n         ' + 'return(temp_variable)\n   ' +                       # Once a legal well is found it is appended to the dup_list to prevent it being selected again
               'blacklist = {0}.columns(0) + {0}.columns(-1) + {0}.rows(0) + {0}.rows(-1)\n   '.format(labware_sort("Final")) + 'dup_list = []\n   ')   # Assigns wells to the blacklist variable, By defaults this blacklist prevents the use of the outside wells of the final labware in the experiment
    file.write('replicates = {}\n   '.format(replicates) + 'def chunks(lst, n):\n      ' + 'temp = []\n      ' +                       # Defines a function for breaking down a list into sublists of a specified length
               'for i in range(0,len(lst),n):\n         ' + 'temp.append(lst[i:i + n])\n      ' + 'return(temp)\n   ')                 # loops around  number of times equal to user specified input and then compiles a list of assembled chunks from the main list
    file.write('well_list = []\n   ' + 'well_counter = 0\n   ' + 'def randomiser(x):\n      ' + 'nonlocal well_list\n      ' +              # Declares well_counter and well_list for a list of random well generations to populate the variables
               'nonlocal well_counter\n      ' + 'nonlocal replicates\n      ' + 'if replicates == 1:\n         ' + 'pass\n      ' +        # Calls several global variables, this bypasses the need to return variables as they cna be directly manipulated outside the local scope of the loop
               'else:\n         ' + 'well_counter = [int(x) for x in str(well_counter)]\n         ' +                               # If there is a number of replicates, well_counter needs to be a list to store all the wells rather than an integer, this code converts the by default well_counter integer into a list
               'for q, i in enumerate(range(replicates)):\n            ' + 'if len(well_counter) < replicates:\n               ' +  # An enumeration loop limited by the number of replicates the user wants in their protocol
               'well_counter.append(q)\n      ' + 'for key in x:\n         ' +                                                      # Iterates through the loop, testing the length of well_counter against the number of replicates, this is to ensure the correct number of wells is in the list for sample placement
               'well_counter = well_blacklist(well_counter)\n         ' + 'if replicates == 1:\n            ' +                     # The .extend() function only works if the item to be appended to the list contains more than a single entry. As a single replicate will only contain a single value, there needs to be an if statement that sorts between which method to use, append or extend
               'well_list.append(well_counter)\n         ' + 'else:\n            ' + 'well_list.extend(well_counter)\n      ' +     # Checks the entries in well_counter against the blacklist, adjusting them as appropriate to create legal entries that fit the number of replicates the user specified
               'random.shuffle(well_list)\n      ' + 'key_list = []\n      ' + 'print_out = {}\n      ' +                           # Shuffles well list so that the position of samples is randomised to improve experimental fidelity
               'for key in x:\n         ' + 'key_list.append(key)\n      ' + 'if replicates > 1:\n         ' +                      # Appends all the keys in the dictionary passed to randomiser into a list
               'well_list = chunks(well_list, replicates)\n      ' + 'for i, key in enumerate(key_list):\n         ' +              # If a number of replicates has been specified, the list of legal well placements is broken down into a main list of sublists with each sublist representing the wells designated for each sample
               'print_out[key] = well_list[i]\n      ' + 'with open("Randomisation.txt", "+a") as file:\n         ' +               # Assigns the wells from the well_list to the print_out dictionary, this can then be exported and written into the print out file, keeping the user informed as to where their samples are on the plate
               'file.write("Sample placement has been randomised as follows:\\n\\n" + "{}\\n".format(print_out) + "\\n" +' + '\n      ' +  # Writes the print_out dictionary into the randomisation.txt output file. Randomisation contains the information such as which samples have been moved into which wells
               '"Sample number refers to the row within the {} file. Location number is the well via zero indexing (0 = A1, 1 = B1 etc.)")\n   \n   '.format(Exp_parameters))  # Text layout for the contents of Randomisation.txt
    file.write('replicates = {}\n   '.format(replicates))
    file.write('pipette1 = protocol.load_instrument(instrument_name="{}",'.format(tools['Pipette']['Pipette 1']) + '\n       ' + 'mount="{}",'.format(tools['Mount']['Pipette 1']) + '\n       ' + 'tip_racks=[{}])'.format(tools['Tip Rack']['Pipette 1']) + '\n   ')               # Writes the pipettes and their calibrations to the protocol from the tools dictionary made from the tools csv
    file.write('pipette2 = protocol.load_instrument(instrument_name="{}",'.format(tools['Pipette']['Pipette 2']) + '\n       ' + 'mount="{}",'.format(tools['Mount']['Pipette 2']) + '\n       ' + 'tip_racks=[{}])'.format(tools['Tip Rack']['Pipette 2']) + '\n   ')                                       # Writes the details of the second pipette to the protocol. This may break if only one pipette is declared...
    file.write('pipette = pipette1' + '\n   ')                                                                                         # Sets pipette1 as the default value for the global pipette variable (which will be used to control which pipette is being used at the time
    file.write('pipette1.flow_rate.aspirate = {}'.format(tools['Aspirate Rate']['Pipette 1']) + '\n   ' +
               'pipette1.flow_rate.dispense = {}'.format(tools['Dispense Rate']['Pipette 1']) + '\n   ')
    file.write('pipette2.flow_rate.aspirate = {}'.format(tools['Aspirate Rate']['Pipette 2']) + '\n   ' +
               'pipette2.flow_rate.dispense = {}'.format(tools['Dispense Rate']['Pipette 2']) + '\n   ')
    file.write('components = {}\n   \n   '.format(dictionary))  # Writes the components dictionary declaration to the protocol file before populating the declaration with data.
    file.write('containers = {}\n   \n   '.format(containers))  # writes the containers dictionary declaration to the file before populating the declaration with data
###################################################################################
# STEP CALCULATION AND PROTOCOL CONSTRUCTION # For the updated No_sample method, need to check the volume tracking and well location designation
with open(Output_file, 'a+') as file:  # Opens the file saved into Output_file to write in the protocol steps, and then examine well tracking procedures
    # Destination assignment
    if role_calc(containers) == "Final":                                                                                                    # Checks to see if the samples are going to be moved out of the mixing plate or not
        file.write('No_sample = {}\n   ' + 'well_assign = 0\n   ' + 'for key in components:\n      ' +                                               # Writes a dictionary for storing the location and volume of samples assembled
                   'for k in components[key]:\n         ' + 'if k in No_sample.keys():\n            ' + 'pass\n         ' +                          # Checks if the sample key is present in the dictionary, if it isn't an entry for the sample is made
                   'else:\n            ' + 'No_sample[k] = {}\n            ' + 'No_sample[k]["Location"] = well_assign\n            ' +   # Creates a dictionary entry in No_sample and initialises an empty list for compiling well locations
                   'No_sample[k]["Volume"] = 0\n            ' + 'well_assign = well_assign + 1\n   ')                # Loops a number of times equal to the users specification, adding wells to list for the samples
    else:                                                                                                                                   # Final needs a different form of well assignment than Mixing, this is because samples are being constructed in triplicate rather than a master mix being made up and dispensed out
        file.write('No_sample = {}\n   ' + 'well_assign = 0\n   ' + 'for key in components:\n      ' + 'for k in components[key]:\n         ' +  # Writes a dictionary to the protocol where the location for sample mixing can be saved (location is assigned via zero indexing)
                   'if k in No_sample.keys():\n            ' + 'pass\n         ' + 'else:\n            ' + 'No_sample[k] = {}\n            ' + 'No_sample[k]["Location"] = well_assign\n            ' +  # Saves a location value to a sub dictionary within the main dictionary that acts like an address for the final solution
                   'No_sample[k]["Volume"] = 0\n            ' + 'well_assign = well_assign + 1\n   ' + '\n   ')                               # Saves volume to the location data as a means to calculate final concentrations of solutions, well_assign also increases in order to assign more wells
    # Volume Calculation
    file.write('for key in components:\n      ' + 'for k in components[key]:\n         ' + 'if components[key][k]["Diluent"].lower() == "y":\n            ' + 'pass\n         ' + 'else:\n            ' +  # writes a loop with a pass case for diuents, water should be included sa a reagent but not treated as being experimental
               'if components[key][k]["Transfer Volume"] == "True":\n               ' + 'if components[key][k]["Percent"].lower() == "y":\n                  ' +         # Writes the algorithm for calculating percentage based concentrations of the final solution
               'if components[key][k]["Target Concentration"] < 1:\n                     ' +    # Percentages may be given as a whole number or decimal, script needs to account for both
               'components[key][k]["Transfer Volume"] = (components[key][k]["Target Volume"]*components[key][k]["Target Concentration"])\n                  ' + 'else:\n                     ' +  # If the percentage is given as a decimal, the division by 100 for the standard calculation is no longer needed
               'components[key][k]["Transfer Volume"] = (components[key][k]["Target Volume"]*((components[key][k]["Target Concentration"])/100))\n               ' +  # Calculates the volume of a reagent required based on percentage concentrations of reagents
               'else:\n                  ' + 'if components[key][k]["Mass per ul"].lower() == "y":\n                     ' +  # If not percentage based, check if the concentration is provided in a mass per ul basis
               'components[key][k]["Transfer Volume"] = (components[key][k]["Target Concentration"]/components[key][k]["Concentration"])\n                  ' +       # Calculates the volumes of reagent required for transfer based on a mass per ul basis
               'else:\n                     ' + 'components[key][k]["Transfer Volume"] = (components[key][k]["Target Concentration"]*components[key][k]["Target Volume"])/components[key][k]["Concentration"]\n            ' +  # Calculates the volume of the reagent to be transferred based on Mols
               'if k in No_sample.keys():\n                  ' + 'No_sample[k]["Volume"] = No_sample[k]["Volume"] + components[key][k]["Transfer Volume"]\n   \n   ')    # Adds the volume to be transferred to the volume stored in the well_assign dictionary so that the
# Tracking methods are carried out when a transfer takes place during the protocol
                                                                           # Section of the code that governs reagent transfer
    file.write('eval_dict = {}\n   ')                                      # Writes the initial eval_dict declaration to the file. The dictionary starts empty so it can be populated with the labware variables later
    for key in containers:                                                 # Iterates through the containers dictionary key by key
        file.write('eval_dict["{0}"] = {1}\n   '.format(key, key))         # Writes the key from the containers dictionary to the the eval_dict both as the key and the value, this keeps the key as a string, but the value as a variable
# Mixture models output the variable numbers in percentages, this creates an issue where the user needs to use linear constraints to set up the model in the right location
################################################################################ Each code block below is selected based on the roles assigned to the labware the user has included in their protocol
    if role_calc(containers) == "Mixing":         # If there is mixing labware before the final, assemble in mixing, transfer to final, call to the randomiser function randomises the destination wells that the samples have assigned to them.
        file.write('for key in components:\n      ' +                      # Iterates through the dictionaries within the components dictionary and then equips each of the pipettes with the tips
                   'for k in components[key]:\n         ' + 'if components[key][k]["Diluent"].lower() == "y":\n            ' +                # Checks if the current reagent has been identified as a Diluent
                   'pass\n         ' + 'else:\n            ' +                                                                                # If the reagent is a diluent, the iteration of the loop skips
                   'if components[key][k]["Transfer Volume"] == 0:\n               ' + 'pass\n            ' +                                 # If there is a piece of labware designated for mixing
                   'else:\n               ' + 'pip_use(components[key][k]["Transfer Volume"])\n               ' +                             # If the volume to be transferred is not 0ul
                   'if components[key][k]["Transfer Volume"] < (pipette.max_volume/2):\n                  ' +                            # If the volume to be dispensed falls below a certain threshold, the risk of droplet formation needs to be minimised
                   'pipette.flow_rate.aspirate = components[key][k]["Speed"] \n                  ' +  # Sets the aspirate and the dispense rate for the pipette
                   'pipette.flow_rate.dispense = components[key][k]["Speed"] \n                  '
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), mixing_rack.wells(No_sample[k]["Location"]), new_tip="always", blow_out=False)\n               ' +  # Dispenses the reagent being transferred to the bottom of the target location, small volumes are more likely to form droplets, this is avoided dispensing into the solution
                   'else:\n                  ' +
                   'pipette.flow_rate.aspirate = components[key][k]["Speed"] \n                  ' +  # Sets the aspirate and the dispense rate for the pipette
                   'pipette.flow_rate.dispense = components[key][k]["Speed"] \n                  '
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), mixing_rack.wells(No_sample[k]["Location"]), new_tip="always", blow_out=True)\n   ')  #                                                                # Write out a script that also handles the transfer of the mixture to the final destination plate
        file.write('for key in No_sample:\n      ' + 'top_up = {} - No_sample[key]["Volume"]\n      '.format(dictionary[list(dictionary)[0]][list(dictionary[list(dictionary)[0]])[0]]['Target Volume']) +  # Top up logic for adding the diluent to the delute, this final step makes up the solutions to the correct volumes
                   'if top_up < 1:\n         ' + 'pass\n      ' + 'else:\n         ' +                                                           # Adds the calculations to determine how much water is needed to be transferred into the final solution in order to make them up to the correct concentrations
                   'pip_use(top_up)\n         ' +                                                                                          # Selects the most accurate pipette from the two
                   'pipette.transfer(top_up, eval(diluent_find(), eval_dict), {}.wells(No_sample[key]["Location"]))\n   '.format(labware_sort('Mixing')))  # Third and first labware match in this case. Is there a way to simplify this in the code?
        file.write('well_counter = 0\n   ' + 'for key in No_sample:\n      ' +                                      # Calls the randomiser function to create a list of legal wells to transfer assembled samples into
                   'for i in range(replicates):\n         ' +                                               # As the loop for pipetting into a plate, or container that will be the final location
                   'pip_use(containers["{}"]["Working Volume"])\n         '.format(labware_sort('Final')) +                                   # Writes a formatted output line of code that inserts the flagged mixing labware from user specification
                   'pipette.transfer(containers["{1}"]["Working Volume"], {0}.wells(No_sample[key]["Location"]), {1}.wells(well_counter), new_tip="always", mix_before = (5,(pipette.max_volume/2)))\n         '.format(labware_sort('Mixing'), labware_sort('Final')) +  # Sets New_tips to never in the protocol so there is accurate handling of the pipetting process
                   'well_counter = well_counter + 1\n      ')  # Increases the well_counter and drops the tip of the pipette as the new tip in the transfer loop is set to never

################################################################################# Each hash-line separates the potential outcomes from the box ticking excercise
    if role_calc(containers) == "Serial":                                           # Changed the enumerate logic to work with the more awkward instances of serial dilution logic in this framework
        file.write('for key in components:\n      ' + 'well_counter = 0\n      ' +        # Writes a loop for iterating through the reagents in the components dictionary
                   'for i, k in enumerate(components[key]):\n         ' +              # Initiates a nested loop within the main loop to iterate through each sample. For a serial process each sample is considered a step in the serial dilution
                   'if components[key][k]["Diluent"].lower() == "y":\n            ' +  # Checks if the currently iterate component is a diluent for diluting down a specified delute
                   'if well_counter == 0:\n               ' + 'well_counter = well_counter + 1\n               ' +  # If well_counter is zero it is the first well (gives a stock of the delute no dilution)
                   'pass\n            ' + 'else:\n               ' + 'pip_use(components[key][k]["Transfer Volume"])\n               ' +  # If it is not the first well, assess the volume to be transferred and select the most accurate pipette
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), {}.wells(well_counter))\n               '.format(labware_sort("Mixing")) +  # Transfers the specified volume from the reagent store into the mixing plate
                   'well_counter = well_counter + 1\n         ' + 'if components[key][k]["Delute"].lower() == "y":\n            ' +  # Identifies the Delute reagent of the experiment
                   'if well_counter == 0:\n               ' + 'pip_use(components[key][k]["Transfer Volume"])\n               ' +    # If well_counter = 0 it is the first well
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), {}.wells(well_counter))\n               '.format(labware_sort("Mixing")) +  # Transfers the Delute into the first well allocated for the dilution series, giving a stock
                   'well_counter = well_counter + 1\n            ' + 'else:\n               ' + 'pass\n   ' +    # Iterates well_counter to handle the next well
                   'well_counter = 1\n   ' + 'for i in No_sample:\n      ' +                                  # sets well counter back to 1 so that previous wells can be used as a source for subsequent wells which dilute down the sample
                   'pipette.transfer(components[key][k]["Transfer Volume"], {0}.wells(well_counter-1), {0}.wells(well_counter), mix_after=(5,(pipette.max_volume/2)), new_tip="always")\n      '.format(labware_sort("Mixing")) +  # Transfers the delute down the line of diluents created earlier in the protocol
                   'well_counter = well_counter + 1\n   ')  # Mixes the delutes and the diluents together to esure that the dilution is accurate down the line

####################################################################################################################
    if role_calc(containers) == "Serial Plate":  # If source and mixing are checked but final is not, need a serial dilution with a transfer to the final plate, #### FIT THE TIP HANDLING LOGIC INTO THE SERIAL AND PLATE DILUTIONS METHODS
        file.write('for key in components:\n      ' + 'well_counter = 0\n      ' +  # Beings a loop, iterating through the reagents stored in the components dictionary
                   'for i, k in enumerate(components[key]):\n         ' +        # Enumerates through the sub-dictionaries stored within the main components dictionary
                   'if components[key][k]["Diluent"].lower() == "y":\n            ' +  # Checks to see if the currently iterated reagent is the diluent for the serial dilution
                   'if well_counter == 0:\n               ' + 'well_counter = well_counter + 1\n               ' +  # If well_counter is equal to zero, skip the well, the first well should just have Delute in it
                   'pass\n            ' + 'else:\n               ' + 'pip_use(components[key][k]["Transfer Volume"])\n               ' +  # Pip_use assess the volume to be transferred and selects the most accurate pipette for the step
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), {}.wells(well_counter))\n               '.format(labware_sort("Mixing")) +  # Uses the previously selected pipette to transfer the specified volume from the source well to the destination well
                   'well_counter = well_counter + 1\n         ' + 'if components[key][k]["Delute"].lower() == "y":\n            ' +  # Increments well counter so the next well can be accessed and checks if the current reagent is the delute in the serial dilution
                   'if well_counter == 0:\n               ' + 'pip_use(components[key][k]["Transfer Volume"])\n               ' +    # If it is the first well, assess the volume to be transferred and select the more accurate pipette
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), {}.wells(well_counter))\n               '.format(labware_sort("Mixing")) +  # Transfers the reagent marked as a delute into the first well in the dilution series
                   'well_counter = well_counter + 1\n            ' + 'else:\n               ' + 'pass\n   ' +  # Increments well_counter by one so the next well can be accessed
                   'well_counter = 1\n   ' + 'for i in No_sample:\n      ' +                                # Resents well counter back to 1, this is so wells can be iterated through serially and backtrack without creating an impossible number. Also starts a loop iterating through the keys in No_sample dictionary
                   'pipette.transfer(components[key][k]["Transfer Volume"], {0}.wells(well_counter-1), {0}.wells(well_counter), mix_after=(5,(pipette.max_volume/2)), new_tip="always")\n      '.format(labware_sort("Mixing")) +  # Serially transfers reagents down the gradient that has been set up with the previous transfer actions
                   'well_counter = well_counter + 1\n   ' +  # Mixes the samples in the wells between transfer steps to ensure an accurate dilution. Increments the well counter so the next well can be worked on
                   'dilution_source = well_counter\n   ' + 'for i in range(replicates):\n      ' +  # Stores the last well_counter value reached in the loop, into the variable 'dilution_source' the last value for ell_counter is where the reagent is diluted down to the user specified levels
                   'pipette.transfer(containers["{0}"]["Working Volume"], {1}.wells(dilution_source), {0}.wells(well_counter))\n      '.format(labware_sort("Final"),labware_sort("Mixing")) +  # Transfers the now diluted reagent from the mixing labware into the final labware, this is done a number of times equal to the replicates the user specifies
                   'well_counter = well_counter +1\n   ')  # Increments well_counter so that the next well in the series can be iterated through
## TO ADD TO FINAL: TIP TOUCHING METHOD AND THE DIVISION BETWEEN THE TWO DIFFERENT TYPES OF PIPETTE IN ORDER TO AVOID DROPLET FORMATION AT THE BASE OF THE PIPETTE TIP IN ORDER TO FACILITATE ACCURATE TRANSFER BETWEEN THE TWO PIPETTES
############################################################################################################ Final should be replicate compatible now and working in triplicate as well as alongside existing elements of the code structure
    if role_calc(containers) == "Final":                                        # If the reagents are being mixed in the piece of labware that will also serve as the final plate/eppendorfs he samples end up in
        file.write('for key in components:\n      ' +  # Randomises the destination of the samples being assembled before transfer whilst also writing these new destinations to a notepad document
                   'for k in components[key]:\n         ' +              # Enumerates through the keys stored in the in the currently iterated components dictionary
                   'if components[key][k]["Transfer Volume"] == 0:\n            ' + 'pass\n         ' +  # If the volume to be transferred into the solution is 0 then skip the transfer step
                   'else:\n            ' + 'if components[key][k]["Diluent"].lower() == "y":\n               ' +  # If the reagent is marked as a diluent, then the step is skipped because the diluent is used at the end of the protocol to make the solution up to the correct concentration
                   'pass\n            ' + 'else:\n               ' + 'pip_use(components[key][k]["Transfer Volume"])\n               ' +  # Writes application of the pip_use function to the protocol script in order to determine which pipette is the most accurate to  use for a calculated volume
                   'pipette.flow_rate.aspirate = components[key][k]["Speed"] \n               ' +  # Sets the aspirate and the dispense rate for the pipette
                   'pipette.flow_rate.dispense = components[key][k]["Speed"] \n               '
                   'if components[key][k]["Transfer Volume"] <(pipette.max_volume/2):\n                  ' +  # Determines dispensing practice based on the volume being transffered in the pipette. One of the issues is that f you do it as a proportion of the tip
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), {}.wells(No_sample[k]["Location"]), new_tip="always", blow_out=False)\n               '.format(labware_sort("Final")) +
                   'else:\n                  ' + # Equips the pipette with a new tip, this should be covered by the transfer command, but this is a catch case just to be safe
                   'pipette.transfer(components[key][k]["Transfer Volume"], eval(components[key][k]["Well Location"], eval_dict), {}.wells(No_sample[k]["Location"]), new_tip="always", blow_out="True")\n   '.format(labware_sort("Final")) +
                   'for key in No_sample:\n      ' +  # Drops the pipette tips after the loops have completed, this should be covered in the transfer command, this is just to be safe
                   'top_up = {} - No_sample[key]["Volume"]\n      '.format(dictionary[list(dictionary)[0]][list(dictionary[list(dictionary)[0]])[0]]['Target Volume']) +  # Calculates how much of the diluent needs to be transferred into the final sample
                   'if top_up < 1:\n         ' + 'pass\n      ' + 'else:\n         ' + 'pip_use(top_up)\n         ' +  # If the top_up is less than 1, skip the top up step, if greater than 1 select the most accurate pipette for the transfer
                   'pipette.transfer(top_up, eval(diluent_find(), eval_dict), {}.wells(No_sample[key]["Location"]), new_tip = "always", mix_after=[5,(pipette.max_volume/2)])'.format(labware_sort("Final")))  # Transfers the diluent into the samples constructed in the final plate, specified by the user
 ############################################################################################################ Final should be compatible with the new pipette tip handling logic. Check to see if it has been included
