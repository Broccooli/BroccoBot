import socket
import sys
import time
import util
from other import ChampData

server = "irc.twitch.tv"       #settings
channel = "#broccoliyumyum"
botnick = "BroccoBot"
password = "oauth:gdlag64kj38mtax9kk8e0e3glzhhpyi"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print ("connecting to:"+server)
irc.connect((server, 6667))#connects to the server
irc.send("PASS " + password + "\n")
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
irc.send("NICK "+ botnick +"\n")                            #sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n")    #auth
irc.send("JOIN "+ channel +"\n")        #join the chan

#Champ Stuff
champfile = open("./champlist.brocc")
data = ChampData(champfile)

def SendMessage(channel, msg):
   irc.send("PRIVMSG " + channel + " :" + msg + "\n")
   
def GetMessageAndUser(text):
   endPriv = text.find('PRIVMSG') + len('PRIVMSG') + 1
   userAndMessage = text[endPriv:] # Strips unnecessary text, leaving only the text that contains user and message
   pound = userAndMessage.find('#')
   colon = userAndMessage.find(':')
   user = userAndMessage[pound + 1: colon - 1] #finds user
   userMessage = userAndMessage[colon + 1:] #finds message
   return [user, userMessage] #return the two   

def ValidateCommand(text):
   text = text[1:]
   colon = text.find(":")
   if (colon == -1):
      return util.ValidCommand(text)
   else:
      return util.ValidCommand(text[:colon])

while 1:    #puts it in a loop
   text=irc.recv(2040)  #receive the text
   print (text)   #print text to console

   if text.find('PING') != -1:                          #check if 'PING' is found
      irc.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
      continue
   	
   msgUser = GetMessageAndUser(text)
   user = msgUser[0]
   userMessage = msgUser[1]

   if userMessage.find("!") == 0:
      if (ValidateCommand(userMessage)):   # Returns true if valid command
         if (userMessage.find("!vote") != -1):
            champToVote = userMessage[userMessage.find(":") + 1:]
            if data.IsChamp(champToVote): # Get the champ the user is voting for
               print("Voting for champ: " + champToVote)
               data.VoteChamp(champToVote.rstrip())
         elif userMessage.find("!showvotes") != -1:
            print("Showing votes")
            votes = data.GetVotes()
            if not votes:
               printstring = "No votes at this time! /r/n"
               SendMessage(channel, printstring)
            else:
               for vote in votes:
                  SendMessage(channel, vote)
         elif userMessage.find("!winning") != -1:
            winner = data.GetWinner()
            printstring = "The winner is " + winner[0] + " with " + str(winner[1]) + " votes"
            SendMessage(channel, printstring)
         elif userMessage.find("!top3") != -1:
            top3 = data.GetTop(3)
            i = 1
            for champ in top3:
               printstring = str(i) + ": " + champ[0] + " with " + str(champ[1]) + " votes"
               SendMessage(channel, printstring)
               i = i + 1
            

            
