from flask import Flask, render_template, request
# Next two lines are for the REST API
import json
#import sourceCode
import databaseCall


# This line is a must for Flask
application = Flask(__name__)


# An example of adding a REST API:
# theDogApiHeaders = {'x-api-key' : 'd3ddba63-0fc4-4961-856c-5078391b472d'}

# the '/' refers to the root page. It is the page someone lands on when they simply enter the URL
@application.route('/')
def index():
   return 'Hello World, from Cyftr!!'

# Referencing another page, "cyftr.com/about.html". You would add and code an about.html file in the
# templates directory so that this would work
@application.route('/uglyMVP.html')
def uglyMVPstartPage():
   return render_template('uglyMVP.html')


@application.route('/update')
def update():
    lname = request.args.get('lname')
    fname = request.args.get('fname')
    address = str(request.args.get('addrOne'))
    table = databaseCall.getDatabase()

    item = {}
    key = "Address"
    item[key] = address
    key = "Last Name"
    item[key] = lname
    # hold = lname+fname
    # key = "Last Name+First Name"
    # item[key] = hold
    print(item)
    table.put_item(Item=item)
    return ("good")


@application.route('/verify')
def verify():

    information = request.args.get('lname')
    address = str(request.args.get('addrOne'))
    print(information)
    print(address)
    # run verification function
    # query database
    table = databaseCall.getDatabase()
    databaseInfo = databaseCall.getQuery(table, address, information)

    if len(databaseInfo) == 1:
        return ("Accurate")
    elif len(databaseInfo)>1:
        return ("Partially Accurate")
    else:
        return ("Not Accurate")
    print("INFO ", databaseInfo[0])
    #next((item for item in databaseInfo if item["First Name"] == "Waller"), None)
    print(str(databaseInfo[0]['First Name']))     # this doesn't work
    return str(databaseInfo)     # breaks without the str. makes it a string

   # print the result of the function
#   return information
#   return render_template('uglyMVP.html', data=information)


# This is an example of referencing an HTML file that uses an API
# @application.route('/psoneCoonhound.html')
# def breed1():
#    url = 'https://api.thedogapi.com/v1/breeds/search?q=Black%20and%20Tan%20Coonhound'
#    req = requests.get(url,headers=theDogApiHeaders)
#    data = json.loads(req.content)
#    return render_template('/psoneCoonhound.html',data=data)


# This is just a python thing. Watch a YouTube video if you'd like to learn more about it
if __name__ == '__main__':
   application.run(debug = True)