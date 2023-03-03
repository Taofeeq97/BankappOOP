import csv
import random


class Customer:
    all_customers = []

    def __init__(self, first_name, email, password, account_type, account_number, balance=0):
        self.first_name = first_name
        self.email = email
        self.password = password
        self.account_type = account_type
        self.balance = balance
        self.account_number = account_number
        Customer.all_customers.append(self)

    @classmethod
    def create_account(cls, name, email, password, account_type, balance=0):
        account_number = random.randint(100000, 999999)
        customer = cls(name, email, password, account_type, account_number, balance)
        customer.save_customer()

    def save_customer(self):
        with open('customers_details.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [self.first_name,self.email,self.password,self.account_type, self.account_number, self.balance])

    def login(self, customer_file, email, password):
        with open(customer_file, 'r') as file:
            reader = csv.reader(file)
            customer_details = []
            for row in reader:
                customer_details.append(row)
            for customer in customer_details:
                if customer[1] == email and customer[2] == password:
                    return True
        return None

    def withdraw(self, amount, email):
        customer=self.get_customer_by_email(customer_file='customers_details.csv',email=email)
        if amount <= int(customer.balance):
            customer.balance=int(customer.balance)-amount
            customer.update_customer_details(customer_file='customers_details.csv',email=email,new_balance=customer.balance)
            return customer.balance


        else:
            print('Insufficient fund')

    def transfer(self, recipient_email,sender_email, amount):
        recipient = self.get_customer_by_email(customer_file='customers_details.csv', email=recipient_email)
        sender=self.get_customer_by_email(customer_file='customers_details.csv',email=sender_email)
        if int(sender.balance)>=amount:
            sender_balance=int(sender.balance)
            recipient_balance=int(recipient.balance)
            sender_balance=sender_balance-amount
            sender.update_customer_details(customer_file='customers_details.csv',email=sender_email,new_balance=sender_balance)
            recipient_balance=recipient_balance+amount
            recipient.update_customer_details(customer_file='customers_details.csv',email=recipient_email,new_balance=recipient_balance)
        else:
            return 'Insufficient fund in the sender account'


    def check_balance(self):
        with open('customers_details.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == email:
                    return f'Your current balance is {(row[5])}'
        return None

    @classmethod
    def get_customer_by_email(cls, customer_file, email):
        with open(customer_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == email:
                    return cls(*row)
        return None

    def update_customer_details(self, customer_file, email, new_balance):
        with open(customer_file, 'r') as file:
            reader = csv.reader(file)
            customers = []
            for row in reader:
                customers.append(row)
            for customer in customers:
                if customer[1] == email:
                    customer[5] = str(new_balance)
        with open(customer_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(customers)


class Staff(Customer):

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def staff_login(self, staff_file, name, password):
        with open(staff_file, 'r') as file:
            reader = csv.reader(file)
            staff_details = []
            for row in reader:
                staff_details.append(row)
            for staff in staff_details:
                if staff[0] == name and staff[1] == password:
                    return True
        return None

    def staff_deposit(self, amount, customer_email, staff_name, staff_password):
        customer = Staff.get_customer_by_email('customers_details.csv', customer_email)
        staff=Staff.get_staff('staff_details.csv',name=staff_name,password=staff_password)
        if staff[0]==staff_name and staff[1]==staff_password:
            if staff[2]=='unsuspended':
                customer_balance=int(customer.balance)
                customer_balance+=amount
                customer.update_customer_details(customer_file='customers_details.csv',email=customer_email,new_balance=customer_balance)
                return f'Deposit successfull customer balance is {customer_balance}'
            else:
                return 'You have been suspended by the Admin, visit HR'

    def staff_withdrawal(self, amount, customer_email, staff_name, staff_password):
        customer = Staff.get_customer_by_email('customers_details.csv', customer_email)
        staff = Staff.get_staff('staff_details.csv', name=staff_name, password=staff_password)
        if staff[0] == staff_name and staff[1] == staff_password:
            if staff[2]=='unsuspended':
                customer_balance = int(customer.balance)
                customer_balance -= amount
                customer.update_customer_details(customer_file='customers_details.csv', email=customer_email,
                                                 new_balance=customer_balance)
                return f'Withdrawal successfull customer balance is {customer_balance}'
            else:
                return 'you have been suspended by the Admin visit the HR'

    def staff_transfer(self,staff_name, staff_password,sender_email, recipient_email, amount):
        sender = Staff.get_customer_by_email('customers_details.csv', sender_email)
        recipient = Staff.get_customer_by_email('customers_details.csv', recipient_email)
        staff = Staff.get_staff('staff_details.csv', name=staff_name, password=staff_password)
        if staff[0] == staff_name and staff[1] == staff_password:
            if staff[2]=='unsuspended':
                sender_balance = int(sender.balance)
                if sender_balance>=amount:
                    sender_balance -= amount
                    recipient_balance=int(recipient.balance)
                    recipient_balance+=amount
                    sender.update_customer_details(customer_file='customers_details.csv', email=sender_email,
                                                     new_balance=sender_balance)
                    recipient.update_customer_details(customer_file='customers_details.csv',email=recipient_email,new_balance=recipient_balance)
                    return f'transfer successful customers balance {sender_balance}'
                else:
                    return 'Insufficient Sender Balance'
            else:
                return 'You have been suspended by the Admin, visit the HR '


    def change_staff_password(self, staff_name, new_staff_password):
        self.update_staff_details(Staff,name=staff_name,new_password=new_staff_password)
        return 'password changed successfully'
    @classmethod
    def get_customer_by_email(cls, customer_file, email):
        with open(customer_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == email:
                    return Customer(*row)

    @classmethod
    def get_staff(cls, staff_file, name, password):
        with open(staff_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == name and row[1]==password:
                    return row
    def check_balance(self, email):
        customer = self.get_customer_by_email('customers_details.csv', email)
        return f'customers balance is {customer.balance}'

    def update_staff_details(self, staff_file, name, new_password):
        with open('staff_details.csv', 'r') as file:
            reader = csv.reader(file)
            staffs = []
            for row in reader:
                staffs.append(row)
            for staff in staffs:
                if staff[0] == name:
                    staff[1] = new_password
        with open('staff_details.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(staffs)

class Admin:

    def __init__(self, admin_password):
        self.admin_password=admin_password

    def admin_login(self, admin_file, admin_password):
        with open(admin_file, 'r') as file:
            reader = csv.reader(file)
            admin_details = []
            for row in reader:
                admin_details.append(row)
            for admin in admin_details:
                if admin[1] == admin_password:
                    return True
        return None

    def create_staff(self, name, password, status='unsuspended'):
        staff=name,password,status
        with open('staff_details.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(staff)
        return 'staff created successfully'

    def view_customer(self):
        with open('customers_details.csv',mode='r') as file:
            reader=csv.reader(file)
            for row in reader:
                print(row)

    def view_staff(self):
        with open('staff_details.csv',mode='r') as file:
            reader=csv.reader(file)
            for row in reader:
                print(row)

    @classmethod
    def get_staff(cls, staff_file, name):
        with open(staff_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == name and row[1]:
                    return row

    def suspend_staff(self, name):
        with open('staff_details.csv', 'r') as file:
            reader = csv.reader(file)
            staffs = []
            for row in reader:
                staffs.append(row)
            for staff in staffs:
                if staff[0] == name:
                    staff[2] = 'suspended'
                    print(f'You have suspend staff {staff[0]}')
                else:
                    print(f'No unsuspended staff named {name}')
        with open('staff_details.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(staffs)


    def unsuspend_staff(self, name):
        with open('staff_details.csv', 'r') as file:
            reader = csv.reader(file)
            staffs = []
            for row in reader:
                staffs.append(row)
            for staff in staffs:
                if staff[0] == name:
                    staff[2] = 'unsuspended'
                    print(f'You have re-activate staff {staff[0]}')
                else:
                    print(f'No suspended staff named {name}')
        with open('staff_details.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(staffs)




'''Control flow'''

print("\nPlease select an option:")
print("1. IF YOU ARE NEW CUSTOMER")
print("2. IF YOU ARE CUSTOMER")
print("3. IF YOU ARE STAFF")
print("4. IF YOU ARE THE ADMIN")
print("5. Exit")
programe_on=True
while programe_on:
    choice=input('Enter your choice')
    if choice=='1':
        name=input('Enter your account name')
        email = input('Enter your email account')
        password = input('Enter your account password')
        account_type=input('Enter the account type')
        Customer.create_account(name,email,password,account_type)
    if choice == '2':
        print('\Please login to your account')
        email=input('Input your account email')
        password=input('input your password')
        while Customer.login(Customer,'customers_details.csv',email,password):
            print("\nPlease select an option:")
            print("1. Withdraw money")
            print("2. Transfer money")
            print("3. Check balance")
            print("4. Exit")
            choice = input('Enter your choice')
            if choice=='1':
                amount=int(input('Enter the amount you want to transfer'))
                Customer.withdraw(Customer,amount,email)
            if choice=='2':
                reciever_email=input('The email address of the recipient')
                amount = int(input('Enter the amount you want to transfer'))
                Customer.transfer(Customer,recipient_email=reciever_email,sender_email=email,amount=amount)
            if choice=='3':
                print(Customer.check_balance(Customer))
            if choice=='4':
                break

        else:
            print('Invalid login credentials')
    if choice=='3':
        print('\Please login to your staff account')
        staff_name = input('Input your staff name')
        staff_password = input('input your staff password')
        while Staff.staff_login(Staff,staff_file='staff_details.csv',name=staff_name,password=staff_password):
            print("\nPlease select an option:")
            print("1. Withdraw for customer")
            print("2. Deposit for customer")
            print("3. Transfer for customer")
            print("4. Check customers balance")
            print("5. Edit your password")
            print("6. Back")
            choice = input("Enter your choice: ")
            if choice=='1':
                customer_email=input('Enter customer email')
                amount=int(input('Input the amount you want to withdraw'))
                staff=Staff(staff_name,staff_password)
                print(Staff.staff_withdrawal(staff,amount=amount,customer_email=customer_email,staff_name=staff_name,staff_password=staff_password))
                break
            if choice == '2':
                customer_email = input('Enter customer email')
                amount = int(input('Input the amount you want to deposit'))
                staff=Staff(name=staff_name,password=staff_password)
                print(Staff.staff_deposit(staff,amount=amount,customer_email=customer_email,staff_name=staff_name,staff_password=staff_password))
                break
            if choice=='3':
                sender_email = input('Enter the sender email')
                recipient_email = input('Enter the reciever email')
                amount = int(input('Input the amount you want to tansfer'))
                staff=Staff(name=staff_name,password=staff_password)
                print(Staff.staff_transfer(staff,staff_name=staff_name,staff_password=staff_password,sender_email=sender_email,recipient_email=recipient_email,amount=amount))
            if choice=='4':
                customer_email = input('Enter the customer email')
                staff=Staff(name=staff_name,password=staff_password)
                print(Staff.check_balance(staff,email=customer_email))
            if choice=='5':
                new_password=input('Enter New password')
                staff=Staff(name=staff_name,password=staff_password)
                print(Staff.change_staff_password(staff,staff_name=staff_name,new_staff_password=new_password))
            if choice=='6':
                break

            break
        else:
            print('Invalid staff login details')
    if choice == '4':
        print('\Please login to admin account')
        admin_password = input('input admin password')
        admin=Admin(admin_password=admin_password)
        while Admin.admin_login(admin,admin_file='admin_detail.csv',admin_password=admin_password):
            print("\nPlease select an option:")
            print("1. Create staff Account")
            print("2. View Bank customers")
            print("3. View bank staffs")
            print("4. suspend a bank staffs account")
            print("5. Activate a suspended account")
            print("6. View Bank logs")
            print("7. Back")
            choice = input("Enter your choice: ")
            if choice == '1':
                staff_name=input('Enter staff name')
                staff_password=input('Enter staff password')
                print(Admin.create_staff(Admin,name=staff_name,password=staff_password))
            if choice == '2':
                Admin.view_customer(Admin)
            if choice == '3':
                Admin.view_staff(Admin)
            if choice == '4':
                staff_to_be_suspended=input('Input the name of the staff to be suspended')
                Admin.suspend_staff(Admin,name=staff_to_be_suspended)
            if choice== '5':
                staff_to_be_activated=input('Input the name of the staff tp be reactivated')
                Admin.unsuspend_staff(Admin,name=staff_to_be_activated)
            if choice== '7':
                break
        else:
            print('Invalid admin login password')
    if choice=='5':
        break









