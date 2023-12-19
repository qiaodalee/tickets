class URL:
    def __init__(self):
        self.index = 'https://booking.tigerairtw.com/zh-TW/index'
        self.admin = 'https://api-membership.tigerairtw.com/api/app/auth/login'
        self.graphql = 'https://api-book.tigerairtw.com/graphql'
        self.flight_result = 'https://booking.tigerairtw.com/zh-TW/flight-result'
        self.destination = 'https://api-book.tigerairtw.com/api/general/available-destinations?locale=zh-TW&origin='
        self.generate_token = 'https://api-wr.tigerairtw.com/generate_token'
        self.request_id = 'https://api-wr.tigerairtw.com/assign_queue_num'

    def get_url(self, action):
        if (action == "index") :
            return self.index
        elif (action == "admin") :
            return self.admin
        elif (action == "graphql") :
            return self.graphql
        elif (action == "flight_result") :
            return self.flight_result
        elif (action == "destination") :
            return self.destination
        elif (action == "generate_token") :
            return self.generate_token
        elif (action == "request_id") :
            return self.request_id
