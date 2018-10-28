import smtplib
from random import shuffle
from pprint import pprint

def get_email_template():
    with open( "email.txt" ) as file:
        email = file.read()
    return email

def create_santa_lists( santas, giftees ):
    with open( "list.txt" ) as file:
        for line in file:
            santa_info = line.strip( '\n' ).split()
            giftees.append( santa_info[1] )
            santas.append( santa_info )

def send_email( santa_email, santa, giftee ):
    my_email = "myemail"
    my_password = "mypass"

    server = smtplib.SMTP( 'smtp.gmail.com', 587 )
    server.starttls()
    server.login( my_email, my_password )

    email = get_email_template()
    msg = email.format( santa, giftee )

    server.sendmail( my_email, santa_email, msg )
    server.quit()


if __name__ == "__main__":
    santas = list()
    giftees = list()
    create_santa_lists( santas, giftees )
    shuffle( giftees )
    for santas_info in santas:
        found = False
        i = 0
        while not found:
            if giftees[i] != santas_info[1]:
                # email name
                # print santas_info[0], santas_info[1], giftees[i]
                send_email( santas_info[0], santas_info[1], giftees[i] )
                del giftees[i]
                found = True
            else:
                i += 1
