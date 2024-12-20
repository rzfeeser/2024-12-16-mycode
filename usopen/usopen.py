#!/usr/bin/env python3
## USOpen Tournament Switch Checker -- 2024.12.17
## Written by RZFesser | Alta3 Research

''' usopen.py
This script is being designed to provide the following automated tasks:
- ping check the switch (import os)
- login check the switch (import netmiko)
- determine if interfaces in use are up (import netmiko)
- Apply new configuration (import netmiko) # not yet built

The IPs and device type should be made available via an Excel spreadsheet
'''

# standard library
import os
import csv
import socket

# python3 -m pip install netmiko
from netmiko import ConnectHandler


## resolve hostname to ip
def resolve_ip(entry):
    """uses socket library to resolve a hostname to an IP address"""
    for switch_info in entry:
        switch_info['ip'] =  socket.getaddrinfo(switch_info['hostname'], 22)[-1][-1][0]  # this will resolve hostname to IP
    return entry # return the updated "entry" list

## retrieve data set from excel
def get_csv(fileloc):
    """get info out of the CSV file and turn into python dict"""
    d = []  # start with an empty list we will fill up with dictionaries

    with open(fileloc, "r") as open_csv_file:
        for row in csv.DictReader(open_csv_file):
            # first value of row == {'hostname': 'sw-1', 'driver': 'arista_eos'}
            keypair = {'hostname': row['hostname'], 'driver': row['driver'], 'username': row['username'], 'password': row['pass']}
            # first value of keypair == {'sw-1': 'arista_eos'}
            d.append(keypair)

    return d  # return the completed list --> [{'hostname': 'sw-1', 'driver': 'arista_eos', 'username': 'student', 'password': 'alta3}, ...]


## Ping switch - returns True or False
def ping_switch(dev_ip):
    """test if device responds to ping"""
    response = os.system("ping -c 1 " + dev_ip)

    # if there were no errors with ping command, response = 0
    # if there WERE errors, response > 0
    if response == 0:
        return True

    else:
        return False


## Check interfaces - Issue "show ip int brief"
def interface_check(dev_ip, dev_type, dev_un, dev_pw):
    """check health of interfaces using SSH"""
    try:
        # attempt to open a connection to this switch
        open_connection = ConnectHandler(device_type=dev_type, ip=dev_ip, username=dev_un, password=dev_pw)

        # send a command to the switch; record the ouput in "my_command" var
        my_command = open_connection.send_command("show ip int brief")

    except:
        # if an error occurs, the value of "my_command" will say it failed
        my_command = "** ISSUING COMMAND FAILED **"

    finally:
        # no matter what, this function will return "my_command"
        return my_command


## Login to switch - SSH Check with Netmiko class ConnectHandler
def login_switch(dev_ip, dev_type, dev_un, dev_pw):
    """test logging into switch with SSH"""
    try:
        # attempt to make a connection to the switch
        open_connection = ConnectHandler(device_type=dev_type, ip=dev_ip, username=dev_un, password=dev_pw)

        # if connection was made with no errors, function returns TRUE
        return True

    except:
        # if error occurred while making connection, function returns FALSE
        return False


def main():
    """runtime code"""
    # Determine where *.xls input is;
    # note that pressing 'enter' without typing anything has a default value
    file_location = input("Host file location [Press ENTER for default: 'host_list.csv']\n>") or "host_list.csv"

    # get the info from the csv file
    entry = get_csv(file_location)
    
    # at this point
    # entry = [{'hostname': 'sw-1', 'driver': 'arista_eos', 'username': 'student', 'password': 'alta3}, ...]

    # the DNS is not setup to cache, and sometimes DNS fails if we try to resolve 'sw-1' or 'sw-2' too rapidly
    # we we will add the resolved IP address for the host names to our list of switch dictonaries "entry"
    entry = resolve_ip(entry)   # this adds a new key to each dictonary "ip"

    # use a loop to check each device for ICMP responses
    print("\n***** BEGIN ICMP CHECKING *****")
    for switch_info in entry:
        if ping_switch(switch_info['ip']):  # check if function returns TRUE or FALSE
            # if func returned TRUE:
            print(f"\n\t**HOST: - {switch_info['hostname']} - responding to ICMP\n")
        else:
            # if func returned FALSE:
            print(f"\n\t**HOST: - {switch_info['hostname']} - NOT responding to ICMP\n")


    # Use a loop to check each device for SSH accessability
    print("\n***** BEGIN SSH CHECKING *****")
    for switch_info in entry:
        if login_switch(switch_info['ip'], switch_info['driver'], switch_info['username'], switch_info['password']):  # returns TRUE and FALSE
            # if function returned true, print connectivity is UP
            print(f"\n\t**HOST: - {switch_info['hostname']} - SSH connectivity UP\n")
        else:
            # if function returned false, print connectivity is DOWN
            print(f"\n\t**HOST: - {switch_info['hostname']} - SSH connectivity DOWN\n")


    # Use a loop to check each device for ICMP responses
    print("\n***** BEGIN SHOW IP INT BRIEF *****")
    for switch_info in entry:
        # pass values needed to make connection into interface_check() function
        # function will save its output to the "result" var
        result = interface_check(switch_info['ip'], switch_info['driver'], switch_info['username'], switch_info['password'])
        print("\n" + result)


if __name__ == "__main__":
    main()