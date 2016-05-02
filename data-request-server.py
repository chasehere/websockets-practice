import optparse, os, time, random
from twisted.internet.protocol import ServerFactory, Protocol

 
def parse_args():
  usage = """usage: %prog [options]"""

  parser = optparse.OptionParser(usage)
  help = "The port to listen on. Default ot random available port"
  parser.add_option('--port', type='int', help=help)
  help = "The interfact to listen on.  Default is localhost."
  parser.add_option('--iface', help=help, default='localhost')

  options, args = parser.parse_args()

  return options

class DataRequestService(object):

  def getData(self):
    print 'Getting data...'
    time.sleep(7)
    return str(random.random())[0:5]

class DataRequestProtocol(Protocol):
 
  def connectionMade(self):
    print "Connecton made to data request server from", self.transport.getPeer()
    self.dataReceived('sample')
 
  def dataReceived(self, data):
    ''' This shows the request for a second user is not completed until the first request has been fulfilled.  The server blocks on the reactor. '''
    start = time.time()
    print 'Received request: ' + data
    output = self.factory.getData()
    end = time.time() - start
    print 'Request completed for %s in %.3f.' % (self.transport.getPeer(),end)
    self.transport.write( output )

  def connectionLost(self, reason):
    print "Connection lost with", self.transport.getPeer() 

class DataRequestFactory(ServerFactory):
  
  protocol = DataRequestProtocol

  def __init__(self, service):
    self.service = service   

  def getData(self):
    return self.service.getData() 

def main():
  
  options = parse_args()

  service = DataRequestService()  
  factory = DataRequestFactory(service)
  
  from twisted.internet import reactor

  port = reactor.listenTCP(options.port or 0, factory, interface = options.iface)

  print 'Servring data requests on %s.' % port.getHost()
 
  reactor.run()

if __name__ == '__main__':
  main()
  
