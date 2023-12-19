import time
import json
import random

class AirAttack():
    def __init__(self, url, webdriver, logger, data, packet):
        self.api = url
        self.driver = webdriver
        self.logger = logger
        self.data = data
        self.packet = packet

    def randomTime(self):
        return random.random()*float(3)+1

    def check_result(self, errorMsg, info, error):
        if (errorMsg == None):
            if (info != None):
                self.logger.info(str(info[0]).upper() + str(info[1:]))
            time.sleep(0.5)
        else:
            self.logger.error(f'{error}\nerrorMsg: {errorMsg}')
            time.sleep(5)

    def end(self):
        while(input('Enter "quit" to quit > ') != 'quit'):
            time.sleep(1)
        try:    
            self.driver.quit()
        except:
            pass
        exit()

    def start(self):
        # 開啟虎航首頁
        errorMsg = self.driver.open(self.api.get_url('index'))
        self.check_result(errorMsg, f'{self.api.get_url("index")} is opened', f'{self.api.get_url("index")} is not opened')
    
        """
        # #選擇幣別
        # while(True):
        #     errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="currency"]')
        #     self.check_result(errorMsg, None, f'cannot click flightType')

        #     errorMsg = self.driver.click_event('xpath', '//div[@data-e2e-test-id="TWD"]')
        #     self.check_result(errorMsg, f'currency: TWD', f'cannot click flightType')

        #     if ( errorMsg == None):
        #         break
        """

        # 選擇單程or來回
        errorMsg = self.driver.click_event('xpath', '//div[@data-e2e-test-id="flightType-oneWay"]')
        self.check_result(errorMsg, f'flightType: oneWay', f'cannot click flightType')

        # 選擇出發地
        errorMsg = self.driver.click_event('xpath', '//div[@data-e2e-test-id="origin"]')
        self.check_result(errorMsg, None, f'cannot click origin')

        errorMsg = self.driver.click_event('xpath', f'//span[contains(text(), "{self.data.request_flight_data["origin"]}")]')
        self.check_result(errorMsg, f'origin: TPE', f'cannot click origin')

        # 選擇目的地
        while(True):
            errorMsg = self.driver.click_event('xpath', '//div[@data-e2e-test-id="destination"]')
            self.check_result(errorMsg, None, f'cannot click destination')

            self.driver.load_page(60, f'//span[contains(text(), "{self.data.request_flight_data["destination"]}")]')

            errorMsg = self.driver.click_event('xpath', f'//span[contains(text(), "{self.data.request_flight_data["destination"]}")]')
            self.check_result(errorMsg, f'destination: KIX', f'cannot click destination')
            if ( errorMsg == None):
                break
        
        if (len(self.data.passengers) > 1):
            print('------------------------------------------------------------------')
            errorMsg = self.driver.click_event('xpath', f'//div[@class="col-sm-3"]')
            self.check_result(errorMsg, f'origin: TPE', f'cannot click tixamount')
            for i in range(len(self.data.passengers) - 1):
                errorMsg = self.driver.click_event('xpath', f'//i[text()="add"]')
                self.check_result(errorMsg, f'origin: TPE', f'cannot click tix add')
            errorMsg = self.driver.click_event('xpath', f'//div[@class="col-sm-3"]')
            self.check_result(errorMsg, f'origin: TPE', f'cannot click tix add')
 

        # 搜尋當天機票
        errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="search"]')
        self.check_result(errorMsg, f'searching...', f'cannot click search')
        

        # 觸發真人驗證
        verificationCode = self.driver.load_page(5, '//button[@data-e2e-test-id="ok"]')
        if (verificationCode == None):
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="ok"]')
            self.check_result(errorMsg, f'clicking ok...', f'cannot click ok')
            self.driver.load_page(5, '//iframe[@title="reCAPTCHA"]')
            errorMsg = self.driver.click_event('xpath', '//iframe[@title="reCAPTCHA"]')
            self.check_result(errorMsg, f'clicking recapcha...', f'cannot click recapcha')
            imageSelect = self.driver.load_page(5, '//iframe[@title="reCAPTCHA"]')
            if (imageSelect == None):
                self.logger.warning('please select image to pass')

        """
        # self.driver.load_page(60, '//div[@class="text-caption"]')
        # time.sleep(3)
        """

        # 抓出sessionId
        while(self.packet.sessionId == None):
            logs = self.driver.get_logs()
            for log in logs:
                message = log["message"]
                if 'graphql' in message:
                    try:
                        self.packet.sessionId = json.loads(json.loads(message)['message']['params']['request']['postData'])['variables']['input']['sessionId']
                        self.logger.info (json.dumps(json.loads(json.loads(message)['message']['params']['request']['postData']), indent=4))
                        break
                    except Exception as error:
                        pass
        print(self.data.target_flight['date'])
        if(self.data.target_flight['date'] == None):
            # 搜尋某個時間區段的每日最低票價
            try:
                flight_infos = self.packet.dailyPrices(self.data.request_flight_data)
                if(flight_infos == None):
                    self.logger.error('interval error')
                    self.end()
            except Exception as error:
                self.logger.error(error)
                self.end()

            # 找出時間區段中最低的票價日期
            try:
                """
                # flight_info = requests.post(self.api.get_url('flight_info'), json = request_flight_data)
                # flight_infos = json.loads(json.dumps(flight_info.json()))['data']['appLiveDailyPrices']
                """
                for info in flight_infos:
                    self.logger.info (info['date'] + ': ' + str(info['amount']))
                    if ( info['amount'] < self.data.target_flight['amount'] and info['amount']> 0):
                        self.data.target_flight = info

                self.logger.info (f'mini_cost_flight\n{json.dumps(self.data.target_flight, indent=4)}')
            except Exception as error:
                self.logger.error(error)
                self.end()
        
        # 更新搜尋的航班
        try:
            isUpdateSession = self.packet.updateFlightSearchSession(self.data.target_flight['date'], None)
            if (isUpdateSession == False):
                self.logger.error('updateFlightSearchSession false')
                self.end()
        except Exception as error:
            self.logger.error(error)
            self.end()

        # 搜尋航班資訊
        try:
            isUpdateSession = self.packet.FlightSearchSession()
            if (isUpdateSession == False):
                self.logger.error('FlightSearchSession false')
                self.end()
        except Exception as error:
            self.logger.error(error)
            self.end()
        
        # 搜尋航班資訊結果
        try:
            isUpdateSession = self.packet.FlightSearchResult()
            if (isUpdateSession == False):
                self.logger.error('FlightSearchResult false')
                self.end()
        except Exception as error:
            self.logger.error(error)
            self.end()

        # 更新票價key
        try:
            isUpdateSession = self.packet.updateFlightKey()
            if (isUpdateSession == False):
                self.logger.error('updateFlightKey false')
                self.end()
        except Exception as error:
            self.logger.error(error)
            self.end()

        """
        # #尋找最低價日期
        # errorMsg = self.driver.click_event('xpath', '//i[text()="search"]')
        # self.check_result(errorMsg, None, f'failed to search the min cost date')

        # errorMsg = self.driver.click_event('xpath', '(//input[@data-e2e-test-id="search-form-departure-date"])[2]')
        # errorMsg = self.driver.input_event('xpath', '(//input[@data-e2e-test-id="search-form-departure-date"])[2]', self.data.target_flight['date'])
        # self.check_result(errorMsg, f'scanning min cost date: {self.data.target_flight["date"]}', f'failed to search the min cost date')

        # errorMsg = self.driver.click_event('xpath', '(//button[@data-e2e-test-id="search"])[2]')
        # self.check_result(errorMsg, f'searching the min cost date', f'failed to search the min cost date')

        # errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="ok"]')
        # self.check_result(errorMsg, None, f'failed to search the min cost date')

        # #選擇最低價航班
        # target_flight_amount = "{:,}".format(self.data.target_flight['amount'])
        # errorMsg = self.driver.load_page(60, f'(//div[text()="{target_flight_amount}"])[last()]')
        # self.check_result(errorMsg, f'page loading', f'failed to load')

        # element = self.driver.find('xpath', f'(//div[text()="{target_flight_amount}"])[last()]')
        # element.location_once_scrolled_into_view
        # time.sleep(1)
        # errorMsg = self.driver.click_event('xpath', f'(//div[text()="{target_flight_amount}"])[last()]')
        # self.check_result(errorMsg, f'choose the min cost: {target_flight_amount}', f'failed to choose')

        # #使用最低價方案
        # self.driver.load_page(60, '//button[@data-e2e-test-id="class-tigerLight"]')
        # errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="class-tigerLight"]')
        # self.check_result(errorMsg, None, f'failed to choose')

        # errorMsg = self.driver.load_page(60, '//div[@class="text-caption"]')
        # self.check_result(errorMsg, f'page loading', f'failed to load page')

        # #同意cookie
        # errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="accept"]')
        # self.check_result(errorMsg, None, f'failed to load page')

        """
        if (self.data.watch == True):
            try:
                time.sleep(3)
                self.driver.refreshPage()
                time.sleep(3)
                self.driver.element_hidden("document.getElementsByClassName('q-dialog__inner flex no-pointer-events q-dialog__inner--minimized q-dialog__inner--bottom fixed-bottom justify-center q-dialog__inner--fullwidth')[0].classList.add('hidden');")
            except Exception as e:
                print('Error occured: '+ str(e))

            self.driver.scroll_page("window.scrollTo(0, document.body.scrollHeight);")

            #下一步
            self.driver.load_page(60, '//button[@data-e2e-test-id="next" and @tabindex="1"]')
            time.sleep(1)
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="next"]')
            self.check_result(errorMsg, None, f'failed to load page')

            #會員登入
            self.driver.load_page(60, '//button[@data-e2e-test-id="visitor"]')
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="visitor"]')
            self.check_result(errorMsg, f'log in', f'failed to load page')

        # 更新乘客、聯絡人資料
        try:
            isUpdateSession = self.packet.UpdatePassengers(self.data.passengers, self.data.contact)
            if (isUpdateSession == False):
                self.logger.error('UpdatePassengers false')
                self.end()
        except Exception as error:
            self.logger.error(error)
            self.end()


        # # 付款
        if ( self.data.pay == True):
            try:
                isUpdateSession = self.packet.check_out(self.data.creditCardDetail)
                if (isUpdateSession == False):
                    self.logger.error('check_out false')
                    self.end()
            except Exception as error:
                self.logger.error(error)
                self.end()

        """
        # # self.driver.switch_page(-1)

        # # self.driver.load_page(60, '//input[@type="email"]')
        # # errorMsg = self.driver.input_event('xpath', '//input[@type="email"]', self.data.admin['email'])
        # # self.check_result(errorMsg, f'scanning email: {self.data.admin["email"]}', f'failed to scanning')

        # # errorMsg = self.driver.input_event('xpath', '//input[@type="password"]', self.data.admin['password'])
        # # self.check_result(errorMsg, f'scanning password: {self.data.admin["password"]}', f'failed to scanning')

        # # self.driver.switch_page(0)
        # # time.sleep(self.randomTime())

        # #開始填寫護照、個人資料
        # errorMsg = self.driver.load_page(60, f'//input[@data-e2e-test-id="passport-number"]')
        # self.check_result(errorMsg, f'page loading', f'failed to load page')
        # element = self.driver.find('xpath', '//input[@data-e2e-test-id="passport-number"]')
        # for i in range( 1, len(element.size)+1):
        #     print(i)
        #     errorMsg = self.driver.click_event('xpath', f'(//div[@data-e2e-test-id="male"])[{i}]')
        #     self.check_result(errorMsg, None, f'failed to choose sexual ')

        #     errorMsg = self.driver.input_event('xpath', f'(//input[@data-e2e-test-id="given-name"])[{i}]', self.data.admin['firstName'])
        #     self.check_result(errorMsg, f'scanning passport-number: {self.data.fake_passport["passportNumber"]}', f'failed to scanning')
            
        #     errorMsg = self.driver.input_event('xpath', f'(//input[@data-e2e-test-id="surname"])[{i}]', self.data.admin['lastName'] + chr(i+65))
        #     self.check_result(errorMsg, f'scanning passport-number: {self.data.fake_passport["passportNumber"]}', f'failed to scanning')
            
        #     errorMsg = self.driver.input_event('xpath', f'(//input[@data-e2e-test-id="birthday"])[{i}]', self.data.admin['birthday'])
        #     self.check_result(errorMsg, f'scanning passport-expire-date: {self.data.fake_passport["passportExpireDate"]}', f'failed to scanning')

        #     errorMsg = self.driver.input_event('xpath', f'(//input[@data-e2e-test-id="nationality"])[{i}]', 'CN')
        #     self.check_result(errorMsg, f'scanning dial-code: {self.data.admin["dialCode"]}', f'failed to scanning')

        #     errorMsg = self.driver.click_event('xpath', f'//div[@data-e2e-test-id="CN"]')
        #     self.check_result(errorMsg, None, f'failed to scanning')

        #     errorMsg = self.driver.input_event('xpath', f'(//input[@data-e2e-test-id="passport-number"])[{i}]', self.data.fake_passport['passportNumber'])
        #     self.check_result(errorMsg, f'scanning passport-number: {self.data.fake_passport["passportNumber"]}', f'failed to scanning')

        #     errorMsg = self.driver.input_event('xpath', f'(//input[@data-e2e-test-id="passport-expire-date"])[{i}]', self.data.fake_passport['passportExpireDate'])
        #     self.check_result(errorMsg, f'scanning passport-expire-date: {self.data.fake_passport["passportExpireDate"]}', f'failed to scanning')

        # self.driver.scroll_page("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(1)
        # errorMsg = self.driver.input_event('xpath', '//input[@data-e2e-test-id="dial-code"]', self.data.admin['dialCode'])
        # self.check_result(errorMsg, f'scanning dial-code: {self.data.admin["dialCode"]}', f'failed to scanning')

        # errorMsg = self.driver.click_event('xpath', f'//div[@data-e2e-test-id="{self.data.admin["dialCode"]}"]')
        # self.check_result(errorMsg, None, f'failed to scanning')

        # errorMsg = self.driver.input_event('xpath', '//input[@data-e2e-test-id="phone-number"]', self.data.admin["phoneNumber"])
        # self.check_result(errorMsg, f'scanning phone-number: {self.data.admin["phoneNumber"]}', f'failed to scanning')

        # errorMsg = self.driver.input_event('xpath', '//input[@data-e2e-test-id="email"]', self.data.admin['email'])
        # self.check_result(errorMsg, None, f'failed to scanning')

        # errorMsg = self.driver.input_event('xpath', '//input[@data-e2e-test-id="confirm-email"]', self.data.admin['email'])
        # self.check_result(errorMsg, None, f'failed to scanning')
        """
        if (self.data.watch == True):
            self.driver.refreshPage()
            time.sleep(3)

            try:
                self.driver.element_hidden("document.getElementsByClassName('q-dialog__inner flex no-pointer-events q-dialog__inner--minimized q-dialog__inner--bottom fixed-bottom justify-center q-dialog__inner--fullwidth')[0].classList.add('hidden');")
            except Exception as e:
                print('Error occured: '+ str(e))

            #下一步，進入加購餐點頁面
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="next"]')
            self.check_result(errorMsg, None, f'failed to next')
            self.driver.load_page(60, '//div[@class="text-caption"]')

            try:
                time.sleep(3)
                self.driver.element_hidden("document.getElementsByClassName('q-dialog__inner flex no-pointer-events q-dialog__inner--minimized q-dialog__inner--bottom fixed-bottom justify-center q-dialog__inner--fullwidth')[0].classList.add('hidden');")
            except Exception as e:
                print('Error occured: ' + str(e))

            #下一步，進入加購選位頁面
            self.driver.scroll_page("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.randomTime())
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="next"]')
            self.check_result(errorMsg, None, f'failed to next')

            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="ok"]')
            self.check_result(errorMsg, None, f'failed to next')
            self.driver.load_page(60, '//button[@data-e2e-test-id="next"]')
            time.sleep(self.randomTime())

            try:
                time.sleep(3)
                self.driver.element_hidden("document.getElementsByClassName('q-dialog__inner flex no-pointer-events q-dialog__inner--minimized q-dialog__inner--bottom fixed-bottom justify-center q-dialog__inner--fullwidth')[0].classList.add('hidden');")
            except Exception as e:
                print('Error occured: '+ str(e))

            #下一步，進入加購彈性航班頁面
            try:
                element = self.driver.find('xpath', '//button[@data-e2e-test-id="next"]')
                element.location_once_scrolled_into_view
            except Exception as error:
                self.driver.scroll_page("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.randomTime())
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="next"]')
            self.check_result(errorMsg, None, f'failed to next')
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="ok"]')
            self.check_result(errorMsg, f'page loading', f'failed to load page')
            self.driver.load_page(60, '//div[@class="text-caption"]')

            try:
                time.sleep(3)
                self.driver.element_hidden("document.getElementsByClassName('q-dialog__inner flex no-pointer-events q-dialog__inner--minimized q-dialog__inner--bottom fixed-bottom justify-center q-dialog__inner--fullwidth')[0].classList.add('hidden');")
            except Exception as e:
                print('Error occured: '+ str(e))

            #下一步，進入付款頁面
            self.driver.scroll_page("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.randomTime())
            errorMsg = self.driver.click_event('xpath', '//button[@data-e2e-test-id="next"]')
            self.check_result(errorMsg, None, f'failed to next')
            self.driver.load_page(60, '//input[@data-e2e-test-id="credit-card"]')

            try:
                time.sleep(3)
                self.driver.element_hidden("document.getElementsByClassName('q-dialog__inner flex no-pointer-events q-dialog__inner--minimized q-dialog__inner--bottom fixed-bottom justify-center q-dialog__inner--fullwidth')[0].classList.add('hidden');")
            except Exception as e:
                print('Error occured: '+ str(e))

        """
        # #填入信用卡資料
        # errorMsg = self.driver.input_event('xpath', '//input[@data-e2e-test-id="credit-card"]', self.data.fake_credit_card['creditCard'])
        # self.check_result(errorMsg, f'scanning credit-card: {self.data.fake_credit_card["creditCard"]}', f'failed to scanning')


        # errorMsg = self.driver.input_event('xpath', '//input[@data-e2e-test-id="card-holder"]', self.data.fake_credit_card["cardHolder"])
        # self.check_result(errorMsg, f'scanning card-holder: {self.data.fake_credit_card["cardHolder"]}', f'failed to scanning')


        # errorMsg = self.driver.click_event('xpath', '//div[@data-e2e-test-id="expired-month"]')
        # self.check_result(errorMsg, None, f'failed to scanning')


        # errorMsg = self.driver.click_event('xpath', f'//div[@data-e2e-test-id="{self.data.fake_credit_card["expiredMonth"]}"]')
        # self.check_result(errorMsg, f'scanning expired-month: {self.data.fake_credit_card["expiredMonth"]}', f'failed to scanning')

        # errorMsg = self.driver.click_event('xpath', '//div[@data-e2e-test-id="expired-year"]')
        # self.check_result(errorMsg, None, f'failed to scanning')

        # errorMsg = self.driver.click_event('xpath', f'//div[@data-e2e-test-id="{self.data.fake_credit_card["expiredYear"]}"]')
        # self.check_result(errorMsg, f'scanning expired-year: {self.data.fake_credit_card["expiredYear"]}', f'failed to scanning')

        # errorMsg = self.driver.input_event('xpath', '//input[@data-e2e-test-id="cvv"]', self.data.fake_credit_card["cvv"])
        # self.check_result(errorMsg, f'scanning cvv: {self.data.fake_credit_card["cvv"]}', f'failed to scanning')
        """
        
        self.end()
