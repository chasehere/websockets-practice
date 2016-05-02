import optparse, os
from twisted.internet.protocol import ClientFactory, Protocol

 
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
  
  def dataReceived(self, data):
    print 'Received: ' + data

  def connectionLost(self, reason):
    pass


class DataStreamingClientFactory(ClientFactory):

  protocol = DataStreamingProtocol

  def __init__(self):
    pass


   
