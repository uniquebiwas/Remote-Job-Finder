import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('remotejob007@gmail.com', 'onky iwgz ibip oyho')
    print("SMTP Connection Successful111")
except Exception as e:
    print("SMTP Connection Failed:", str(e))
finally:
    server.quit()
