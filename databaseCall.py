from __future__ import division
from __future__ import print_function

import csv
import boto3
from boto3.dynamodb.conditions import Key
import argparse
from csv import reader

residenceData = "ExampleDataForResidences.csv"
senderData = "ExampleDataForSenders.csv"


def getDatabase():
    endpointUrl = "https://dynamodb.us-east-1.amazonaws.com"
    dynamodb = boto3.resource('dynamodb', "us-east-1" , endpoint_url=endpointUrl)
    table = dynamodb.Table('cyftr_fourth')   # used to be as an argument. We hard coded lol
    return table


def getQuery(table, room, lastName):
    response = table.query(
            KeyConditionExpression=(Key('Room').eq(room) & Key('Last Name').eq(lastName))
        )
#    print("RESPONSE   ", response['Items'])
    return response['Items']

