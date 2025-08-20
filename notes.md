## Notes


Registry.save() will:

1. Load the current data from the passed in registry file to a dictionary
2. Modify the loaded dictionary by replacing the updated set data
3. Write the updated registry data back to registry file line by line:
    1. Write each meta data line
    2. Write the node list, iteratively writing individual node objects to registry file nested inside a nodes list: nodes = [ <In Here> ] 



