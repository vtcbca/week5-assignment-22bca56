Python 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> def create_contact_table():
    tbl="Create table IF NOT EXISTS contact(\
        fname text,\
        lname text,\
        contact integer,\
        email text,\
        city text\
        )"
    curobj.execute(tbl)
    def create_log_table():
    logtbl="create table  IF NOT EXISTS logtable1\
        (\
        fname text,\
        lname text,\
        contact integer,\
        datetime text,\
        operation text\
        );"
    curobj.execute(logtbl)
def contact_validate_trigger():
    con_validate_trigger="create trigger IF NOT EXISTS contact_validate\
                        before insert\
                        on contact\
                        begin\
                        select\
                                case \
                                when length(new.contact)>10 then\
                                raise(abort,'Given number is greater than 10 digit . Please enter 10 digit number')\
                                when length(new.contact)<10 then\
                                raise(abort,'Given number is less than 10 digit . Please enter 10 digit number')\
                        end;\
                        end;"

    curobj.execute(con_validate_trigger)

def log_table_trigger():
    log_tbl_insert_trigger="create trigger IF NOT EXISTS insert_trigger\
                        after insert \
                        on contact\
                        begin\
                            insert into logtable\
                            values(new.fname,new.lname,new.contact,datetime('now','localtime'),'INSERT');\
                        end;"

    curobj.execute(log_tbl_insert_trigger)


    log_table_delete_trigger="create trigger IF NOT EXISTS delete_trigger\
                                after delete \
                                on contact\
                                begin\
                                insert into logtable\
                                values(old.fname,old.lname,old.contact,datetime('now','localtime'),'DELETE');\
                                end;"

    curobj.execute(log_table_delete_trigger)


    log_table_update_trigger="create trigger IF NOT EXISTS update_trigger\
                                after update\
                                on contact\
                                begin\
                                insert into logtable\
                                values(new.fname,new.lname,new.contact,datetime('now','localtime'),'UPDATE(After)');\
                                insert into logtable\
                                values(old.fname,old.lname,old.contact,datetime('now','localtime'),'UPDATE(Before)');\
                                end;"

    curobj.execute(log_table_update_trigger)

def menu():
    print('Enter 1 For Insert Contact No')
    print('Enter 2 For Delete Contact No')
    print('Enter 3 For Update Contact No')
    print('Enter 4 For Search Contact No')
    print('Enter 0 For Quit')

def insert_contact():
    try:
            query = "insert into contact \
                    values(?,?,?,?,?)"
            
            First_Name=input('Enter First Name :')
            Last_Name=input('Enter Last Name :')
            Contact = int(input('Enter Contact No :'))
            Email=input('Enter Email ID :')
            City=input('Enter City :')
            main_list=[First_Name,Last_Name,Contact,Email,City]
            curobj.execute(query,main_list)
            print()
            print("Record Insert Successfully")
            print()
    except Error as e:
            print()
            print(e)
            print()

def delete_contact():
    try:
            Name = input('Enter Contact First Name You Want To Delete : ')
            query = f"delete from contact\
                        where fname='{Name}'"
            curobj.execute(query,main_list)
            print()
            print("Record Delete Successfully")
            print()
    except Error as e:
            print()
            print(e)
            print()

def update_contact():
    try:
            print('\nFirst Name\tLast Name\tContact No',end="\n")
            col_name=input("Enter Your Choice Which Thing You Want To Update :").lower()
            
            print(col_name)
            if col_name=='first name':
                old_fname=input("Enter Old First Name :")
                new_fname=input("Enter New First Name :")
                query =f"""update contact
                                    set fname='{new_fname}'
                                    where fname='{old_fname}' """
            elif col_name=='last name':
                old_lname=input("Enter Old Last Name :")
                new_lname=input("Enter New Last Name :")
                query =f"""update contact
                                    set fname='{new_lname}'
                                    where fname='{old_lname}'  """
            elif col_name=='contact no':
                old_contact=input("Enter Old Contact No :")
                new_conatct=input("Enter New Contact No :")
                query =f"""update contact
                                    set fname='{new_contact}'
                                    where fname='{old_contact}' """
            curobj.execute(query)
            print()
            print("Record Update Successfully")
            print()
    except Error as e:
            print()
            print(e)
            print()

def search_contact():
    try:
                curobj.execute('select fname , lname from contact')
                All_Record = curobj.fetchall()
                print('First Name\tLast Name')
                for i in All_Record:
                    print(f'{i[0]}\t\t{i[1]}')
    except Error as e:
                print(e)
                    
    try:
                Name = input('Enter Name : ')
                curobj.execute(f'''select fname , lname , contact from contact
                                                where fname = '{Name}' ''')
                Contact_No =curobj.fetchall()
                print()
                print("-------------------------------------------------------------------",end='\n')
                print('First Name\tLast Name\tContact No')
                print("-------------------------------------------------------------------",end='\n')
                for i in Contact_No:
                     print(f'{i[0]}\t\t{i[1]}\t\t{i[2]}')
                print()
    except Error as e:
                print(e)


#MAIN PROGRAM 
from sqlite3 import *

conn=connect('c:\\sqlite\\week4.db')

curobj = conn.cursor()
create_contact_table()
create_log_table()
contact_validate_trigger()
log_table_trigger()
main_list=[]
choice=1

while choice!=0:
    menu()
    choice=int(input('Enter Your Choice : '))
    if choice==1:
        insert_contact()
    if choice==2:
        delete_contact()
    if choice==3:
        update_contact()
    if choice==4:
            search_contact()

conn.commit()

conn.close()