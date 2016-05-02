import optparse, os, time, random

from twisted.internet.defer import Deferred, succeed
from twisted.internet.protocol import ClientFactory, ServerFactory, Protocol

 
def parse_args():
  usage = """usage: %prog [options]"""

  parser = optparse.OptionParser(usage)
  help = "The port to listen on. Default ot random available port"
  parser.add_option('--port', type='int', help=help)
  help = "The interfact to listen on.  Default is localhost."
  parser.add_option('--iface', help=help, default='localhost')

  options, args = parser.parse_args()

  if len(args) != 1:
    parser.error('Provide exactly one server address.')

  def parse_address(addr):
    if ':' not in addr:
       host = '127.0.0.1'
       port = addr
    else:
      host, port = addr.split(':', 1)

    if not port.isdigit():
      parser.error('Ports must be integers.')

    return host, int(port)

  return options, parse_address(args[0])
  

class DataProxyProtocol(Protocol):

  def connectionMade(self):
    print 'Connection made with proxy server.'
    d = self.factory.service.get_data()
    d.addCallback(self.transport.write)
    d.addBoth(lambda r: self.transport.loseConnection())

  def dataReceived(self, data):
    # this where historical data should be fired
    print 'The proxy server has received some data: ' + data
 
class DataProxyFactory(ServerFactory):
  
  protocol = DataProxyProtocol

  def __init__(self, service):
    self.service = service


class DataClientProtocol(Protocol):
    #historical_data = ''
  
  def dataReceived(self,data):
    #self.historical_data += data
    self.factory.data_received(data)
  
  def connectionLost(self, reason):
    print 'Data Proxy Client has lost connection.'

class DataClientFactory(ClientFactory):

  protocol = DataClientProtocol

  def __init__(self):
    self.deferred = Deferred()

  def data_received(self, data):
    if self.deferred is not None:
      d, self.deferred = self.deferred, None
      d.callback(data)

  def clientConnectionFailed(self, connector, reason):
    if self.derred is not None:
      d, self.deferred = self.deferred, None
      d.errback(reason)

class ProxyService(object):

  data = None

  def __init__(self, host, port):
    self.host = host
    self.port = port

  def get_data(self):
    print 'Fetching data from server.'
    factory = DataClientFactory()
    #factory.deferred.addCallback(self.set_data) 
    from twisted.internet import reactor
    reactor.connectTCP(self.host, self.port, factory)
    return factory.deferred


def main():

  options, server_addr = parse_args()

  service = ProxyService(*server_addr)

  factory = DataProxyFactory(service)

  from twisted.internet import reactor

  port = reactor.listenTCP(options.port or 0, factory, interface=options.iface)

  print 'Proxying %s on %s.' % (server_addr, port.getHost())

  reactor.run()

if __name__ == '__main__':
  main()

