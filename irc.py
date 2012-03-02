import sys
import time
from ircbot import SingleServerIRCBot
import pprint
import irclib

def on_welcome(connection, event):
    connection.join(channel)

def on_pubmsg(connection, event):
    msg = event.arguments()[0]
    nick = event.source().split('!')[0]
    logfile.write("%s [%s] %s\n" % (time.strftime("%Y/%m/%d: %H:%M:%S %Z"),
            nick, msg))


if len(sys.argv) != 6:
    print "Usage: %s server:[port] nickname channel duration logfile" % (sys.argv[0])
    print "This is a IRC bot to log message of an IRC channel for a certain duration"
    print "  server:port - IRC server and its corresponding port number"
    print "  nickname - nickname of this IRC bot on the IRC channel"
    print "  duration - duration where this daemon must continue to log the message in seconds"
    print "  logfile - name of the logfile where the messages will go to"
    sys.exit(1)

server = sys.argv[1].split(':')
port = 6667

if len(server) == 2:
    port = int(server[1])

channel = sys.argv[3]
server = server[0]
nickname = sys.argv[2]
expiry_time = time.time() + int(sys.argv[4])
logfile = open(sys.argv[5], 'w')

if not channel.startswith('#'):
    print 'channel name %s should starts with #' % (channel)
    sys.exit(1)

irc = irclib.IRC()

try:
    c = irc.server().connect(server, port, nickname)
except irclib.ServerConnectionError, x:
    logfile.write('Error connecting to server %s port %d nick %s:%s' % (server,
        port, nickname, x))
    logfile.flush()
    logfile.close()
    sys.exit(1)

c.add_global_handler("welcome", on_welcome)
c.add_global_handler("pubmsg", on_pubmsg)

while expiry_time > time.time():
    irc.process_once(expiry_time - time.time())

logfile.flush()
logfile.close()
