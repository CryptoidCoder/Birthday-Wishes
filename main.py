# Import Modules & Initiate Using .env file
from dotenv import load_dotenv
import os
load_dotenv()


from functions import * # import functions file

import datetime #import dates
import schedule, time # for scheduling

token = os.getenv('notion_token')
databaseId = os.getenv('Birthday-databaseId')

def main(): #main functions for checking for birthdays
    readDatabase(databaseId) #read from database & save to file
    data = json.load(open("db_read.json")) #read file
    os.remove("db_read.json") #delete file
    for row in data['results']: #for people in table
        FirstName = getdata(row, ["properties", "First Name", "title", "text", "content"]) #get first  name from title-type column
        SecondName = getdata(row, ["properties", "Second Name", "rich_text", "text", "content"]) #get second name from rich_text type column
        Name = f"{FirstName} {SecondName}" #combine First & Last name 
        Birthday =  getdata(row, ["properties", "Birthday", "date", "start"]) #get birthday from date-type column
        Message = getdata(row, ["properties", "Message", "rich_text", "text", "content"]) #get message from rich_text type column
        phonenumber = getdata(row, ["properties", "Phone Number", "rich_text", "text", "content"]) #get phone number from rich_text type column

        Birthday = Birthday.split("-") #split into a list
        Birth_Year, Birth_Month, Birth_Day = int(Birthday[0]),int(Birthday[1]),int(Birthday[2]) #first itme is year, second item is month, third item is day

        Birthday = datetime.datetime(Birth_Year, Birth_Month, Birth_Day).date()

        Today = datetime.datetime.now().date()

        if Today == Birthday:
            print(f"{Name}'s Birthday Is Today!")
            if Message != None: #if message exists include it, else don'use generic
                print(f"Here is the message: {Message}")
            else: #use generic message
                Message = f"Happy Birthday {Name}, Hope You Have A Great Day"

            sendmessage(phonenumber, Message)



if __name__ == '__main__':
    schedule.every().day.at("06:00").do(main) #every day at 6 AM check if it's anyone's birthday
    while True:
        schedule.run_pending()#run pending scheduled tasks
        time.sleep(1) #sleep for 1 second
