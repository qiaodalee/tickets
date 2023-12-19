import sys
import json
import time

from webdriver import WebDriver
from url import URL
from log import Logger
from data import Data
from packetAttack import packet
from airAttack import AirAttack

# parser = argparse.ArgumentParser(description="Automatic booking system")

# parser.add_argument('-o', '--org', help='Specify the origin')
# parser.add_argument('-d', '--des', help='Specify the destination')
# parser.add_argument('-c', '--cost', help='Set the cost limit')
# parser.add_argument('-a', '--amount', help='Specify the tickets quantity')
# parser.add_argument('-b', '--back', help='For round-trip tickets')
# parser.add_argument('-s', '--speed', help='Specify speed 0 to 10, 0 is maxinum.')
# parser.add_argument('-n', '--name', help='Input your name, format: "LASTNAME FIRSTNAME", sample: "SHINCHUN LEE"')
# parser.add_argument('-p', '--phone', help='Input your phone number, format: "CountryCode PhoneNumber", sample: "886 0912345678"')


# args = parser.parse_args()
data = Data()
if len(sys.argv) > 1:
    contact = sys.argv[1]
    creditCard = sys.argv[2]
    flight = sys.argv[3]
    passengers = sys.argv[4:]

    # print(contact)
    # print(creditCard)
    # print(flight)
    # print(passengers)

    contact = json.loads(contact)
    creditCard = json.loads(creditCard)
    flight = json.loads(flight)
    for passenger in range(len(passengers)):
        passengers[passenger] = json.loads(passengers[passenger])
    
    data.contact['gender'] = passengers[0]['gender']
    data.contact['givenName'] = passengers[0]['givenName']
    data.contact['surname'] = passengers[0]['surname']
    data.contact['countryCode'] = contact['countryCode']
    data.contact['phoneNumber'] = contact['phoneNumber']
    data.contact['email'] = contact['email']

    data.creditCardDetail['primaryAccountNumber'] = creditCard['primaryAccountNumber']
    data.creditCardDetail['expiredMonth'] = creditCard['expiredMonth']
    data.creditCardDetail['expiredYear'] = creditCard['expiredYear']
    data.creditCardDetail['cvv'] = creditCard['cvv']
    data.creditCardDetail['cardHolderName'] = f'{passengers[0]["surname"]} {passengers[0]["givenName"]}'

    data.request_flight_data['origin'] = flight['origin']
    data.request_flight_data['destination'] = flight['destination']
    if (flight['amount'] != None):
        data.target_flight['amount'] = int(flight['amount'])
    if (flight['date'] != None):
        data.target_flight['date'] = flight['date']
    data.pay = flight['pay']
    data.watch = flight['watch']

    # time.sleep(30000)

    data.passengers = passengers

    print(data.passengers)





    # time.sleep(30000)

# if args.org:
#     data.request_flight_data['origin'] = args.org
# if args.des:
#     data.request_flight_data['destination'] = args.des
# if args.cost:
#     data.target_flight['amount'] = int(args.cost)
# if args.amount:
#     data.args['tixAmount'] = int(args.amount)
# if args.back:
#     data.args['roundTrip'] = args.back
# if args.speed:
#     data.args['speed'] = args.speed
# if args.name:
#     fname, lname = args.name.split('-')
#     data.admin['firstName'] = fname
#     data.admin['lastName'] = lname
# if args.phone:
#     country_code, phone_number = args.phone.split('-')
#     data.admin['dialCode'] = country_code
#     data.admin['phoneNumber'] = phone_number

airAttack = AirAttack(URL(), WebDriver(), Logger(), data, packet())
airAttack.start()

