import requests
import json
import pandas as pd

dehashedAPIKey = ''
dehashedEmail= ''
recordSize = ''
domainToParse = ''

def GetUserInput():
    global dehashedAPIKey
    global dehashedEmail
    global recordSize
    global domainToParse
    dehashedAPIKey = input('Please Enter Your pwnedAPIKey: ')
    print(' ')
    print(' ')
    dehashedEmail = input('Please Enter Your Dehashed Email: ')
    print(' ')
    print(' ')
    print('The DeHashed API Allows up to 5000 records per call (3000 is reccomended)')
    print(' ')
    recordSize = input('How many records would you like to parse? ---> ')
    domainToParse = input('Which domain name to lookup? (Ex: google.com, facebook.com) --> ')


def GETAPIData():
    dehashedHeaders = {
        'Accept':'application/json'
    }
    params = (
    ('query', 'domain:{}'.format(domainToParse)),
    ('size', '{}'.format(recordSize))
    )

    data = requests.get('https://api.dehashed.com/search',headers=dehashedHeaders, params=params, auth=('{}', '{}'.format(dehashedEmail,dehashedAPIKey)))

    with open('DeHashedData.json', 'w') as f:
        f.write(data.text)
        f.close()


def ParseDataFormat():
    data = open('DeHashedData.json', 'r') 
    table = []
    loadedJSON = json.load(data)
    for every in loadedJSON['entries']:
        table.append({
            'Email': every['email'],
            'Database Source': every['database_name'],
            'ip_address': every['ip_address'],
            'username': every['username'],
            'password': every['password'],
            'hashed_password': every['hashed_password'],
            'name': every['name'],
            'vin': every['vin'],
            'address': every['address'],
            'phone': every['phone']
        })
    df = pd.DataFrame(table)
    df.to_csv('ParsedDeHashedData.csv', index=False)


GetUserInput()
GETAPIData()
ParseDataFormat()


