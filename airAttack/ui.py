import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry 
from datetime import datetime
import subprocess
import json
import schedule
import time

class TicketSelectionApp:
    def __init__(self, root):
        self.user_entries = []
        self.contact_entries = {}
        self.creditCard_entries = {}
        self.flight_entries = {}

        self.root = root
        self.root.title("選擇票數")
        self.root.geometry("1200x600")   # 设置窗口初始大小
        self.root.resizable(True, True)  # 可调整宽度和高度
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.ticket_label = ttk.Label(self.main_frame, text="選擇票數", font=("Helvetica", 16, "bold"))
        self.ticket_label.grid(row=0, column=0)

        self.ticket_var = tk.IntVar()
        self.ticket_var.set(1)  # 初始值为1
        self.ticket_entry = ttk.Spinbox(self.main_frame, from_=1, to=8, textvariable=self.ticket_var, command=self.updateTicket)
        self.ticket_entry.grid(row=1, column=0)

        self.confirm_button = ttk.Button(self.main_frame, text="確認", command=self.change_content)
        self.confirm_button.grid(row=2, column=0)

        self.start_button = ttk.Button(self.main_frame, text="立即搶票", command=self.start)
        self.start_button.grid(row=3, column=0)

        self.confirm_button = ttk.Button(self.main_frame, text="設定搶票時間", command=self.setScechule)
        self.confirm_button.grid(row=4, column=0, columnspan=4)

        self.main_frame.columnconfigure((0), weight=1)

    def start(self):

        if (len(self.user_entries) == 0):
            try:
                subprocess.run(["python", "./airAttack/main.py"], check=True)
            except Exception:
                try:
                    subprocess.run(["python", "./main.py"], check=True)
                except:
                    subprocess.run(["python", "../main.py"], check=True)
            return
        for entries in range(len(self.user_entries)):
            self.user_entries[entries]['gender'] = self.user_entries[entries]['gender'].get()
            self.user_entries[entries]['surname'] = self.user_entries[entries]['surname'].get()
            self.user_entries[entries]['givenName'] = self.user_entries[entries]['givenName'].get()
            day = (self.user_entries[entries]['birthday'].get()).split('/')
            for d in range(len(day)):
                if (len(day[d]) != 2):
                    day[d] = '0'+day[d]
            if ( int(day[2]) > 24):
                day = f'20{day[2]}-{day[0]}-{day[1]}' 
            else:
                day = f'19{day[2]}-{day[0]}-{day[1]}' 
            self.user_entries[entries]['birthday'] = day
            self.user_entries[entries]['passportNumber'] = self.user_entries[entries]['passportNumber'].get()
            day = (self.user_entries[entries]['passportExpireDate'].get()).split('/')
            for d in range(len(day)):
                if (len(day[d]) != 2):
                    day[d] = '0'+day[d]
            self.user_entries[entries]['passportExpireDate'] = f'20{day[2]}-{day[0]}-{day[1]}'
            self.user_entries[entries] = json.dumps(self.user_entries[entries])
        self.contact_entries = {'countryCode':self.country_entries.get(),
                                'phoneNumber':self.phone_entries.get(),
                                'email':self.mail_entries.get()}
        self.creditCard_entries = {'primaryAccountNumber':self.creditNumber_entries.get(),
                                   'expiredMonth':self.creditMonth_entries.get(),
                                   'expiredYear':self.creditYear_entries.get(),
                                   'cvv':self.creditCVV_entries.get()}
        day = (self.departure_Date_entry.get()).split('/')
        for d in range(len(day)):
            if (len(day[d]) != 2):                                              
                day[d] = '0'+day[d]
                       
        self.flight_entries = {'origin':self.origin_entries.get(),
                               'destination':self.des_entries.get(),
                               'date': f'20{day[2]}-{day[0]}-{day[1]}' if self.departure_Date_checkbox_var.get() == True else None,
                               'amount': None if self.budget_entries.get() == "" else self.budget_entries.get(),
                               'pay': self.pay_checkbox_var.get(),
                               'watch': self.check_checkbox_var.get()
                               }
        try:
                subprocess.run(["python", "./airAttack/main.py", json.dumps(self.contact_entries), json.dumps(self.creditCard_entries), json.dumps(self.flight_entries)]+self.user_entries, check=True)
        except Exception:
            print('no content')
            try:
                subprocess.run(["python", "./main.py", json.dumps(self.contact_entries), json.dumps(self.creditCard_entries), json.dumps(self.flight_entries)]+self.user_entries, check=True)
            except:
                subprocess.run(["python", "../main.py", json.dumps(self.contact_entries), json.dumps(self.creditCard_entries), json.dumps(self.flight_entries)]+self.user_entries, check=True)
            

    def createEntry(self, row, frame, text):
        label = ttk.Label(frame, text=text)
        label.grid(row=row, column=0, sticky="E")

        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, sticky="W")

        return entry
    
    def updateTicket(self):
        pass

    def setScechule(self):
        # 創建子視窗
        dialog = tk.Toplevel(self.root)
        dialog.title("日期與時間輸入")

        # 獲取當前日期和時間
        now = datetime.now()

        # 創建日期輸入框
        date_label = ttk.Label(dialog, text="設定日期:")
        date_label.grid(row=0, column=0, padx=10, pady=10)
        date_entry = ttk.Entry(dialog)
        date_entry.insert(0, now.strftime("%Y-%m-%d"))
        date_entry.grid(row=0, column=1, padx=10, pady=10)

        # 創建時間輸入框
        time_label = ttk.Label(dialog, text="設定時間:")
        time_label.grid(row=1, column=0, padx=10, pady=10)
        time_entry = ttk.Entry(dialog)
        time_entry.insert(0, now.strftime("%H:%M:%S"))
        time_entry.grid(row=1, column=1, padx=10, pady=10)

        # 定義一個函式，用於獲取輸入的日期和時間
        def set():
            now_label = ttk.Label(dialog, text="剩餘時間:")
            now_label.grid(row=2, column=0, padx=10, pady=10)
            deff = (datetime.strptime(f'{date_entry.get()} {time_entry.get()}', "%Y-%m-%d %H:%M:%S") -  datetime.now()).total_seconds()
            now_entry = ttk.Label(dialog, text=deff)
            now_entry.grid(row=2, column=1, padx=10, pady=10)
            runTime = int(deff)
            # 設定每日定時執行的時間，這裡是每日的00:00
            schedule.every().day.at(f'{time_entry.get()}').do(self.start)

            # 主迴圈，用來持續檢查是否有定時任務需要執行
            while(True):
                schedule.run_pending()
                runTime -= 1
                if (runTime < 0):
                    return
                print(str(runTime))
                time.sleep(1)  # 1秒後再次執行該函式


        # 創建確定按鈕
        ok_button = ttk.Button(dialog, text="確定", command=set)
        ok_button.grid(row=3, column=0, columnspan=2, pady=10)

    def update_user_data_interface(self):
        if (self.ticket_count > 4):
            split=4
            self.main_frame.rowconfigure((0,1,2,3), weight=1)
        else:
            split=int(self.ticket_count)
            self.main_frame.rowconfigure((0,1,2), weight=1)
        for i in range(split):
            self.main_frame.columnconfigure(i, weight=1)

        top_frame = ttk.Frame(self.main_frame, padding=0, style="My.TFrame")
        top_frame.grid(row=0, column=0, sticky="nsew", columnspan=4)
        top_frame.columnconfigure(0, weight=1)

        self.user_data_label = ttk.Label(top_frame, text="使用者資料", font=("Helvetica", 16, "bold"))
        self.user_data_label.grid(row=0, column=0)

        self.user_entries = []
        for i in range(self.ticket_var.get()):
            user_frame = ttk.Frame(self.main_frame, padding=0, style="My.TFrame")
            user_frame.grid(row=(i // 4)+1, column=i % 4, padx=5, pady=5, sticky="nsew")

            row = 1

            user_label = ttk.Label(user_frame, text=f"使用者{i + 1}")
            user_label.grid(row=row, column=0, padx=1, pady=1, sticky="W")

            radio_var = tk.StringVar()
            maile_radio_button = ttk.Radiobutton(user_frame, text="男", variable=radio_var, value="male")
            woman_radio_button = ttk.Radiobutton(user_frame, text="女", variable=radio_var, value="female")
            maile_radio_button.grid(row=row, column=0, sticky="E")
            woman_radio_button.grid(row=row, column=1, sticky="W")
            row += 1

            surname = self.createEntry(row, user_frame, f"姓氏:")
            row += 1

            givenName = self.createEntry(row, user_frame, f"名字:")
            row += 1

            birthday_label = ttk.Label(user_frame, text=f"生日:")
            birthday_label.grid(row=row, column=0, padx=10, pady=10, sticky="E")

            birthday_entry = DateEntry(user_frame, width=12, background='darkblue',
                                       foreground='white', borderwidth=2)
            birthday_entry.grid(row=row, column=1, padx=10, pady=10, sticky="W")
            row += 1

            passNum = self.createEntry(row, user_frame, f"護照號碼:")
            row += 1

            passportExpireDate_label = ttk.Label(user_frame, text=f"護照號碼到期日:")
            passportExpireDate_label.grid(row=6, column=0, padx=10, pady=10, sticky="E")

            passportExpireDate_entry = DateEntry(user_frame, width=12, background='darkblue',
                                       foreground='white', borderwidth=2)
            passportExpireDate_entry.grid(row=6, column=1, padx=10, pady=10, sticky="W")
            row += 1

            self.user_entries.append({'gender':radio_var,
                                      "passengerType":"ADT",
                                      'surname':surname,
                                      'givenName':givenName,
                                      'birthday':birthday_entry,
                                      "nationality":"TW",
                                      'passportNumber':passNum,
                                      "passportCountry":None,
                                      'passportExpireDate':passportExpireDate_entry,
                                      "memberNumber":""})

        if (self.ticket_count>4):
            row = 3
        else:
            row = 2

        bottom_frame = ttk.Frame(self.main_frame, padding=0, style="My.TFrame")
        bottom_frame.grid(row=row, column=0, columnspan=4, sticky="nsew")
        bottom_frame.columnconfigure((0,1,2), weight=1)

        contact_frame = ttk.Frame(bottom_frame, padding=0, style="My.TFrame")
        contact_frame.grid(row=row, column=0)

        creditCard_frame = ttk.Frame(bottom_frame, padding=0, style="My.TFrame")
        creditCard_frame.grid(row=row, column=1)

        flight_frame = ttk.Frame(bottom_frame, padding=0, style="My.TFrame")
        flight_frame.grid(row=row, column=2)
        

        self.country_entries = self.createEntry(row, contact_frame, f"城市號碼:")
        self.creditNumber_entries = self.createEntry(row, creditCard_frame, f"信用卡號碼:")
        self.origin_entries = self.createEntry(row, flight_frame, f"出發地:")
        row += 1

        self.phone_entries = self.createEntry(row, contact_frame, f"電話號碼:")
        self.creditMonth_entries = self.createEntry(row, creditCard_frame, f"信用卡到期月:")
        self.des_entries = self.createEntry(row, flight_frame, f"目的地:")
        row += 1

        self.mail_entries = self.createEntry(row, contact_frame, f"email:")
        self.creditYear_entries = self.createEntry(row, creditCard_frame, f"信用卡到期年:")
        self.budget_entries = self.createEntry(row, flight_frame, f"預算(預設99999):")
        row += 1

        self.creditCVV_entries = self.createEntry(row, creditCard_frame, f"CVV:")
        self.departure_Date_checkbox_var = tk.BooleanVar()
        departure_Date_checkbox = ttk.Checkbutton(flight_frame, text="指定出發日(預設選擇最低票價):", variable=self.departure_Date_checkbox_var)
        departure_Date_checkbox.grid(row=row, column=0, padx=10, pady=10, sticky="E")
        self.departure_Date_entry = DateEntry(flight_frame, width=12, background='darkblue',
                                       foreground='white', borderwidth=2)
        self.departure_Date_entry.grid(row=row, column=1, padx=10, pady=10, sticky="W")
        row += 1

        self.confirm_button = ttk.Button(bottom_frame, text="開始搶票", command=self.start)
        self.confirm_button.grid(row=row, column=0, columnspan=4)
        self.pay_checkbox_var = tk.BooleanVar()
        pay_checkbox = ttk.Checkbutton(flight_frame, text="自動付款", variable=self.pay_checkbox_var)
        pay_checkbox.grid(row=row, column=0, padx=10, pady=10, sticky="E")
        row += 1

        self.check_checkbox_var = tk.BooleanVar()
        check_checkbox = ttk.Checkbutton(flight_frame, text="顯示結果", variable=self.check_checkbox_var)
        check_checkbox.grid(row=row, column=0, padx=10, pady=10, sticky="E")

        self.confirm_button = ttk.Button(bottom_frame, text="設定搶票時間", command=self.setScechule)
        self.confirm_button.grid(row=row, column=0, columnspan=4)
        root.style = ttk.Style()
        self.root.style.configure("My.TFrame", background="lightblue")

    
    def change_content(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.root.title("填寫使用者資料")

        self.ticket_count = self.ticket_var.get()
        self.update_user_data_interface()

        
        
    def show_success_message(self):
        user_data = [(user_entry.get(), birthday_entry.get()) for user_entry, birthday_entry in self.user_entries]

        print("用户数据:", user_data)

        messagebox.showinfo("成功", "資料更新成功！")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketSelectionApp(root)
    root.mainloop()
