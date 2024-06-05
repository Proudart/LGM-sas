import os
import smtplib
from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import datetime


SENDER_EMAIL = 'work.address.lgm@gmail.com'
RECEIVER_1 = 'work.address.lgm@gmail.com'
RECEIVER_MAIN = 'lgmsasdi@gmail.com'

app = Flask(__name__)

def opening_time():
    today = datetime.datetime.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    xt = current_time.split(':')
    opn_hrs1 = [n for n in range(8,12)]
    opn_hrs2 = [n for n in range(14,18)]
    opn_days = [i for i in range(5)]
    hour = int(xt[0]) + 1
    time = 'Chiuso'
    if today.weekday() in opn_days:
        if hour in opn_hrs1 or hour in opn_hrs2:
            time = 'Aperti'
        elif hour == 12 or hour == 13:
            time = 'Chiuso - riapre alle 14:00'
    return time


def send_email(sender, receiver, name, number, mail, msg, ):
        subject = f'Nuovo messaggio da {name}'
        message = f"\nNome del clienet: {name}\n\nEmail del cliente: {mail}\n\nNumero del cliente: {number}\n\nMessaggio del cliente: {msg}"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        text = f"Subject: {subject}\n\n{message}"
        load_dotenv()
        server.login(sender, os.getenv("PASSWORD"))
        server.sendmail(sender, receiver, text)

@app.route("/")
def index():
    time = opening_time()
    return render_template("index.html", time=time)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    time = opening_time()
    if request.method == "POST":
        number = request.form.get("phone")
        name = request.form.get("name")
        mail = request.form.get("email")
        msg = request.form.get("message")

        err = 'Tutti i box devono essere completati'
        success = 'Messaggio inviato!'

        if number and name and mail and msg:
            if len(number) == 10:
                num_check = [i for i in number if i.isdigit()]
                if len(num_check) == 10:
                    send_email(SENDER_EMAIL, RECEIVER_1, name, number, mail, msg)
                    send_email(SENDER_EMAIL, RECEIVER_MAIN, name, number, mail, msg)
                    time = opening_time()
                    return render_template("contact.html", sent=success, time=time)
                return render_template("contact.html", error = 'Il numero deve contenere solo cifre', time=time)
            return render_template("contact.html", error = 'Il numero deve contenere 10 cifre', time=time)
        return render_template("contact.html", error=err, time=time)
    else:
        return render_template("contact.html", time=time)
    
@app.route("/services")
def services():
    time = opening_time()
    return render_template("services.html", time=time)
