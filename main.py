
import os

import os

# Define a list
my_list = ["value1", "value2", "value3"]

# Convert the list into a string with a delimiter (comma in this case)
list_as_string = ",".join(my_list)

# Set the environment variable with the string representation of the list
os.environ["MY_LIST"] = list_as_string



import os

# Get the environment variable
list_as_string = os.getenv("MY_LIST")

# Convert the string back to a list using the delimiter
retrieved_list = list_as_string.split(",") if list_as_string else []

# Print the retrieved list
print(retrieved_list)
