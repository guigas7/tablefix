# tableFix

rows_to_cols.py -> From a base table in the same directory, called 'input.csv', for all questionaries in quests, finds 
the columns for the labels of each questionaries and repeats their columns for every new line of repeated column 0 entry,
acording to the 'days' list. For every repeated entry, while passing their data from questionaries in quest to the newly
created columns, in the line of the original entry (second line to first new column range, third line to second new column
range, and so on, taking from the repeated lines, to the first of that entry). The columns from post list will be copied
from the last repeated line of each entry (checking by col 0) to the same columns in the line of the original entry. After
the data is all copied to the first line of each unique entry in col 0, all repeated lines will be removed.

replicate.py -> From a base table in the same directory, called 'input.csv', for all questionaries in admiss and for all
questionaries in post, copies admiss values to all the subsequent rows from the same patient and all the post values to
all the previous rows from the same patient.

Transfer Handler

---- patient.py -> Defines Patient class

---- helpers.py -> Helpers to clean lookups in the dataframe

---- sofa.py -> Keeps Sofa data structure and helpers to append, check and increase it

---- clean_transf.py -> From a base table in the same directory, called 'input.csv', process all lines to remove trailing
                        and leading spaces on patient names and makes it all uppercas. For all transfers pass all
                        sofa + discharge data from the transfer lines to the parent line.
