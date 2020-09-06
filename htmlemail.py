import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import requests

# me == my email address
# you == recipient's email address
me = "harrycawe@gmail.com"
you = "harrycawe@gmail.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
#text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
# html = """\
# <html>
#   <head></head>
#   <body>
#     <p>Hi!<br>
#        How are you?<br>
#        Here is the <a href="https://www.python.org">link</a> you wanted.
#     </p>
#     <img src="https://blog.mailtrap.io/wp-content/uploads/2018/11/blog-illustration-email-embedding-images.png?w=640" alt="test">
#   </body>
# </html>
# """

# html = requests.get('https://raw.githubusercontent.com/HarryCawe/Murder-Role-Randomiser/master/email-inlined.html')
html = Path('murderer2.html').read_text()

# Record the MIME types of both parts - text/plain and text/html.
#part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
#msg.attach(part1)
msg.attach(part2)

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
  smtp.ehlo() # Start the server
  smtp.starttls()  # Encryption mechanism, connect securely
  smtp.login('harrycawe@gmail.com', 'ixgoupzmdxhpxkhj')
  smtp.send_message(msg)
  print('all good boss!')