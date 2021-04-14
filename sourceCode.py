from __future__ import division
from __future__ import print_function

import csv
import boto3
from boto3.dynamodb.conditions import Key
import argparse
from csv import reader

from cyftr import databaseCall

residenceData = "ExampleDataForResidences.csv"
senderData = "ExampleDataForSenders.csv"

# doing the initialization for the titles and rows list
fieldsResi = []
rowsResi = []

fieldsSenders = []
rowsSenders = []

# command line arguments
parser = argparse.ArgumentParser(
    description='Write CSV records to dynamo db table. CSV Header must map to dynamo table field names.')
parser.add_argument('csvFile', help='Example Data for Residences')
parser.add_argument('table', help='Dynamo db table name')
parser.add_argument('results')
parser.add_argument('check')
parser.add_argument('writeRate', default=5, type=int, nargs='?',
                    help='Number of records to write in table per second (default:5)')
parser.add_argument('delimiter', default=',', nargs='?', help='Delimiter for csv records (default=,)')
parser.add_argument('region', default='us-east-1', nargs='?', help='Dynamo db region name (default=us-east-1)')
args = parser.parse_args()
print(args)

# dynamodb and table initialization
endpointUrl = "https://dynamodb.us-east-1.amazonaws.com"
dynamodb = boto3.resource('dynamodb', region_name=args.region, endpoint_url=endpointUrl)
table = dynamodb.Table(args.table)

with open(args.csvFile) as csv_file:
    tokens = reader(csv_file, delimiter=args.delimiter)
    # read first line in file which contains dynamo db field names
    header = next(tokens)
    # rest of file contain new records
    for token in tokens:
        print(token)
        item = {}
        for i, val in enumerate(token):
            print(val)
            if val:
                key = header[i]
                print(val)
                if key == "Last Name":
                    hold = val
                elif key == "First Name":
                    hold += val
                item[key] = val
        key = "Last Name+First Name"
        item[key] = hold
        print(item)
        table.put_item(Item=item)

outF = open(args.results, 'w')
with open(args.check) as csv_file:
    tokens = reader(csv_file, delimiter=args.delimiter)
    header = next(tokens)
    for token in tokens:
        for i, val in enumerate(token):
            if val:
                if header[i] == "Last Name":
                    information = val
                elif header[i] == "Address":
                    address = val
        table = databaseCall.getDatabase()
        databaseInfo = databaseCall.getQuery(table, address, information)

        if len(databaseInfo) == 1:
            outF.write("Accurate\n")
            # return ("Accurate")
        elif len(databaseInfo) > 1:
            outF.write("Partially Accurate\n")
            # return ("Partially Accurate")
        else:
            outF.write("Not Accurate\n")
            # return ("Not Accurate")

#Address,Last Name,First Name
# # try a query
# def checkDB():
#     response = table.query(
#             KeyConditionExpression=(Key('Last Name').eq('Waller'))
#         )
#
#     print("RESPONSE   ", response['Items'])
#     return response['Items']
#
# # reading csv file
# with open(senderData, 'r') as csvfile:
#     # creating a csv reader object
#     csvreader = csv.reader(csvfile)
#
#     # extracting field names through first row
#     fieldsSenders = next(csvreader)
#
#     # extracting each data row one by one
#     for row in csvreader:
#         rowsSenders.append(row)
#
#         # get total number of rows
#     print("Total no. of rows: %d" % (csvreader.line_num))
#
# # printing the field names
# print('Field names are: ' + ', '.join(field for field in fieldsSenders))
#
# #  printing first 5 rows
# print('\nFirst 5 rows are:\n')
# for row in rowsSenders[:5]:
#     # parsing each column of a row
#     for col in row:
#         # print out an item and doesn't new line, just adds a space
#         print(col, end=' ')
#     print('')  # gets it on a new line
#
# print("testing indexing: ", rowsSenders[1][1])
# print("testing indexing: ", rowsSenders[1][2])
# print("testing indexing: ", rowsSenders[1][3])
# print("testing indexing: ", rowsSenders[1][4])
#
# ###### Now we're going to test the other file.
#
# print("\n\n", "******* Now, we are going to test the other CSV file, for the Residence side*************", "\n")
#
# # reading csv file
# with open(residenceData, 'r') as csvfile:
#     # creating a csv reader object
#     csvreader = csv.reader(csvfile)
#     # extracting field names through first row
#     fieldsResi = next(csvreader)
#     # extracting each data row one by one
#     for row in csvreader:
#         rowsResi.append(row)
#
#         # get total number of rows
#     print("Total no. of rows: %d" % (csvreader.line_num))
#
# # printing the field names
# print('Field names are: ' + ', '.join(field for field in fieldsResi))
#
# #  printing first 5 rows
# print('\nFirst 5 rows are:\n')
# for row in rowsResi[:5]:
#     # parsing each column of a row
#     for col in row:
#         # print out an item and doesn't new line, just adds a space
#         print(col, end=' ')
#     print('')  # gets it on a new line
#
# print("testing indexing: ", rowsResi[1][1])
# print("testing indexing: ", rowsResi[1][2])
# print("testing indexing: ", rowsResi[1][3])
# print("testing indexing: ", rowsResi[1][4])
#
# print("\n\nNow, using both Sender and Residence files:")
# print("Test 1:")
# if rowsResi[1][3] == rowsSenders[4][3]:
#     print(rowsResi[1][3], " ", rowsSenders[4][3], "<--- This is a match")
# else:
#     print(rowsResi[1][3], " ", rowsSenders[4][3], "<--- This is not a match")
#
# print("Test 2:")
# if rowsResi[1][3] == rowsSenders[5][3]:
#     print(rowsResi[1][3], " ", rowsSenders[5][3], "<--- This is a match")
# else:
#     print(rowsResi[1][3], " ", rowsSenders[5][3], "<--- This is not a match")
#
# print("Test 3:")
# if rowsResi[8][5] == rowsSenders[12][5]:
#     print(rowsResi[8][5], " ", rowsSenders[12][5], "<--- This is a match")
# else:
#     print(rowsResi[8][5], " ", rowsSenders[12][5], "<--- This is not a match")
#

