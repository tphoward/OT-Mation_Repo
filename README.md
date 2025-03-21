# Howard-Group-Newcastle
Howard Group at Newcastle University

# OT-Mation
OT-Mation is a Python script that reads through a series of csv files, filled out by the user, to generate Python scripts that can be uploaded into the OT-2 liquid handling robot companion application to automate laboratory experiments. We aim to make the OT-2 liquid handling robot more accessible by removing the pre-requisite of Python programming skills from OT-2 operation.

Our preprint describing OT-Mation can be found on bioRxiv: https://doi.org/10.1101/2025.01.20.633898

## Getting Set Up
Because `OT-Mation` is a Python script it is easy to install and automates a majority of the OT-2 setup for the user. There are a couple of dependencies for `OT-Mation`, these are freely available and listed under **Prerequisites**.

### Prerequisites
There are two packages, as well as Python itself, that `OT-Mation` relies on in order to operate correctly:
- Python (Tested on versions: 3.7, 3.9 and 3.12)
  - Tested with Opentrons 3.1
  - Tested with Pandas 0.25.0

OT-Mation has been tested and successfully used on both Windows and MacOS machines.

Python 3.7, and more up to date versions can be dowloaded and installed from the [Python](https://www.python.org/) website. 
Navigate to the downloads section, selecting your version, and operating system. The wizard will guide you the rest of the way.

Both the [Opentrons](https://pypi.org/project/opentrons/) and [Pandas](https://pypi.org/project/pandas/) packages can be installed by using Pip. Python versions 3 and later come with Pip installed. The following code can be used to install the packages:

```python3 
pip install opentrons
```

and 

```python3 
pip install pandas
``` 

both packages will be installed ready for use. If you encounter issues installing either package Pandas and Opentrons are available on [Pypi](https://pypi.org/), which also has short descriptions and install instructions for the packages.

As a script `OT-Mation` does not require installation. Simply download `OT-Mation` from this GtHub and save `OT-Mation` to a memorable location.

## Using OT-Mation
`OT-Mation` uses csv input in order to generate the python scripts for use with the OT-2 liquid handling robot. Effectively removing the need for a user to code in Python in order to operate the robot. `OT-Mation` produces a script after reading the required csv files. It is the output script that enables operation of the robot **not the** `OT-Mation` **script.** Uploading the output script into the OT-2 companion application will program the experiment.

It is strongly recommended that the user reads through the [Opentrons API](https://docs.opentrons.com/index.html) or at least has the API open before/whilst using `OT-Mation` and reading through `OT-Mation` documentation. This will help users identify causes of errors should any occur.

### CSV. Input
`OT-Mation` uses csv file input in order to generate the python scripts for operating the OT-2 liquid handling robot. Enabling users to effctively program the OT-2 using their spreadsheet program of choice (such as Microsoft Excel) rather than Python.

Four csv files are used in order to generate the Python scripts to operate the OT-2. Templates of these csv files, what they should contain and how they should look, can be found on this GitHub. The four csv files contain: 
- Inventory of stocks and where they are in the OT-2 workspace: `Stock Inventory.csv`
- Experimental Parameters: `Experimental Parameters.csv`
- Pipette settings of the OT-2: `Pippette Settings.csv`
- What labware is being used in the experiment and how it is identified: `Labware.csv`

These four csv files can be renamed from within the `OT-Mation` script to fit user preference. In the OT-Mation script are four variables which hold the names of the csv files: `Exp_parameters`, `Stock_inventory`, `Pipette_settings` and `Labware_definitions`. The string saved to each variable is the name of the csv file that `OT-Mation` will look for when run:
```Python3
Exp_parameters = "Experimental Parameters.csv"  # Change the strings to match desired file names i.e. "Statistical experiment.py"
Stock_inventory = "Stock Inventory.csv"
Pipette_settings = "Pipette Settings.csv"
Labware_definitions = "Labware.csv"
```
Each string must match the name of the csv file exactly in order for `OT-Mation` to find the file. Additionally, the file needs to be within the same working directory as the `OT-Mation` script. Users familiar with Python can code in a file pathway so files do not need to be in the same working directory.

By combining the input from these four csv files a Python script can be written for programming the OT-2. These csv files can be shared with other researchers, as can the output python script from `OT-Mation`, to facilitate replication of experiments. Output and csv files can also be archived in order to maintain a trackable paper trail.

Blank templates as well as filled in examples of how the csv files should be completed are also posted on this GitHub. `OT-Mation` is written to read the data from each csv in a file specific manner i.e. `Experimental Parameters.csv` will not be read in the same way as `Labware.csv` if the user does change the names for the files to be read, ensure the correct file is saved to the right variable. Please note that the `Experimental Parameters.csv` file is blank, this is because the column headers must match the reagent names in `Stock Inventory.csv` **(need a better blank template for experimental parameters)**.


### Stock Inventory
Stock Inventory is arranged so that each row represents a reagent and the samples said reagent is present in, whilst the columns are reagent details i.e. name, volume, location. 
- **Component** This is the name of the reagent. What is entered in each row of this column will be how the reagent is referred to in the output script. If there are multiple samples with the reagent in, you do not need to put the reagent name on every single row. It is imortant to note that if the reagent name contains a space **use an underscore instead** if a reagent is named `Q5 Buffer` instead write `Q5_Buffer` spaces in variable names will create an error. 

- **Sample** Refers to each sample being assembled by the OT-2. The naming convention is simply `Sample #` where the # represents a numerical number such as 1. **Python lists start at 0 not 1 so the first sample should be named** `Sample 0`.
- **Well Location** Where the reagent stock is stored in the OT-2 work surface and what piece of labware it is stored in. The names used in the Well Location cells must match the names used in the Labware csv file. 
- **Volume** The volume of the stock, this is recorded in microlitres as that is the scale the OT-2 operates on.
- **Concentration** Concentration of the stock solution. Depending on how other cells are filled out in the csv the concentration can be recorded as percentage, mass per microlitre and mols.
- **Target Volume** Recorded in microlitres, the target volume is the final volume of the sample being assembled by the OT-2.
- **Speed** This sets a default value for both aspirating and dispensing in microlitres per second. This is further customised in the pipette settings csv file.
- **Transfer Volume** `OT-Mation` will calculate what transfers need to occur in order to create a sample containing the correct concentrations of reagents. If the user already knows a volume or wants to use a custom volume, enter in the Transfer Volume cells in microlitres. Leave Transfer Volume blank if you want `OT-Mation` to calculate instead.
- **Percent** Enter `Y` or `N` in the cell (for yes or no) if the concentration entered is a percentage. This is not case sensitive. The entry must be `Y` or `N`.
- **Mass per ul** Enter `Y` or `N` in the cell (for yes or no) if the concentration entered is in mas per ul. This is not case sensitive. The entry must by `Y` or `N`.
- **Diluent** Enter `Y` or `N` in the cell (for yes or no) if the reagent is for diluting down a sample or other reagent. This is not case sensitive. Entry must be `Y` or `N`. 
- **Delute** Enter `Y` or `N` in the cell (for yes or no) if the reagent is to be diluted down by a Diluent before it is used in sample assembly. This is not case sensitive. entry must be `Y` or `N`.

A row for every single sample being assembled is not needed. `OT-Mation` will calculate how many Samples should be assembled in total by combining the information from `Stock Inventory` and `Experimental Parameters` csv. files.

### Experimental Parameters
The layout for the experimental parameters csv. is such that each row represents a Sample being assembled by the OT-2 and each column is one of the reagents previously specified in the `Stock Inventory` csv. **The reagent names acting as column headers must match what is in the** `Stock Inventory` **csv.** In addition, there is no need for a column which just acts as Sample names, this is automatically deduced by `OT-Mation` with the system: First row is headers, second row is `Sample 0` third row is `Samples 1` etc. In each cell enter the deseried final concentration of the reagent in the sample, matching the concentration measure in the `Stock inventory` csv. For example, if `Glucose` was given as a percentage in `Stock Inventory` then `OT-Mation` will assume `Glucose` concentrations given in `Experimental Parameters.csv` will be a percentage as well.

### Pipette Settings
Pipette settings contains the settings the user wishes to establish for the pipettes to be used through the assembly of the samples. Two pipettes can be mounted simaltaneously in the OT-2 and `OT-Mation` takes advantage of this. `OT-Mation` enables full control over pipette settings that would be available to the user if they were assembling a protocol with Python, the columns represent the two pipettes as well as a title column for the various settings:

**Columns**
- **Elements** Each setting available for the pippettes that `OT-Mation` can handle. The `Elements` column does not need to be adjusted by the user.
- **Pipette 1** The first pipette in the OT-2.
- **Pipette 2** The second pipette in the OT-2.

**Rows**
- **Pipette** Specifies which model of pipette ( P10, P50 etc) to be used. This needs to be entered as it appears in the [Opentrons API](https://docs.opentrons.com/v1/pipettes.html). Specifying whether the pipette is single or multichannel as well. The entry should be written as `P50_Single()` for a P50 single channel pipette or `P10_Multi()` for a P10 multi channel, as examples.
- **Mount** Which mount the pipette is afixed to within the OT-2. Mounts are identified as either `left` or `right` with no capitalisation. 
- **Aspirate Rate** Sets the aspiration rate of the pippete. The value given is in microlitres per second (default value 150).
- **Dispense Rate** Sets the dispense rate of the pipette. The value is given in microlitres per second (default value 150).
- **Tip Rack** Allocates a tip rack with a name that matches the entry to the corresponding pipette. The names entered in these cells must match names given to tip racks in `Labware.csv`, for example: `tiprack50ul`. Multiple tip racks can be assigned to the same pipette by writing all the names of the desired tip racks as they appear in `Labware.csv` placing a comma between each rack : `tiprack50ul, tiprack50ul2`.
- **Trash Container** Assigns a trash box to the corresponding pipette. If a custom trash container is assigned to the pipette the name entered must match a labware name specified within the `Labware` csv.

Whilst some settings have default values for the pipettes, it is recommended to fill out each field for the two pipettes. If an experiments only needs a single pipette the unused pipette column can be filled with `NULL` values.

### Labware
All labware to be used in the OT-2 (tip racks, tube racks, trash containers etc.) is named and specified in the `Labware` csv. Whilst it is possible to use Python to make your own custom labware for use within the OT-2, `OT-Mation` can use any custom labware you have already written. **However, `OT-Mation` cannot be used to write custom labware.** Currently support pre installed labware is available on the [Opentrons API](https://docs.opentrons.com/v1/labware.html) as well as the [Opentrons Labware Library](https://labware.opentrons.com/)

**Columns**
- **Name** The name that will be used to identify the labware within the script. If the name you wish to use has a space, use under scores. For example the name `Reagent Rack` should be written as `Reagent_Rack`.
- **Labware** Which pieces of labware are being used in the protocol. The names entered in these cells must match as written in the [Opentrons API](https://docs.opentrons.com/v1/labware.html) or [Opentrons Labware Library](https://labware.opentrons.com/). The names of the labware are case sensitive.
- **Slot** Refers to which working slot the labware will be in. The OT-2 work surface as 11 fixed labware slots (and a twelth permanent trash) essentially informing the `OT-Mation` where the labware will be in the OT-2. 
- **Working Volume** Assigns the working volume to the labware, given in microlitres, this value can be 0 and is used to make sure that the labware isn't overfilled.
- **Source** Identifies if the labware is a 'Source' such as where the reagents are stored. Enter `Y` or `N` (for yes or no) entry is not case sensitive. Entry must be `Y` or `N`.
- **Mixing** Identifies if the labware is acting as an intermediary mixing platform, reagents are combined in this labware before being moved into a final rack/eppendorf in a different slot. Enter `Y` or `N` (for yes or no) entry is not case sensitive. Entry must be `Y` or `N`.
- **Final** Identifies if the labware is the final destination for samples being assembled by the OT-2. Enter `Y` or `N` (for yes or no) entry is not case sensitive.

The combination of `Y` and `N` enables `OT-Mation` to calculate what needs to be done and where with regards to the protcol. The information of `Source`, `Mixing` and `Final` can be combined with data from the `Experimental Parameters` csv. to write the protocol and how reagents are handled. This enables `OT-Mation` to program complex liquid handling procedures as well as simpler ones such as serial dilutions.

After completing each of the csv files, `OT-Mation` is ready to run and produce protocol scripts for use with the OT-2. Any errors that occur from running `OT-Mation` will be produced in standard Python error message format. If errors do occur, they are like to stem from simple mistakes. Such errors could be due to file names not matching what is written in `OT-Mation` exactly.

## Using `OT-Mation`
`OT-Mation` is easy to use and aims to be accessible to users regardless of whether they have Python programming skills. It is strongly recommend that the user gets comfortable with a Python environment, whilst it is possible to use `OT-Mation` with no coding skills at all, quality of experiments and the protocols produce by `OT-Mation` can be dramatically improved with application of basic Python skills.

### Running `OT-Mation`
`OT-Mation` runs in the same way as a standard Python script through the user's preferred IDE or text editor. Files to be read by `OT-Mation` need to be within the same working directory as the `OT-Mation` script (folder space) in order to read the csv. files. `OT-Mation` can be edited to contain file roots to the csv files of interest if the user has the Python knowledge to do so. After running `OT-Mation` a Python script will be generated in the same working directory as the `OT-Mation`. The name of the newly generated Python script will match whatever string (or integer) has been saved into the `Output_file` within the `OT-Mation` script. This name may include spaces.

**Finding the csv files**

The `OT-Mation` script needs to be in the same working directory as the csv files in order to find and read them. Experienced Python user can put file pathways into the `OT-Mation` script to remove the need for same working directory to find the csv files and increase convenience. `OT-Mation` needs to know what the names of the csv files in order to find them. By default `OT-Mation` will be looking for csv files with the standard names mentioned in here `Experimental Parameters.csv` `Labware.csv` `Stock Inventory.csv` and `Pipette Settings.csv`. These names are case sensitive. If the user requires alternative names to be given to the files for use with `OT-Mation` required names can be adjusted from within the `OT-Mation` script.

**Generating Protocols**

Protocols are automatically generated by `OT-Mation` depending on how the user fills out their csv files. Information from the `Stock Inventory.csv` and `Labware.csv` dictate what protocol is generated and how the different reagents are handled. 
Initial calculations of the protocol are determined by how the fields in `Labware.csv` have been completed. `Source`, `Mixing` and `Final` are responsible for the generation of the protocol.
- **Source:** When a piece of labware is identified as a source this cause `OT-Mation` to view the labware as a place to aspirate reagents from but not dispense them to. This does not mean that reagents and components cannot be aspirated from plates that are **not** marked as source, but reagents and components cannot be dispensed to the labware marked as `Source` in an aim to reduce contamination risks.
- **Mixing:** Labware marked as `Mixing` Is labware identified for the mixing of reagents, where if the user wanted to mix `Reagent A` and `Reagent B` together, this would be done on `Mixing` labware. `OT-Mation` Will aspirate and dispense from `Mixing` labware, treating the designated labware as an intermediate location between `Source` and `Final` labware. If labware is identified as `Mixing`, `OT-Mation` will look for labware identified as `Final`, by default, `OT-Mation` will look to mix reagents together and then move the resultant solution to a `Final` labware.
- **Final:** If a piece of labware is marked as `Final`, `OT-Mation` will treat the labware as a final destination for reagents and solutions. Reagents and solutions can be dispensed to but **not** aspirated from a `Final` plate. `OT-Mation` will not seek to move solutions and reagents out of the `Final` labware. A piece of Labware can be the final destination of solution and reagents, whilst also being the labware the user would like to mix reagents in i.e. mix the reagents in an eppendorf. In this instance, by marking a piece of labware as `Final` and then not identifying a `Mixing` labware `OT-Mation` will generate a protocol where reagents are mixed and kept in the `Final` labware.

Within the `Experimental Parameters.csv` there are two fields that contribute to the protocol generation:
- **Diluent:** When a reagent is marked as a `Diluent`, for the purposes of protocol calculation it is considered a diluting agent for the purpose of diluting down other reagents that have been marked as a `Delute`. `Diluent` is also used to identify which reagent in the stock inventory will be used to 'top up' samples to the target volume/concentration. By having a selectable `Diluent` instead of assuming water, users can incorporate buffers and other reagents into their protocols. Diluents do not need concentration values etc. just well locations. Reagents marked as `Diluents` will not be considered as reagents for sample assembly.
- **Delute:** Marking a reagent as a `Delute` identifies that it needs to be diluted down during the protocol, similarly to a serial dilution. This enables the user to set up serial dilutions with `OT-Mation` as part of reagent preparation for a larger protocol.

**Calculating Reagent Concentrations and Transfers**

Based on the `Concentrations` and `Target Volumes` within `Stock Inventory.csv` and the concentrations specified in `Experimental Parameters.csv`, `OT-Mation` is able to calculate what transfers/dilutions need to be made from a stock solution to the final location in order to produce solutions of the correct concentration. This is why it is possible for the `Transfer Volume` field to be left blank in `Stock Inventory.csv` as `OT-Mation` will calculate the volume to transfer if the field is left blank. If the user enters a value in the `Transfer Volume` field, it will overwrite whatever `OT-Mation` would have calculated. This is only the case for the `Sample` row that the volume is entered into, so the user can set a unique `Transfer Volume` on a per sample basis. Because the volumes are set on a per sample basis, the user can enter a volume for some samples whilst also allowing `OT-Mation` to calculate the volumes required for other samples. When entering custom `Transfer Volume` the volume being transferred will still be tracked by `OT-Mation` prevent the final volume from being higher or lower than expected, as a means to prevent concentration errors. `OT-Mation` Will automatically create the correct number of rows in `Stock Inventory.csv` to make up with the number of rows in `Experimental Parameters.csv`

`OT-Mation` will calculate reagent concentrations based either on mols or via the field that was checked with `Y` in `Stock Inventory.csv`. Users can change this by making edits to the `OT-Mation` script.

## Protocol Output

Rather than being the protocol itself, `OT-Mation` produces an output script that is used to program the OT-2 liquid handling robot. Nothing needs to be done to the script by the user in order to generate an output, `OT-Mation` produces a ready to use script from the default settings. It is strongly recommended, although not needed, for the user to open the output script and write the following code block:
```Python3
for c in robot.commands():
  print(c)
```

Once run, this will print all the actions the protocol is programming for, allowing the user to read and double check what the robot will actually do with the passed protocol script, allowing for the identification of any potential errors in the protocol. As the output script is isolated from `OT-Mation` the user can freely adjust the output script if they have the Python skills. As the output script operates independently of `OT-Mation` it can be passed to other users who wish to replicate or adjust the protocol. 

By default, Python scripts produced by `OT-Mation` will have the name `Output Experiment.py` names can be changed by the user opening `OT-Mation` and navigating to the `Output_file` variable and changing the string to the users preferred name: 
```Python 3
Output_file = "Output Experiment.py"  # Change "Output Experiment.py" to desired name i.e. "Best Experiment.py"
```
a file extension of .py must be included in the name in order to generate a Python script. 

To generate a protocol `OT-Mation` needs to find all four of the user generated csv files. When run, if a file is not present an error message will inform the user which of the files is missing. Importantly, the names of the csv files are case sensitive if the name of the file and the string in the script do not match exactly, as well as having the correct file extension, `OT-Mation` will fail to generate a protocol.

## Examples of OT-Mation in Operation

Two regularly utilised experimental procedures were automated using `OT-Mation` to validate the generation of protocols from user written csv files. These procedures were: Serial dilution and master mix preparation. Each procedure was chosen due to how frequently it is used in research and the differing levels of complexity between the procedures. It is important to note that `OT-Mation` is **not** limited to just these procedures, these are simply examples of what `OT-Mation` can be used to generate and automate.
