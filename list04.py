#!/usr/bin/env python3

'''Alta3 Research | RZFeeser
   Reading data out of a file and into a list format.'''   
   
def main():
    '''reading data out of a file'''
    
    # create an empty list we can write our data into
    network = []
    
    # open data in "read" mode
    with open('ipdata.txt', 'r') as ipdata:
        for line in ipdata: # single line from our file is line
            # rstrip removes and special characters on the right of the str
            #line = line.rstrip("\n")
            
            # append adds to the end of the list
            network.append(line)   # append a line to our list
            
            # display the line read from the file to the screen
            print(line)
    
    # the loop is now finished
    print(network)  # display the finished list, "network"

# best practice technique to call our python script
if __name__ == "__main__":
    main()     # calls the "main" function to run

