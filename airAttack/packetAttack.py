import requests
import time
import json

class packet:
	def __init__(self):  
		self.sessionId = None
		self.legSellKey = None
		self.fareSellKey = None

	def dailyPrices(self, flightData):
		url = 'https://api-book.tigerairtw.com/graphql'
		res = requests.post(url, 
					  json={"operationName":"appLiveDailyPrices",
			 "variables":{"input":{"sessionId":self.sessionId,
						  "origin":flightData['origin'],
						  "destination":flightData['destination'],
						  "userCurrency":flightData['userCurrency'],
						  "pricingCurrency":flightData['userCurrency'],
						  "since":flightData['since'],
						  "until":flightData['until'],
						  "source":"resultPagePriceBrick"}},
						  "query":"query appLiveDailyPrices($input: QueryLiveDailyPricesInput!) {\n  appLiveDailyPrices(input: $input) {\n    origin\n    destination\n    date\n    currency\n    amount\n    fareLabels {\n      id\n    }\n  }\n}\n"})
		# print(json.dumps(res.json(), indent=4))
		return res.json()['data']['appLiveDailyPrices']

	def updateFlightSearchSession(self, departureDate, returnDate):
		url = 'https://api-book.tigerairtw.com/graphql'
		res = requests.post(url, 
					  json={"operationName":"appUpdateFlightSearchSessionSearchDate",
                               "variables":{"input":{"id":self.sessionId,
                                                     "departureDate":departureDate, #"2024-03-03",
                                                     "returnDate":returnDate}},#None}},
                                                     "query":"fragment UpdateSearchCondition on FlightSearchSession {\n  id\n  adultCount\n  childCount\n  infantCount\n  departureDate\n  returnDate\n  promotionCode\n  stationPairs {\n    origin\n    destination\n  }\n  userCurrency\n  pricingCurrency\n  flightType\n  expiredAt\n  portal {\n    slug\n    type\n    startAt\n    endAt\n    departStartAt\n    departEndAt\n    returnStartAt\n    returnEndAt\n    flightType\n    maxPassengerCount\n    defaultPromotionCode\n    promotionCodeLength\n    isPromotionCodeDisplayed\n    voucherDetail {\n      totalLength\n      discardStartLength\n      discardEndLength\n    }\n    creditCardDetail {\n      length\n      binCode\n    }\n    portalEmbargoDates {\n      startAt\n      endAt\n    }\n  }\n}\n\nmutation appUpdateFlightSearchSessionSearchDate($input: UpdateFlightSearchSessionSearchDateInput) {\n  appUpdateFlightSearchSessionSearchDate(input: $input) {\n    ...UpdateSearchCondition\n  }\n}\n"})
		print(json.dumps(res.json(), indent=4))
		time.sleep(1)
		res = requests.post(url, 
					  json={"operationName":"appUpdateFlightSearchSession",
			 				"variables":{"input":{"id":self.sessionId,"userCurrency":"TWD"}},"query":"mutation appUpdateFlightSearchSession($input: UpdateFlightSearchSessionInput!) {\n  appUpdateFlightSearchSession(input: $input) {\n    userCurrency\n  }\n}\n"})
		print(json.dumps(res.json(), indent=4))
		return (res.status_code < 400)
	
	def FlightSearchSession(self):
		url = 'https://api-book.tigerairtw.com/graphql'
		res = requests.post(url, 
                    json={"operationName":"appFlightSearchSession",
                               "variables":{"id":self.sessionId},
                               "query":"fragment PriceBreakdown on PriceBreakdown {\n  isPaymentCompleted\n  isLastPaymentDeclined\n  canCheckout\n  canDeduct\n  payments {\n    channel\n    status\n    authStatus\n    authStatusCategory\n    accountNumber\n    paymentNumber\n    methodType\n    methodCode\n    pricingCurrency\n    pricingAmount\n    billingCurrency\n    billingAmount\n    exchangeRate\n    approvedDateTime\n  }\n  summary {\n    userCurrency\n    total\n    balanceDue\n    totalPaid\n    totalPaymentFee\n    exchangeRate\n    paymentMethodCode\n    legs {\n      state\n      origin\n      destination\n      total\n      duration\n      overnight\n      canCheckIn\n      segments {\n        carrierCode\n        flightNumber\n        origin\n        destination\n        departureTime\n        arrivalTime\n        duration\n        overnight\n        productClass\n        passengerServices {\n          total\n          passengers {\n            passengerNumber\n            isRegisterExtraSeat\n            seat {\n              state\n              seat\n              seatGroup\n              type\n              feeCode\n              paxType\n              quantity\n              currency\n              unitAmount\n              totalAmount\n            }\n            items {\n              available\n              state\n              ssrCode\n              ssrCodeType\n              type\n              feeCode\n              paxType\n              quantity\n              currency\n              unitAmount\n              totalAmount\n              isGifted\n            }\n          }\n        }\n      }\n      fares {\n        total\n        paxTypes {\n          paxType\n          items {\n            type\n            feeCode\n            chargeType\n            paxType\n            quantity\n            currency\n            unitAmount\n            totalAmount\n          }\n        }\n      }\n      taxAndFees {\n        total\n        items {\n          type\n          feeCode\n          chargeType\n          paxType\n          quantity\n          currency\n          unitAmount\n          totalAmount\n        }\n      }\n    }\n  }\n}\n\nquery appFlightSearchSession($id: String!) {\n  appFlightSearchSession(id: $id) {\n    id\n    adultCount\n    childCount\n    infantCount\n    departureDate\n    returnDate\n    promotionCode\n    stationPairs {\n      origin\n      destination\n    }\n    userCurrency\n    pricingCurrency\n    flightType\n    soldContent {\n      soldLegs {\n        origin\n        destination\n        legSellKey\n        soldSegments {\n          fareSellKey\n          carrierCode\n          flightNumber\n          origin\n          destination\n          departureTime\n          arrivalTime\n          productClass\n          fareSellKey\n          userSoldPrices {\n            feeCode\n            type\n            paxType\n            quantity\n            currency\n            unitAmount\n            totalAmount\n          }\n        }\n      }\n      soldServices {\n        passengerNumber\n        ssrCode\n        ssrCodeType\n        isGifted\n        userSoldPrice {\n          feeCode\n          paxType\n          quantity\n          currency\n          unitAmount\n          totalAmount\n        }\n        soldServiceSegment {\n          carrierCode\n          flightNumber\n          origin\n          destination\n          departureTime\n        }\n      }\n      soldSeats {\n        passengerNumber\n        seatDesignator\n        seatGroup\n        userSoldPrice {\n          feeCode\n          paxType\n          quantity\n          currency\n          unitAmount\n          totalAmount\n        }\n        soldServiceSegment {\n          carrierCode\n          flightNumber\n          origin\n          destination\n          departureTime\n        }\n      }\n      extraSegmentPaxInfos {\n        passengerNumber\n        isRegisterExtraSeat\n        segmentNumber\n      }\n    }\n    expiredAt\n    passengers {\n      type\n      givenName\n      surname\n      passengerNumber\n      gender\n      birthday\n      nationality {\n        code2\n      }\n      nationalityCountry {\n        code2\n      }\n      passportNumber\n      passportExpireDate\n      passportCountry {\n        code2\n      }\n      memberNumber\n    }\n    infants {\n      givenName\n      surname\n      gender\n      birthday\n      nationality {\n        code2\n      }\n      nationalityCountry {\n        code2\n      }\n      passportNumber\n      passportExpireDate\n      passportCountry {\n        code2\n      }\n      bindingAdultPassengerNumber\n    }\n    contact {\n      givenName\n      surname\n      gender\n      countryCode\n      phoneNumber\n      email\n    }\n    priceBreakdown {\n      ...PriceBreakdown\n    }\n    paymentValidationError\n    portal {\n      title\n      type\n      slug\n      startAt\n      endAt\n      departStartAt\n      departEndAt\n      returnStartAt\n      returnEndAt\n      flightType\n      maxPassengerCount\n      defaultPromotionCode\n      promotionCodeLength\n      isPromotionCodeDisplayed\n      voucherDetail {\n        totalLength\n        discardStartLength\n        discardEndLength\n      }\n      creditCardDetail {\n        length\n        binCode\n      }\n      portalEmbargoDates {\n        startAt\n        endAt\n      }\n    }\n    voucherCode\n  }\n}\n"})

		print(json.dumps(res.json(), indent=4))
		return (res.status_code < 400)

	def setSellKey(self, res):
		amount = 9999999
		res = json.loads(json.dumps(res))
		# print(res['data']['appFlightSearchResult']['journeys'][0]['legs'][0]['availabilityLegs'])
		for leg in res['data']['appFlightSearchResult']['journeys'][0]['legs'][0]['availabilityLegs']:
			# print(leg['legSellKey'])
			# print(leg['fares'][0]['fareSellKey'])
			try:
				# print('-------------------------------------------')
				# print(json.dumps(leg, indent=4))
				if leg['fares'][0]['paxFares'][0]['ticketPrice']['fareAmount'] < amount:
					amount = leg['fares'][0]['paxFares'][0]['ticketPrice']['fareAmount']
					self.fareSellKey = leg['fares'][0]['fareSellKey']
					self.legSellKey = leg['legSellKey']
			except Exception as e:
				print(e)
				pass
		print('legSellKey: '+self.legSellKey)
		print('fareSellKey: '+self.fareSellKey)

	def FlightSearchResult(self):
		url = 'https://api-book.tigerairtw.com/graphql'
		res = requests.post(url, 
							json={"operationName":"appFlightSearchResult",
								"variables":{"id":self.sessionId},
								"query":"query appFlightSearchResult($id: String!) {\n  appFlightSearchResult(id: $id) {\n    id\n    sessionId\n    flightType\n    journeys {\n      legs {\n        origin\n        destination\n        departureDate\n        availabilityLegs {\n          origin\n          destination\n          legSellKey\n          duration\n          overnight\n          infantSoldOut\n          infantTooMany\n          availabilitySegments {\n            origin\n            destination\n            departureTime\n            arrivalTime\n            duration\n            overnight\n            carrierCode\n            flightNumber\n            availabilitySegmentDetails {\n              equipmentType\n              totalSeat\n              soldSeat\n              remainingSeat\n              subjectToGovernmentApproval\n              availabilitySegmentDetailSsrs {\n                ssrNestCode\n                ssrLid\n                ssrSold\n                ssrValueSold\n              }\n            }\n          }\n          fares {\n            sellable\n            availableCount\n            productClass\n            carrierCode\n            ruleNumber\n            fareSellKey\n            paxFares {\n              paxType\n              ticketPrice {\n                userCurrency\n                fareAmount\n                taxAmount\n                productClassAmount\n                promotionDiscountAmount\n                discountedFareAmount\n                totalAmountWithoutTax\n                discountedTotalAmountWithoutTax\n                totalAmount\n                discountedTotalAmount\n              }\n            }\n            fareLabels {\n              translations {\n                locale\n                name\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n"})
		self.setSellKey(res.json())
		return (res.status_code < 400)

	def updateFlightKey(self):
		url = 'https://api-book.tigerairtw.com/api/app/sell/flight'
		res = requests.post(url, 
							json={"sessionId":self.sessionId,
								"flightKeyPair":{"origin":"TPE",
												"destination":"OKA",
												"legSellKey":self.legSellKey,
												"fareSellKey":self.fareSellKey,
												"event":{"isTrusted":True}}})
		print('update status: '+res.reason)
		return (res.reason == 'OK')

	def UpdatePassengers(self, passengers_detail, contact_detail):
		url = 'https://api-book.tigerairtw.com/graphql'
		res = requests.post(url, 
							json={"operationName":"appUpdatePassengers",
								"variables":{"input":{"sessionId":self.sessionId,
							  							"passengers":passengers_detail,
														"infants":[],
														"contact":contact_detail}},
																	"query":"mutation appUpdatePassengers($input: UpdatePassengersInput!) {\n  appUpdatePassengers(input: $input)\n}\n"})

		print(json.dumps(res.json(), indent=4))
		return (res.status_code < 400)

	def check_out(self, creditCardDetail):
		url = 'https://api-book.tigerairtw.com/api/app/checkout/search-session/3ds2/ddc'
		res = requests.post(url, 
							json={"sessionId":self.sessionId,
								"primaryAccountNumber":creditCardDetail['primaryAccountNumber'], #"4005550000000019",
								"expiredMonth":creditCardDetail['expiredMonth'], #"04",
								"expiredYear":creditCardDetail['expiredYear'], #"2026",
								"cvv":creditCardDetail['cvv'], #"111",
								"cardHolderName":creditCardDetail['cardHolderName'], #"SADASD",
								"currency":creditCardDetail['currency']})#"TWD"})
		print(json.dumps(res.json(), indent=4))
		time.sleep(15)
		url = 'https://api-book.tigerairtw.com/api/app/checkout/search-session/3ds2/checkout'
		res = requests.post(url, 
							json={"sessionId":self.sessionId,
								"browserColorDepth":24,
								"browserScreenHeight":720,
								"browserScreenWidth":1280,
								"browserTimezoneOffsetInMinutes":-480,
								"primaryAccountNumber":creditCardDetail['primaryAccountNumber'], #"4005550000000019",
								"expiredMonth":creditCardDetail['expiredMonth'], #"04",
								"expiredYear":creditCardDetail['expiredYear'], #"2026",
								"cvv":creditCardDetail['cvv'], #"111",
								"cardHolderName":creditCardDetail['cardHolderName'], #"SADASD",
								"currency":creditCardDetail['currency']}) #"TWD"})
		print(res)
		print(res.text)
		return (res.status_code < 400)
