import zmq
import time

from machinetalk.protobuf.message_pb2 import Container
from machinetalk.protobuf.types_pb2 import MT_PING

from zeroconf import ServiceBrowser, Zeroconf

IDENTITY = 'batman'
PING = Container()
PING.type = MT_PING

class MyListener(object): 
    commandUri=''
    
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        # print "service added"
        info = zeroconf.get_service_info(type, name)
        # print name, info.get_name(), info.server,
        # print name, info
        if 'Command service' in info.get_name() :
            self.commandUri = "tcp://" + info.server + ":" + str(info.port)
        
def send_ping(port, uri):
    global ping
    global IDENTITY

    context = zmq.Context()
    dealer = context.socket(zmq.DEALER)
    dealer.identity = IDENTITY
    #hostname = 'tcp://machinekit.local:49155'
    hostname = uri
    dealer.connect(hostname)
    dealer.send(PING.SerializeToString())

def test_send_ping():
    zeroconf = Zeroconf()  
    listener = MyListener()  
    ServiceBrowser(zeroconf, "_machinekit._tcp.local.", listener) 	
    
    while listener.commandUri == '' :
        print "waiting for command uri"
        time.sleep(2)
	
    print "Found command uri at: " + listener.commandUri
    
    context = zmq.Context()
    dealer = context.socket(zmq.DEALER)
    port = dealer.bind_to_random_port('tcp://127.0.0.1')
    # port = 6202
    send_ping(port, listener.commandUri)
    buf = dealer.recv()
    msg = Container()
    msg.ParseFromString(buf)
    assert msg == PING

if __name__ == '__main__':
    test_send_ping()
    




