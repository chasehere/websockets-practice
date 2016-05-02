import optparse, os
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.task import LoopingCall
import random
 
def parse_args():
  usage = """usage: %prog [options]"""

  parser = optparse.OptionParser(usage)
  help = "The port to listen on. Default ot random available port"
  parser.add_option('--port', type='int', help=help)
  help = "The interfact to listen on.  Default is localhost."
  parser.add_option('--iface', help=help, default='localhost')

  options, args = parser.parse_args()

  return options

class DataStreamingProtocol(Protocol):
 
  def connectionMade(self):
    print "Connected to data streaming server."
    self.factory.clientConnectionMade(self)
  
  def connectionLost(self, reason):
    print "Connection lost."
    self.factory.clientConnectionLost(self)


class DataStreamingFactory(ServerFactory):
  
  protocol = DataStreamingProtocol

  def __init__(self):
    self.clients = []
    self.lc = LoopingCall(self.announce)
    self.lc.start(1)

  def announce(self):
    stream = str(random.random())[0:5] + '\n'
    for client in self.clients:
      client.transport.write(stream)

  def clientConnectionMade(self, client):
    #print "Client has connected: " + client
    self.clients.append(client)

  def clientConnectionLost(self, client):
    #print "Client has disconnected: " + client
    self.clients.remove(client)

def main():
  
  options = parse_args()
  
  factory = DataStreamingFactory()
  
  from twisted.internet import reactor

  port = reactor.listenTCP(options.port or 0, factory, interface = options.iface)

  print 'Servring data requests on %s.' % port.getHost()
 
  reactor.run()

if __name__ == '__main__':
  main()
  
