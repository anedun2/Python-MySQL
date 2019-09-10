import mysql.connector

#Establishing connection with the MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="invoice"
)

mycursor = mydb.cursor()

#Function for Report 1
def report1(date1, date2):
    #query to print all invoices for a specified time period
    query = ("SELECT * FROM invoiceheader WHERE invoicedate BETWEEN %s AND %s")
    mycursor.execute(query, (date1, date2))
    myresult = mycursor.fetchall()
    print ("Report 1: ")
    for x in myresult:
        print("Invoice Num:",x[0],"Date:",x[1],"Invoice Amount:","$",x[2])

#Function for Report 2    
def report2(date1, date2):
    #query to print all invoices for a specified time period where invoice amount does not match the sum of all detailamount column values for an invoice
    query = ("SELECT i.*, id.sumdetail, (i.invoiceamount-id.sumdetail) as discrepancy FROM invoiceheader AS i LEFT JOIN (SELECT id.invoicenum, sum(detailamount) AS sumdetail FROM invoicedetail AS id GROUP BY id.invoicenum) id ON i.invoicenum = id.invoicenum WHERE invoicedate BETWEEN %s AND %s HAVING id.sumdetail <> i.invoicenum OR id.sumdetail IS NULL ;")
    mycursor.execute(query, (date1, date2))
    myresult = mycursor.fetchall()
    print ("Report 2: ")
    for x in myresult:
        print("Invoice Num:",x[0],"Date:",x[1],"Invoice Amount:","$",x[2],"Detail Amount:","$",x[3],"Discrepancy:","$",x[4])

#Function for Report 3
def report3(date1,date2):
    #query to print all tracking nos. for a specified time period where detail amount does not match the sum of all charge amount column values for an invoice and tracking no
    query = ("SELECT i.invoicenum, i.invoicedate, t.trackingno, t.sum1 as detailamount, t.sum2 as chargeamount,(t.sum1-t.sum2) as discrepancy FROM invoiceheader i, (SELECT d.invoicenum, d.trackingno, sum( d.detailamount ) AS sum1, c.sum2 FROM invoicedetail d, (select invoicenum, trackingno,sum( chargeamount ) as sum2 from invoicecharges GROUP BY invoicenum, trackingno) c WHERE d.invoicenum = c.invoicenum AND d.trackingno = c.trackingno GROUP BY d.invoicenum, d.trackingno) t where invoicedate between %s and %s and i.invoicenum=t.invoicenum and (t.sum1-t.sum2) != 0 ")  
    mycursor.execute(query, (date1, date2))
    myresult = mycursor.fetchall()
    print ("Report 3: ")
    for x in myresult:
        print("Invoice Num:",x[0],"Date:",x[1],"Tracking No.:",x[2],"Invoice Amount:","$",x[3],"Detail Amount:","$",x[4],"Discrepancy:","$",x[5])

#Entering the date input        
date1 = input("Enter starting date in format yyyy-mm-dd: ")
date2 = input("Enter ending date in format yyyy-mm-dd: ")

report1(date1, date2)
report2(date1, date2)
report3(date1, date2)