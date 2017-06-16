import time
import zmq

from machinetalk.protobuf.message_pb2 import Container
from machinetalk.protobuf.types_pb2 import MT_PING
from machinetalk.protobuf.types_pb2 import MT_HALRCOMP_BIND 


from zeroconf import ServiceBrowser, Zeroconf

IDENTITY = 'batman'
myContainer = Container()
myContainer.type = MT_HALRCOMP_BIND 

class MyListener(object): 
    commandUri=''
    
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        # print "service added"
        info = zeroconf.get_service_info(type, name)
        # print name, info.get_name(), info.server,
        print(name, info)
        print("---")
        if 'HAL Rcommand service' in info.get_name() :
            self.commandUri = "tcp://" + info.server + ":" + str(info.port)
        
def send(port, uri):
    global ping
    global IDENTITY

    context = zmq.Context()
    dealer = context.socket(zmq.DEALER)
    dealer.identity = IDENTITY
    #hostname = 'tcp://machinekit.local:49155'
    hostname = uri
    print("connecting")
    dealer.connect(hostname)
    print("connected")
    #dealer.send(PING.SerializeToString())

    hex_string1 = "088002A206DB060A056D79696E69820116080112106D79696E692E7468632D656E61626C652020820118080212126D79696E692E61637475616C2D766F6C7473201082011B080212156D79696E692E766F6C74732D7265717565737465642020820116080112106D79696E692E76656C2D73746174757320108201130802120D6D79696E692E76656C2D746F6C2020820118080212126D79696E692E7363616C652D6F666673657420208201150802120F6D79696E692E76656C2D7363616C652020820117080212116D79696E692E766F6C746167652D746F6C202082011A080212146D79696E692E636F7272656374696F6E2D76656C2020820117080112116D79696E692E746F7263682D70726F626520108201150802120F6D79696E692E7468632D7A2D706F732010820118080212126D79696E692E6F66667365742D76616C756520108201140802120E6D79696E692E6D617876656C5F3320208201140802120E6D79696E692E6D61786163635F33202082011C080212166D79696E692E7374657067656E5F6D617876656C5F33202082011C080212166D79696E692E7374657067656E5F6D61786163635F3320208201140802120E6D79696E692E6D617876656C5F3420208201140802120E6D79696E692E6D61786163635F34202082011C080212166D79696E692E7374657067656E5F6D617876656C5F34202082011C080212166D79696E692E7374657067656E5F6D61786163635F3420208201140802120E6D79696E692E6D617876656C5F3020208201140802120E6D79696E692E6D61786163635F30202082011C080212166D79696E692E7374657067656E5F6D617876656C5F30202082011C080212166D79696E692E7374657067656E5F6D61786163635F3020208201140802120E6D79696E692E6D617876656C5F3120208201140802120E6D79696E692E6D61786163635F31202082011C080212166D79696E692E7374657067656E5F6D617876656C5F31202082011C080212166D79696E692E7374657067656E5F6D61786163635F3120208201140802120E6D79696E692E6D617876656C5F3220208201140802120E6D79696E692E6D61786163635F32202082011C080212166D79696E692E7374657067656E5F6D617876656C5F32202082011C080212166D79696E692E7374657067656E5F6D61786163635F322020"    
    hex_string = "088002A206DB060A056D79696E69820116080112106D79696E692E7468632D656E61626C652020820118080212126D79696E692E61637475616C2D766F6C7473201082011B080212156D79696E692E766F6C74732D7265717565737465642020820116080112106D79696E692E76656C2D73746174757320108201130802120D6D79696E692E76656C2D746F6C2020820118080212126D79696E692E7363616C652D6F666673657420208201150802120F6D79696E692E76656C2D7363616C652020820117080212116D79696E692E766F6C746167652D746F6C202082011A080212146D79696E692E636F7272656374696F6E2D76656C2020820117080112116D79696E692E746F7263682D70726F626520108201150802120F6D79696E692E7468632D7A2D706F732010820118080212126D79696E692E6F66667365742D76616C756520108201140802120E6D79696E692E6D617876656C5F3320208201140802120E6D79696E692E6D61786163635F33202082011C080212166D79696E692E7374657067656E5F6D617876656C5F33202082011C080212166D79696E692E7374657067656E5F6D61786163635F3320208201140802120E6D79696E692E6D617876656C5F3420208201140802120E6D79696E692E6D61786163635F34202082011C080212166D79696E692E7374657067656E5F6D617876656C5F34202082011C080212166D79696E692E7374657067656E5F6D61786163635F3420208201140802120E6D79696E692E6D617876656C5F3020208201140802120E6D79696E692E6D61786163635F30202082011C080212166D79696E692E7374657067656E5F6D617876656C5F30202082011C080212166D79696E692E7374657067656E5F6D61786163635F3020208201140802120E6D79696E692E6D617876656C5F3120208201140802120E6D79696E692E6D61786163635F31202082011C080212166D79696E692E7374657067656E5F6D617876656C5F31202082011C080212166D79696E692E7374657067656E5F6D61786163635F3120208201140802120E6D79696E692E6D617876656C5F3220208201140802120E6D79696E692E6D61786163635F32202082011C080212166D79696E692E7374657067656E5F6D617876656C5F32202082011C080212166D79696E692E7374657067656E5F6D61786163635F322020A206FB010A086D796D6F74696F6E8201110802120B6D796D6F74696F6E2E767820108201120802120C6D796D6F74696F6E2E64767820108201110802120B6D796D6F74696F6E2E767920108201110802120B6D796D6F74696F6E2E767A20108201120802120C6D796D6F74696F6E2E64767A201082011D080212176D796D6F74696F6E2E63757272656E742D72616469757320108201100802120A6D796D6F74696F6E2E76201082011B080212156D796D6F74696F6E2E6C6173657248656967687431201082011B080312156D796D6F74696F6E2E70726F6772616D2D6C696E652010820119080112136D796D6F74696F6E2E7370696E646C652D6F6E2010"
    myContainer.ParseFromString(hex_string.decode("hex"))
    
    dealer.send(myContainer.SerializeToString())

def test_send_ping():
    print("send ping 1")
    zeroconf = Zeroconf()  
    print("send ping 2")
    listener = MyListener()  
    ServiceBrowser(zeroconf, "_machinekit._tcp.local.", listener) 	
    
    while listener.commandUri == '' :
        print("waiting for command uri")
        time.sleep(2)
	
    print("Found command uri at: " + listener.commandUri)
    
    context = zmq.Context()
    dealer = context.socket(zmq.DEALER)
    port = dealer.bind_to_random_port('tcp://127.0.0.1')
    # port = 6202
    print("send ping")
    send(port, listener.commandUri)
    print ("receive")
    buf = dealer.recv()
    print ("parsing...")
    msg = Container()
    msg.ParseFromString(buf)
    print ("parsing...1")
    assert msg == PING

if __name__ == '__main__':
    test_send_ping()
