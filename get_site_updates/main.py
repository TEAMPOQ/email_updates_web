import requests, ssl, smtplib, getpass, time
from email.message import EmailMessage

#smtp port
port = 587

# get website from user
#url = "https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=9200190313867800478305"
#url = "https://www.clocktab.com/"
url = "http://tracking.modafinilxl.com/tracking/click?d=yx9XZPur-k1bEo1Uvx7mH-IccO5lWyWnYuhDz2BsUpRHsH50PxThoslSjAhwIZvfoz5Tecgh7_wfFDvQDCkPiks7rC5yzCeWNqTL6SdbJ580_corH3LeapZ0x2M9_NBXcbJMA2tstseIjNldWfqAy1xsI0_7T0d_uqZy9hKlN71xqfSAYd38a1sicTB29v6kTA2"

# get user email and pass to signin
email = input("Enter your email > ")
password = getpass.getpass(prompt='Enter your password > ')
data = "test"
list_of_data = []
msg = ""

#initial url grab
old_data = requests.get(url).text

#save data to a text file (a.k.a database)
file = open("data.txt", "w", encoding="utf-8")
file.write(old_data)
file.close()


def sendmsg(strMsg):
     msg = EmailMessage()
     msg.set_content(strMsg)
     msg["Subject"] = "An Email Alert"
     msg["From"] = "pythonscriptmessageupdate@hotmail.com"
     msg["To"] = "pythonscriptmessageupdate@hotmail.com"

     # Create a secure SSL context
     context = ssl.create_default_context()
     with smtplib.SMTP("smtp.office365.com", port) as server:
          server.starttls()
          server.login(email, password)
          server.sendmail('pythonscriptmessageupdate@hotmail.com', 'pythonscriptmessageupdate@hotmail.com', msg.as_string())
          print("Successfully sent email")



while True:
     # get updated data
     data = requests.get(url).text

     # check if new data is the same
     if old_data is not data:
     # will be used for sending if an update occurs
          wanted_data = data[data.find('content_panel tracking-details tracking_events_details'):data.find(
               'product_details" class="heading_panel')]

          while wanted_data.find("<strong>") != -1:
               msg += (wanted_data[wanted_data.find('<strong>') + 8:wanted_data.find('</strong>')]) + " --- "
               msg += (wanted_data[wanted_data.find('<p>') + 3:wanted_data.find('</p>')]) + " --- "
               wanted_data = wanted_data[wanted_data.find('</p>') + 3:]


          sendmsg(msg)

          # save updated data to a text file (a.k.a database)
          file = open("data.txt", "w", encoding="utf-8")
          file.write(data)
          file.close()

     # Timeout the program to check every 5 minutes
     time.sleep(500)
