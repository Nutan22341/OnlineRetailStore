import mysql.connector
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='nutan@2004'
)
cursor  = mydb.cursor()
cursor.execute("use temp")

def Print():
    cursor.execute("select* from Vendor")
    for data in cursor.fetchall():
        print("-------------------------")
        print("Vendor ID: ",data[0])
        print("Vendor Name: ",data[1])
        print("Vendor Age: ",data[2])
        print("Vendor EMAIL: ",data[3])
        print("Vendor Phone Number: ",data[5])
        print("-------------------------")


def add():
    vendor_id = int(input("Enter vendor ID: "))
    cursor.execute("select* from Vendor")
    vendor = cursor.fetchall()
    for i in vendor:
        if(i[0]==vendor_id):
            print("THE VENDOR ID ALREADY EXISTS")
            return
    vendor_name = input("Enter vendor name: ")
    vendor_age = int(input("Enter vendor age: "))
    phone_number = int(input("Enter phone number: "))
    vendor_email = input("Enter vendor email (press Enter if none): ")
    # admin_id = int(input("Enter admin ID: "))
    cursor.execute(f"insert into Vendor values({vendor_id},'{vendor_name}',{vendor_age},{phone_number},'{vendor_email}',1)")
    mydb.commit()


def remove():
    print("Enter the id of the vendor which you want to remove:")
    id = int(input())
    cursor.execute(f"Delete from Vendor where {id} = vendor_id")
    mydb.commit()


def admin():
    while(True):
        print("1. ADD NEW VENDOR ")
        print("2. PRINT VENDOR LIST: ")
        print("3. Show Customers Stats with total spending")
        print("4. Total Payment from each type")
        print("5. EXIT: ")
        b = input("Enter the operation number:")
        if(b=="1"):
            add()
        elif(b=="2"):
            Print()
        elif (b=="3"):
            cursor.execute("SELECT Customer.customer_id, first_name, last_name, SUM(Product.product_price) AS total_spending FROM Customer JOIN ShoppingOrder ON Customer.customer_id = ShoppingOrder.customer_id JOIN ShoppingCart ON ShoppingOrder.orderId = ShoppingCart.shopping_cart_id JOIN Product ON ShoppingCart.product_id = Product.product_id GROUP BY Customer.customer_id, first_name, last_name;")
            data=cursor.fetchall()
            for item in data:
                print("------------------------")
                print("Customer ID: ",item[0])
                print("Customer Name: ",item[1],item[2])
                print("Total Spending: ",item[3])
                print("------------------------")
        elif(b=="4"):
            cursor.execute("SELECT pt.payment_name, SUM(p.payment_amount) AS total_amount FROM Payment p INNER JOIN PaymentType pt ON p.payment_type_id = pt.payment_type_id GROUP BY pt.payment_name;")
            data=cursor.fetchall()
            for item in data:
                print("------------------------")
                print("Payment Name: ",item[0])
                print("Total Amount: ",item[1])
                print("------------------------")
        elif(b=="5"):
            print("Going Back.....")
            return
        else:
            print("Wrong Option!!!!!")

def insertCustomer():
    first_name = input("Enter first name: ")
    middle_name = input("Enter middle name (press Enter if none): ")
    last_name = input("Enter last name: ")
    phone_number = int(input("Enter phone number: "))
    email_id = input("Enter email ID: ")
    age = int(input("Enter age: "))
    street_no = int(input("Enter street number: "))
    street_name = input("Enter street name: ")
    house_no = input("Enter house number: ")
    pin_code = input("Enter pin code: ")
    city = input("Enter city: ")
    state_name = input("Enter state name: ")
    cursor.execute(f"insert into customer values({customer_id},'{first_name}','{middle_name}','{last_name}',{phone_number},'{email_id}',{age},{street_no},'{street_name}',{house_no},'{pin_code}','{city}','{state_name}',1)")
    mydb.commit()
    print("Successfully Inserted......")

def customer(customerID):
    while True:
        print("1. View My Orders")
        print("2. Show Past Transactions")
        print("3. Place and Order for the item")
        print("4. EXIT")
        choice=input("Enter your option: ")
        if(choice=="1"):
            cursor.execute(f"select * from shoppingorder where customer_id = {customerID}")
            data = cursor.fetchall()
            if(data==[]):
                print("YOU HAVE NOT PLACE ANY ORDER YET!")
            else:
                for item in data:
                    print("-----------------------------------------")
                    print("Order ID: ",item[0])
                    print("Order Date: ",item[1].strftime("%Y-%m-%d"))
                    print("Delivery Address: ",item[2])
                    print("-----------------------------------------")
        elif choice=="2":
            # NHI MILA TABLE M :-(
            cursor.execute(f"select* from payment where customer_id = {customerID} ")
            paymentData = cursor.fetchall()
            if(paymentData == []):
                print("YOU DO NOT HAVE ANY TRANSACTION YET!")
            else:
                # paymentTypeId =  paymentData[]
                for item in paymentData:
                    print("-----------------------------------------")
                    print("payment_id: ",item[0])
                    print("payment_amount: ",item[1])
                    print("expirydate: ",item[2].strftime("%Y-%m-%d"))
                    print("-----------------------------------------")
        elif choice=="3":
            cursor.execute(f"select* from product")
            for items in cursor.fetchall():
                print("-------------------------------------------")
                print("Product ID: ",items[0])
                print("Product Name: ",items[2])
                print("Product Description: ",items[1])
                print("Product Price: ",items[3])
                print("-------------------------------------------")
            print()
            print("The above is the list of product, enter the Id and product quantity which you want to order:")
            id = int(input("Enter Id of the product here: "))
            quantity = int(input("Enter the number of items which you want to buy: "))
            cursor.execute("SELECT * FROM Inventory WHERE product_quantity >= %s AND product_id = %s", (quantity, id))
            order_data = cursor.fetchall()
            if(order_data == []):
                print("Either the product does not exist or there is out of stock!")
            else:
                cursor.execute("Select Max(orderID) from shoppingorder")
                order_id = cursor.fetchall()[0][0]
                cursor.execute(f"select * from Customer where customer_id = {customerID}")
                data=cursor.fetchall()
                address = str(data[0][7])+" "+data[0][8]+" "+str(data[0][9])+" "+data[0][10]+" "+data[0][11]+" "+data[0][12]
                cursor.execute(f"INSERT INTO ShoppingOrder VALUES ({int(order_id)+1},CURRENT_DATE(),'{address}',{customerID})")
                print("The order has been placed!")
                # but how to handle the quantity of stock
                """
                update kr diya inverntory hi direct us product id k corresponding 
                """
                cursor.execute(f"UPDATE INVENTORY SET product_quantity = product_quantity - {quantity} where product_id = {id}")
                mydb.commit()
        elif choice=="4":
            print("Going Back.....")
            return
        else:
            print("Wrong Option!!!!!")


print("Choose the option given below:-")
while(1):
    print()
    print("1. LOGIN AS A ADMIN: ")
    print("2. LOGIN AS A CUSTOMER: ")
    print("3. SIGN UP AS A CUSTOMER: ")
    print("4. LOGIN AS A VENDOR: ")
    print("5. EXIT: ")
    print()
    choice = input("Enter your option: ")
    if(choice=="1"):
        adminId = input("ENTER THE ADMIN ID: ")
        adminName = input("ENTER THE ADMIN NAME: ")
        cursor.execute("select* from Admin1")
        adminData = cursor.fetchall()
        flag = 1
        for i in adminData:
            data=i
            if(data[0]==int(adminId)) and data[2]==adminName :
                flag = 0
                print("YOU ARE WELECOME AS A POST OF ADMIN :)")
                option = input("Enter YES if you want to perform admin operation: ")
                if(option.upper() =="YES"):
                    admin()
                else:
                    print("YOU DO NOT WANT TO PERFORM OPERATION RELATED TO ADMIN.....")
                break
        if(flag==1):
            print("YOU HAVE ENTERED THE WRONG DETAILS OF ADMIN")
    elif(choice=="2"):
        customerId = input("ENTER YOUR CUSTOEMR ID: ")
        customerName = input("ENTER YOUR CUSTOMER NAME: ")
        customerEmail = input("ENTER YOUR CUSTOMER EMAIL: ")
        cursor.execute(f"select* from Customer where customer_id = {int(customerId)} and first_name = '{customerName}' AND email_id = '{customerEmail}' ")
        customerData = cursor.fetchall()
        if(customerData==[]):
            print("YOU HAVE ENTERED WRONG DETAILS!!!!!")
        else:
            print("YOU ARE WELECOME:)")
            customer(customerId)
    elif(choice=="3"):
        cursor.execute("select* from Customer")
        cust = cursor.fetchall()
        customer_id = int(input("Enter customer ID: "))
        flag2=0
        for i in cust:
            if(i[0]==(customer_id)):
                print("THE CUSTOMER ID ALREADY EXIT")
                flag2=1
                break
        if(flag2==0):
            insertCustomer()
    elif(choice=="4"):
        vendorID = int(input("Enter the vendor Id: "))
        name = input("Enter the vendor name: ")
        cursor.execute(f"select* from Vendor where vendor_id = {vendorID} and vendor_name = '{name}'")
        vendor_data = cursor.fetchall()
        if(vendor_data == []):
            print("You have entered wrong details:")
        else:
            print("Here is the functionality of Vendor: ")
            check = input("Enter YES if you want to check vendor notification of yours: ")
            if(check.upper()=="YES"):
                cursor.execute(f"select* from VendorNotifications where vendor_id={vendorID}")
                # print(cursor.fetchall())
                notification_data = cursor.fetchall()
                if(notification_data==[]):
                    print("You do not have any notification yet!")
                    print("Loging Out......")
                else:
                    for items in notification_data:
                        print("------------------")
                        print("Notification:--")
                        print(items[1])
                        print("------------------")
                        print("Updating Product Qunatity......")
                        id=items[1].split()[3]
                        cursor.execute(f"update inventory set product_quantity = product_quantity+10 where product_id = {id}")
                        print("Successfully Updated.......")
                    cursor.execute(f"Delete from VendorNotifications where vendor_id={vendorID}")
                    mydb.commit()
                    print("")
            else:
                print("Loging Out....")
                continue

    elif(choice=="5"):
        print("YOU ARE OUT!")
        break
    else:
        print("Wrong Option!!!!!")