from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
  return "Hello.I am alive!!"

def run():
  app.run(host = '0.0.0.0',port=5000)

def keep_alive():
  t = Thread(target = run)
  t.start()


#SERVER WILL RUN ON A SEPERATE THREAD FROM THE BOT ,hence both will run simultaneously!