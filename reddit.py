# importing both the schedule and time library in order schedule the time for my script to run
import schedule
import time
# package that will enable my program to with the Reddit application
import praw

# package that will enable me to send email to any internet machine with SMTP or ESMTP listener deamon
import smtplib

# Importing only email.message from EmailMessage
from email.message import EmailMessage

# Imprting pandas to gather the subreddit data

# Importing the database i will use to save my reddit data
import sqlite3

conn = sqlite3.connect('reddit.db')
c = conn.cursor()
c.execute(''' CREATE TABLE IF NOT EXISTS  redditData(title TEXT, upvotes INT, url TEXT, numberOfComments)''')

def databaseConnection(title, upvotes, url, numComments):
    '''
    creating connection to the database
    '''
    c.execute('''INSERT INTO  redditData VALUES(?, ?,?,?)''', (title, upvotes, url, numComments))
    conn.commit()

    c.execute(''' SELECT * FROM redditData''')
    result = c.fetchall()
    print(result)


def email_alert(to, subject, body):
    """ using the Email message package
        to create a message that takes the
        to, subject, and body arguments

        Args: 
            to, subject, body
        Returns:
            none
    """
    # Creating message object
    myMessage = EmailMessage()
    # Set message content to body
    myMessage.set_content(body)
    # Set message subject property to subject
    myMessage['subject'] = subject
    # Set message to property to to
    myMessage['to'] = to

    # information needed for email authentication
    user = "pythonlearning78@gmail.com"
    password = "bcbtvfsrvvelqxdv"

    # Set message from property to user
    myMessage['from'] = user

    # Use the SMTP package to create a session to send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # uses the arguments user and password to gain access to the server
    server.login(user, password)

    # Send the message
    server.send_message(myMessage)

    # print this line of code on the terminal everytime a message is sent
    print("The message was successfully sent")

    # Exit the session
    server.quit()


def getting_popular_reddits():
    """
    Using the praw package to interact with reddit
    Argument: No argument
    Return: None

    """
    # Creating an instance of the reddit class
    # Using client_id and Client_secret to log in to my reddit account
    reddit = praw.Reddit(client_id='KdKf0wIRtXkTWsk3GF4ynQ',
                         client_secret='_oA9OnRUnvFffil763N-92oZZFGIqQ', user_agent='redBot')

    # limit the numbers of post i see to only the top 10 in the rutgers subreddit
    subRed = reddit.subreddit('rutgers').hot(limit=30)

    # creating empty list to store my data
    popular_reddit = []

    # iterate over the rutgers subreddit
    for thread in subRed:
        # if the post is not permanently display at the top of the subreddit
        if not thread.stickied:
            # and if it has more than 10 upvote append it to the popular_reddit array and the pandas dataframe
            if(thread.score > 10):
                popular_reddit.append(thread.url)
                databaseConnection(thread.title, thread.score, thread.url, thread.num_comments)

    # Use the email alert function
    # Send each popular post one by one so it is clickable on my mobile device

    email_alert("6096656286@tmomail.net", "today's popular reddit discussion", f"here is the first url: {popular_reddit[0]}")
    email_alert("6096656286@tmomail.net", "today's popular reddit discussion", f"here is the second url: {popular_reddit[1]}")
    email_alert("6096656286@tmomail.net", "today's popular reddit discussion", f"here is the third url: {popular_reddit[2]}")


# everyday at 10:30 am send me the top three most popular post on the rutgers subreddit

schedule.every().day.at("10:00").do(getting_popular_reddits)

while 1:
    schedule.run_pending()
    time.sleep(1)
