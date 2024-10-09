import smtplib
from flask import Flask, render_template, request, redirect, url_for
import random
import time as pytime
from datetime import datetime

main = smtplib.SMTP_SSL('smtp.gmail.com')
sender = 'projectptg4@gmail.com'
password = 'mmkk vnpv hjri isyk'
main.login(sender, password)

mail = ''
name = ''
mMail = ''
eMsg = ''
rMail = ''
diff = ''
# ____________________________Mail Management________________________________

def OTPSend(mail, name, holder):
    msg = f"""HI {name},\nThis is from the team of Project PTG, Your OTP is given below\n{holder}\nDont share this otp unless you trust the Asker"""
    main.sendmail(sender, mail, msg)
    print("Successfully done")
    
    return render_template("otpCon.html")
    # main.quit()

def MailSend(mail,msg):
    main.sendmail(sender, mail, msg)
    return redirect(url_for('rHome'))
# ____________________________OTP Generator__________________________________
val = ''
def OTPGen():
    global val
    temp  = ''
    for i in range(6):
        temp += str(random.randrange(0,9))
    val = temp


# ____________________________Flask Management________________________________
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    global mail
    global name
    mail = request.form.get("mail")
    name = request.form.get("name")
    print(mail)
    OTPGen()
    OTPSend(mail, name, val)
    return render_template('otpCon.html')

@app.route('/realHome')
def rHome():
    return render_template("realHome.html")

@app.route('/verify-otp', methods=['POST', 'GET'])
def otpverify():
    otp = request.form.get('otp')
    if otp == val:
        return render_template("realHome.html")
    return render_template('otpCon.html')

@app.route('/message',methods = ['POST', 'GET'])
def message():
    global mMail, eMsg, rMail, diff
    rMail = request.form.get("toMail")
    Msg = request.form.get("message")
    time = request.form.get("time")
    date = request.form.get("date")
    
    current = datetime.now()
    datetime_str = f"{date} {time}"
    sched = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    diff = (sched - current).total_seconds()
    if diff < 0:
        return "no"
    
    mMail = mail.split('@')[0]
    eMsg = f"""
Hello,

This message is sent from the Project PTG on behalf of {name}, who wanted to express something important to you.

Unfortunately, {name} feels a bit hesitant or lacks the confidence to share this directly, so they asked us to help convey the message below:

---

{Msg}

---

Please understand that this message is sent with sincerity, and {name} truly values your response.

Best regards,  
Project PTG
"""
    
    print(rMail, eMsg)
    return render_template("preview.html",msg = eMsg)

@app.route('/confirm', methods = ['POST', 'GET'])
def preview():
    pytime.sleep(diff)
    main.sendmail(sender, rMail,eMsg)
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    app.run(debug=True)