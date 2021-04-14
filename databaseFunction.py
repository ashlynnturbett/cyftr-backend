from __future__ import division
from __future__ import print_function

import csv
import boto3
from boto3.dynamodb.conditions import Key
import argparse
from csv import reader

from cyftr import databaseCall


def updateSingle(room, lname, fname, pname, email, status, location):
    table = databaseCall.getDatabase()

    item = {}
    key = "Room"
    item[key] = room
    key = "Last Name"
    item[key] = lname
    key = "First Name"
    item[key] = fname
    key = "Preferred Name"
    item[key] = pname
    key = "Email"
    item[key] = email
    key = "Entry Status"
    item[key] = status
    key = "Location"
    item[key] = location
    table.put_item(Item=item)
    return ("good")


def updateList(filename):
    with open(filename) as csv_file:
        tokens = reader(csv_file, delimiter=',')
        # read first line in file which contains dynamo db field names
        header = next(tokens)

        room = ""
        lname = ""
        fname = ""
        pname = ""
        email = ""
        status = ""
        location = ""
        # rest of file contain new records
        for token in tokens:
            for i, val in enumerate(token):
                if val:
                    if header[i] == "Room":
                        room = val
                    elif header[i] == "Last Name":
                        lname = val
                    elif header[i] == "First Name":
                        fname = val
                    elif header[i] == "Preferred Name":
                        pname = val
                    elif header[i] == "Email":
                        email = val
                    elif header[i] == "Entry Status":
                        status = val
                    elif header[i] == "Location":
                        location = val
            updateSingle(room, lname, fname, pname, email, status, location)
    csv_file.close()


def verifySingle(room, lname, fname, pname, email, location):
    result = "not accurate"
    analysis = "recipient could not be identified"
    table = databaseCall.getDatabase()
    databaseInfo = databaseCall.getQuery(table, room, lname)
    # print(databaseInfo[0]['Last Name'])
    for item in databaseInfo:
        print(item['Last Name'])
        print(item['First Name'])
        if item['Last Name'].upper() == lname.upper() and item['First Name'].upper() == fname.upper():
            if item['Entry Status'] == 'In Room':
                result = "accurate"
                analysis = 'complete match'
            elif item['Entry Status'] == 'History':
                result = 'not accurate'
                analysis = 'recipient has moved'
        elif item['Last Name'].upper() == lname.upper() and item['First Name'].upper() == pname.upper():
            if item['Entry Status'] == 'In Room':
                result = "accurate"
                analysis = 'complete match'
            elif item['Entry Status'] == 'History':
                result = 'not accurate'
                analysis = 'recipient has moved'
        elif item['Email'].upper() == email.upper():
            if item['Entry Status'] == 'In Room':
                result = "accurate"
                analysis = 'matched by email'
            elif item['Entry Status'] == 'History':
                result = 'not accurate'
                analysis = 'recipient has moved'
                # partials
        elif item['Last Name'].upper() == lname.upper():
            if item['Entry Status'] == 'In Room':
                result = "partially accurate"
                analysis = 'incorrect first name'

    # print looks like this [{'Entry Status': 'History', 'Last Name': 'TURBETT', 'Preferred Name': 'Ashlynn', 'Location': 'Jester Center-West', 'Room': 'JSW W0428B', 'First Name': 'ASHLYNN', 'Email': 'ashlynn.turbett@austin.utexas.edu'}]
    #verify function
    return result, analysis


def verifyList(filename):
    with open(r'C:\Users\suzie\Documents\cyftr2\ResidentData_Results.csv', 'w', newline='') as write_file:
        writer = csv.writer(write_file)
        with open(filename) as csv_file:
            tokens = reader(csv_file, delimiter=',')
            # read first line in file which contains dynamo db field names
            header = next(tokens)
            room = ""
            lname = ""
            fname = ""
            pname = ""
            email = ""
            location = ""
            field = ['Room', 'LastName', 'FirstName', 'PreferredName', 'Email', 'Location', 'Result', 'Analysis']
            writer.writerow(field)
            # rest of file contain new records
            for token in tokens:
                for i, val in enumerate(token):
                    if val:
                        if header[i] == "Room":
                            room = val
                        elif header[i] == "Last Name":
                            lname = val
                        elif header[i] == "First Name":
                            fname = val
                        elif header[i] == "Preferred Name":
                            pname = val
                        elif header[i] == "Email":
                            email = val
                        elif header[i] == "Location":
                            location = val
                result, analysis = verifySingle(room, lname, fname, pname, email, location)
                row = [room, lname, fname, pname, email, location, result, analysis]
                writer.writerow(row)
                room = ""
                lname = ""
                fname = ""
                pname = ""
                email = ""
                location = ""
        csv_file.close()
