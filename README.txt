This zip contains 5 elements:
    - This README
    - The report (Report.pdf)
    - A folder named "queries"
    - A folder named "data"
    - A folder named "programs"

The folder named "data" contains the scripts used to manipulate and analyze the original data, and a folder (csvs)
containing such data.

The folder named "queries" contains 6 cypher files containing the different queries used in the lab.

The folder named "programs" contains three subdirectories:
    - "programs" contains the different python files for the loading and evolving programs
    - "program_queries" contains cypher files with the queries used in the programs
    - "program_csvs" contains the data files that should be used to load the graph

Steps to run the programs:
    1. Install dependencies if necessary (the only required package is "neo4j")
        - If using pipenv, in the top "programs" folder there is a Pipfile so you can use "pipenv install"
    2. Copy the folder "program_csvs" in the Neo4j import file directory
    3. Run the programs from the top "programs" folder:
        - A2 -> python ./programs/partA2_ZafalonDivi.py
        - A3 -> python ./programs/partA3_ZafalonDivi.py
        The programs accept several parameters that can be checked with the -h flag, but the defaults should work normally
