import discord
#discord.py : revolves around the events,listens and responds to events
#asynchronous library,hence works with callbacks

#the function names are specifically from the discord library,hence they cannot be given any other name!

import os


###to work with APIs:###
#to allow to make http requests to data from the API
import requests

#since data returned from the API is in JSON!
import json

import random

#for using the replit database:
from replit import db


#for webserver:
from keep_alive import keep_alive

#helper function : to return the quote from the API:
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -"+ json_data[0]['a']
  return quote

#instance of a client:
client = discord.Client()


#for encouraging quotes depending on the following words in the message:

sad_words = ['sad','depressed','unhappy','angry','miserable','depressing']

starter_encouragements = ['Cheer up!','hang in there.','You are a great person/bot!']

if "responding" not in db.keys():
  db["responding"] = True


#helper function to update the db:
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]


#helper function to delete the value in db:

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if(len(encouragements)>index):
    del encouragements[index]
    db['encouragements'] = encouragements


#Registering an event:
#event trigerred when the bot is ready!
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

#event for responding to messages:
@client.event
async def on_message(message):
  #checking if the message is from the bot itself or not!,if it is, do nothing:
  if message.author == client.user:
    return 
  
  # #if the message starts with command $hello:

  # if message.content.startswith("$hello"):
  #   await message.channel.send('Hello!')

  msg = message.content

#return random inspirational quotes:
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)
  
  #returning encouragements when typed in sad /sad like words!
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"].value 
      # options = options.append(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  #add user submitted message (new encouragement )to the database:

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  
  #to delete an encouragement:
  if msg.startswith("$del"):
    ecouragements=[]
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  #list all the encouraging messages:
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  #changing responding:
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is ON.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is OFF.")


#for running the webserver:

keep_alive()

#to run the bot:
client.run(os.environ['token'])
    


