import csv
from datetime import date
import random
import os 

class Account() :
     def __init__(self,name,ledger_file = "ledger.csv"):
          self.name = name
          self.ledger_file = ledger_file
          # cwd = os.cwd
          # self.my_path = os.path.join(cwd,self.name)
          # self.ledger = os.path.join(self.my_path,"ledger.csv")
          self.cwd= os.getcwd()
          self.folder_path = self.cwd+"/"+self.name


          if not os.path.exists(self.folder_path):
               os.mkdir(self.folder_path)
          

     def ledger(self,n_date, category, desc, mode_of_payment, amount):

          with open(self.ledger_file ,"a", encoding="utf-8") as f:
               values = {
                    "date": n_date,
                    "category": category,
                    "desc": desc,
                    "mode_of_payment": mode_of_payment,
                    "amount": amount,
               }
               write = csv.DictWriter(f, fieldnames=values.keys())
               if f.tell() == 0:
                    write.writeheader()
               write.writerow(values)


     def generate_random_data(self):
          """new"""
     
          categories = ["Food", "Rent", "tools", "Entertainment", "Travel"]
          descriptions = ["Car", "Restaurant", "bike", "Movie", "Grocerie"]
          modes_of_payment = ["Phonepe", "googlepay", "Cash", "card", "Paytm"]

          for _ in range(20):
               amount = round(random.randint(1000, 10000))
               category = random.choice(categories)
               desc = random.choice(descriptions)
               mode_of_payment = random.choice(modes_of_payment)
               year = random.randrange(2020, 2024)
               month = random.randrange(1, 13)
               day = random.randrange(1, 29)

               self.ledger(f"{year}-{month}-{day}", category, desc, mode_of_payment, amount)


     def read_ledger(self,filename):
          """read_ledger"""
          with open( filename, "r", encoding="utf-8") as f:
               read = csv.DictReader(f)
          return list(read)

          # cleaned_data = [{k: v.replace(',', '') for k, v in record.items()} for record in read]
          # return cleaned_data

     def credit_m(self,amount):

          with open(self.ledger_file, "r", encoding="utf-8") as f:
               data = list(csv.DictReader(f))

          current_balance = int(data[-1]["amount"])
          return float((current_balance) + amount)


     def debit_m(self,amount):

          with open( self.ledger_file, "r", encoding="utf-8") as f:
               data = list(csv.DictReader(f))

               current_balance = int(data[-1]["amount"])
               return float(current_balance - amount)


     def transaction(self,amount, category, desc, mode_of_payment, credit=False):

          current_date = date.today()
          if credit:
               amount = self.credit_m(amount)
               self.ledger(current_date, category, desc, mode_of_payment, amount)
               return f"{amount} amount credited "

          amount = self.debit_m(amount)
          self.ledger(current_date, category, desc, mode_of_payment, amount)
          return f"{amount} amount debited "

     # need to right path 
     
     def generate_category_report(self,filename):

          with open(filename, "r", encoding="utf-8") as f:
               data = list(csv.DictReader(f))

          value = ["date", "category", "desc", "amount"]
          up_data = [{keys: i[keys] for keys in value} for i in data]
          
          with open(self.folder_path + "/category.csv","a", encoding="utf-8", newline="") as f:
               writer = csv.DictWriter(f, fieldnames=value)
               writer.writeheader()
               writer.writerows(up_data)

          return "category.csv"


     # need to right path 
     def generate_payment_report(self,filename):

          with open(filename, "r", encoding="utf-8") as f:
               data = list(csv.DictReader(f))

          value = ["date", "mode_of_payment", "amount", "desc"]
          up_data = [{keys: i[keys] for keys in value} for i in data]

          with open(self.folder_path + "/payment.csv", "a", encoding="utf-8", newline="") as f:
               writer = csv.DictWriter(f, fieldnames=value)

               writer.writeheader()
               writer.writerows(up_data)
          return "payment.csv"


     def print_reports(self):
          "print"
          months = {}

          map_month = {
               "01": "Jan",
               "02": "Feb",
               "03": "Mar",
               "04": "Apr",
               "05": "May",
               "06": "Jun",
               "07": "Jul",
               "08": "Aug",
               "09": "Sep",
               "10": "Oct",
               "11": "Nov",
               "12": "Dec",
          }

          with open( self.ledger_file, "r", encoding="utf-8") as f:
               read = list(csv.DictReader(f))
               categories = sorted({i["category"] for i in read})
               in_cat = {
                    category: {
                         data["date"]: int(data["amount"])
                         for data in read
                         if category == data["category"]
                    }
                    for category in categories
               }

          for category, data in in_cat.items():
               for s_date, amount in data.items():
                    month, year = s_date.split("-")[1], s_date.split("-")[0]
                    m_year = f"{map_month.get(month, 'Jan')}/{year}"
                    if category not in months:
                         months[category] = {}
                    if m_year not in months[category]:
                         months[category][m_year] = 0
                    months[category][m_year] += amount

          result = ""
          header = ["Category"] + sorted(
               set(m_year for data in months.values() for m_year in data)
          )
          result += "\t".join(header) + "\n"
          for category, data in months.items():
               row = [category] + [str(data.get(m_year, 0)) for m_year in header[1:]]
               result += "\t".join(row) + "\n"

          return result


     def generate_txt(self):
          """generate"""


          with open(self.ledger_file, "r", encoding="utf-8") as f:
               data = list(csv.reader(f))

          with open(self.folder_path +"/report.txt", "w", encoding="utf-8") as file:
               x = csv.writer(file)
               for lines in data:
                    x.writerow(lines)

if __name__== "__main__":
    
    obj = Account("kunal")

    obj.generate_random_data()
    
    obj.print_reports()
    obj.generate_txt()
    obj.generate_category_report("ledger.csv")
    obj.generate_payment_report("ledger.csv")
    obj.credit_m(4000)
    obj.debit_m(2000)

    