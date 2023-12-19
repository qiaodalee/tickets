class Data:
    def __init__(self):
        self.watch = True
        self.pay = False

        self.passengers = [{"gender":"male",
                            "passengerType":"ADT",
                            "givenName":"AA",
                            "surname":"AA",
                            "birthday":"2006-02-01",
                            "nationality":"TW",
                            "passportNumber":"ASCASDASDASD",
                            "passportCountry":None,
                            "passportExpireDate":"2026-02-20",
                            "memberNumber":""}]
        
        self.contact = {"gender":"male",
                        "givenName":"AA",
                        "surname":"AA",
                        "countryCode":"MO",
                        "phoneNumber":"12312312312",
                        "email":"dsaasd@asd.com"}
        
        self.creditCardDetail = {"primaryAccountNumber":"4005550000000019",
								"expiredMonth":"04",
								"expiredYear":"2026",
								"cvv":"111",
								"cardHolderName":"SADASD",
								"currency":"TWD"}
        self.request_flight_data = {                                
                                    "origin": "TPE",
                                    "destination": "KIX",
                                    "userCurrency": "TWD",
                                    "pricingCurrency": "TWD",
                                    "since": "2023-12-5",
                                    "until": "2024-3-20",
                                    }
        self.target_flight = {
                            'origin': None,
                            'destination': None,
                            'date': None,
                            'currency': None,
                            'amount': 999999,
                            'fareLabels': []
                            }
        
