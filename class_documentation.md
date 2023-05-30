# ProcessGameState Python Class

## File Ingestion and ETL

- Methods:
  - \_\_ingest_data()
  - Private method: takes in a file path and returns a Pandas DataFrame of the data in the file.
- With regards to data cleaning and ETL, the 'clock_time' values were converted to Pandas datetime objects for efficient time calculations for questions later on in the assessment.
- No other transformations or explorations were deemed necessary for the scope of this assessment, as there were no questions that dealt with requiring the data to be in a different format or meet a certain criteria.

## Boundary Checks for Each Row

For this section, two methods were tested for efficiency and accuracy: a naive approach that simply calculates a box based on minimum and maximum x and y values, and a more complex approach that utilizes Matplotlib's Path class to create a polygon and check if the x and y values of each row are within the polygon. More on the analysis of each method's performance can be found in the 'analysis_and_interpretation.md' markdown file.

- Methods:
  - \_\_calculate_boundary()
    - Private method: takes in a list of xy coordinates and z values, and returns a dictionary with the minimum and maximum x, y, and z values.
  - \_\_in_bounds()
    - Private method: takes in a coordinate point (x, y, z) and the bounds dictionary returned from \_\_calculate_boundary().
    - Checks if the x, y, and z values are within the bounds, and returns a boolean value.
  - check_boundaries() - Naive approach
    - Public method: takes in xy coordinates, z values, team name, and team side
    - Creates a dictionary of the minimum and maximum x, y, and z values for each team and team side
    - Loops through subset of data based on team name and team side to check if each row is within the boundary
    - Returns a list of integers, each index representing a round and the value representing the number of times the team was within the boundary for that round
  - check_boundaries_with_matplotlib() - Matplotlib Path approach
    - Public method: takes in xy coordinates, z values, team name, and team side
    - Creates a polygon using Matplotlib's Path class
    - Loops through subset of data based on team name and team side to check if each row is within the boundary
    - Returns a list of integers, each index representing a round and the value representing the number of times the team was within the boundary for that round

## Weapon Classes Extraction

It was determined that the most efficient way to store the weapon classes for each row was to create a new column in the DataFrame that contained a list of the weapon classes used for each row. This was done by looping through the 'inventory' json for each row and extracting the weapon class for each weapon. This allowed for a more efficient way to answer the questions in the assessment, as the timer for each round was needed to determine the number of times a team was within the boundary for each round.

- Methods:
  - extract_weapon_classes()
    - Public method: loops through the 'inventory' json for each row and extracts the weapon class for each weapon
    - Adds a new column to the DataFrame with the weapon classes used for each row
