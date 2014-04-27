import socket
import sys
import time
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

def GetMessage(text):
   privMsgIndex = text.find('PRIVMSG')
   msg = ""
   if privMsgIndex != -1:
      msgAfterPriv = text[privMsgIndex:]
      colonIndex = msgAfterPriv.find(':')

      if colonIndex != -1:
         msg = msgAfterPriv[colonIndex + 1:]

   return msg

def StripMsg(text):
   if text[0] == "!":
      return text[1:]
   else:
      return text

while 1:    #puts it in a loop
   text=irc.recv(2040)  #receive the text
   print (text)   #print text to console

   if text.find('PING') != -1:                          #check if 'PING' is found
      irc.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
      continue
   	
   msg = GetMessage(text)
   data.Test()
   print("Got message: " + msg)

   if msg.find("!") != -1:
      msg = StripMsg(msg)
      print("Stripped msg: " + msg)
      if msg != "":
         if data.IsChamp(msg):
            print("Voting for champ: " + msg)
            data.VoteChamp(msg.rstrip())
         if msg.find("showvotes") != -1:
            print("Showing votes")
            votes = data.GetVotes()
            if not votes:
               printstring = "No votes at this time!"
            else:
               for vote in votes:
                  print(repr(vote))
                  irc.send("PRIVMSG " + channel + " :" + vote + "\n")
         if msg.find("test") != -1:
            print("testing")
            irc.send("PRIVMSG " + channel + " :test\n")

            
