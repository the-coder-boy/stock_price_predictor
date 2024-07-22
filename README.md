def main():
  print("\t\t\t\tMain Menu\t\t\t\t", "1.", "2.", "3.", "4.", "5.", "6.", sep="\n")

def show_databases():
  import mysql.connector as mc
  db = mc.connect(host = "localhost", user = "root", password = "dav123")
  cursor = db.cursor()
  cursor.execute("show databases;")
  print("The databases present in the MySQL Server are:")
  for i in cursor.fetchall():
    print(i)
  db.commit()
  db.close()

def create_database(name):
  import mysql.connector as mc
  db = mc.connect(host = "localhost", user = "root", password = "dav123")
  cursor = db.cursor()
  cursor.execute("create database '{}'".format(name))
  print("Database creation successfull!")
  db.commit()
  db.close()

def create_table(name, database):
  import mysql.connector as mc
  db = mc.connect(host = "localhost", user = "root", password = "dav123", database = database)
  cursor = db.cursor()
  cursor.execute("create table if not exists '{}'(name varchar(20), class int, section char, roll_no int, phone long);".format(name))
  print("Your table {} has been created !!".format(name))
  db.commit()
  db.close()

def show_all_tables(database):
  import mysql.connector as mc
  db = mc.connect(host = "localhost", user = "root", password = "dav123", database = database)
  cursor = db.cursor()
  cursor.execute("show tables;")
  print("The tables present in the database named {} are listed below".format(database))
  for i in cursor.fetchall():
    print(i)

def show_structure_table(database, name):
  import mysql.connector as mc
  db = mc.connect(host = "localhost", user = "root", password = "dav123", database = database)
  cursor = db.cursor()
  cursor.execute("desc {};".format(name))
  print("The structure of the table {} is given below".format(name))
  for i in cursor.fetchall():
    print(i)

run = 1
while run:
  main()
  prompt = int("Enter your choice:\n")
  if(prompt==1):
    show_databases()
  elif(prompt==2):
    name = input("Enter the name you want to give to the database:\n")
    create_database(name)
  elif(prompt==3):
    database = input("Enter the name of the database to work upon:\n")
    name = input("Enter the name of the table to create:\n")
    create_table(name, database)
  elif(prompt==4):
    database = input("Enter the database name to work upon:\n")
    show_all_tables(database)
  elif(prompt==5):
    database = input("Enter the database name to work upon:\n")
    name = input("Enter the name of the table to work upon:\n")
    show_structure_table(database, name)
  elif(prompt==6):
    print("Thanks for using !")
    run = 0
  else:
    print("Invalid Input!")


















    ## Exp 2

def main():
  print("\t\t\t\tMain Menu\t\t\t\t", "1.", "2.", "3.", "4.", "5.", "6.", sep="\n")

def add_records(database, name):
  import mysql.connector as mc
  db = mc.connect(host = "localhost", user = "root", password = "dav123", database = database)
  cursor = db.cursor()
  n = int(input("Enter the number of records to enter:\n"))
  for i in range(n):
    print("Entry:", i+1)
    t_name = input("Enter the name:\n")
    t_class = int(input("Enter the class:\n"))
    section = input("Enter the section (single character):\n")
    roll_no = int(input("Enter the roll number:\n"))
    phone = int(input("Enter the phone number:\n"))
    cursor.execute("insert into '{}' values('{}', {}, '{}', {}, {});".format(name, t_name, t_class, section, roll_no, phone))
  print("Table is updated with records !!")
  db.commit()
  db.close()

def display_records(database, name):
  import mysql.connector as mc
  db = mc.connect(host = "localhost", user = "root", password = "dav123", database = database)
  cursor = db.cursor()
  cursor.execute("select * from {};".format(name))
  print("Records in table {}".format(name))
  for i in cursor.fetchall():
    print(i)

run = 1
while run:
  main()
  prompt = int(input("Enter your choice:\n"))
  if(prompt==1):
    database = input("Enter the database name:\n")
    name = input("Enter the table name:\n")
    add_records(database, name)
  elif(prompt==2):
    database = input("Enter the database name:\n")
    name = input("Enter the table name:\n")
    display_records(database, name)
  elif(prompt==3):
    print("Thank you for using !!")
    run = 0
  else:
    print("Invalid Input")