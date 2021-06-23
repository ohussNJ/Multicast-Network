from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import Link
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from cleanup import cleanup

class topo1( Mininet ):
    def __init__(self):
        Mininet.__init__(self, link=TCLink, controller=None, cleanup=True)

        info( "Creating nodes\n" )

        r1 = self.addHost( 'r1' , ip='192.168.1.2/24', inNamespace=False )
        r2 = self.addHost( 'r2' , ip='192.168.2.3/24', inNamespace=False )
        r3 = self.addHost( 'r3' , ip='192.168.1.4/24', inNamespace=False )
        r4 = self.addHost( 'r4' , ip='192.168.1.5/24', inNamespace=False )
        r5 = self.addHost( 'r5' , ip='192.168.5.3/24', inNamespace=False )
        r6 = self.addHost( 'r6' , ip='192.168.3.3/24', inNamespace=False )
        r7 = self.addHost( 'r7' , ip='192.168.4.3/24', inNamespace=False )

        h1 = self.addHost( 'h1' , ip='192.168.1.1/24', defaultRoute= 'via 192.168.1.2', inNamespace=False)
        h2 = self.addHost( 'h2' , ip='192.168.2.1/24', defaultRoute= 'via 192.168.2.2', inNamespace=False)
        h3 = self.addHost( 'h3' , ip='192.168.3.1/24', defaultRoute= 'via 192.168.3.2', inNamespace=False)
        h4 = self.addHost( 'h4' , ip='192.168.4.1/24', defaultRoute= 'via 192.168.4.2', inNamespace=False)
        #Establishing the links from hosts to routers
        info( "Creating links\n" )
        self.addLink( r1, r2, intfName1='r1-eth1', intfName2='r2-eth1')
        self.addLink( r1, r3, intfName1='r1-eth2', intfName2='r3-eth1')
        self.addLink( r3, r4, intfName1='r3-eth2', intfName2='r4-eth1')
        self.addLink( r2, r6, intfName1='r2-eth2', intfName2='r6-eth1')
        self.addLink( r3, r5, intfName1='r3-eth3', intfName2='r5-eth1')
        self.addLink( r6, r7, intfName1='r6-eth2', intfName2='r7-eth1')

        self.addLink( h1, r1, intfName2='r1-eth3', params2={'ip' : '192.168.1.2/24'})
        self.addLink( h2, r7, intfName2='r7-eth2', params2={'ip' : '192.168.2.2/24'})
        self.addLink( h3, r4, intfName2='r4-eth2', params2={'ip' : '192.168.3.2/24'})
        self.addLink( h4, r5, intfName2='r5-eth2', params2={'ip' : '192.168.4.2/24'})

        #create interfaces
        router1 = self.get('r1')
        router2 = self.get('r2')
        router3 = self.get('r3')
        router4 = self.get('r4')
        router5 = self.get('r5')
        router6 = self.get('r6')
        router7 = self.get('r7')
        #host1 = self.get('h1')
        #host2 = self.get('h2')
        #host3 = self.get('h3')
        #host4 = self.get('h4')

        #host1.setIP('192.168.1.1/24', intf='h1-eth0')
        #host2.setIP('192.168.2.1/24', intf='h2-eth0')
        #host3.setIP('192.168.3.1/24', intf='h3-eth0')
        #host4.setIP('192.168.3.1/24', intf='h3-eth0')
        #router1.setIP('192.168.1.2/24', intf='r1-eth0')
        router1.setIP('10.0.1.0/24', intf='r1-eth1')
        router1.setIP('10.0.1.1/24', intf='r1-eth2')
        router2.setIP('10.0.2.1/24', intf='r2-eth1')
        router2.setIP('10.0.2.2/24', intf='r2-eth2')
        router3.setIP('10.0.3.1/24', intf='r3-eth1')
        router3.setIP('10.0.3.2/24', intf='r3-eth2')
        router3.setIP('10.0.3.3/24', intf='r3-eth3')
        router4.setIP('10.0.4.1/24', intf='r4-eth1')
        #router4.setIP('10.0.4.2/24', intf='r4-eth2')
        router5.setIP('10.0.5.1/24', intf='r5-eth1')
        #router5.setIP('10.0.5.2/24', intf='r5-eth2')
        router6.setIP('10.0.6.1/24', intf='r6-eth1')
        router6.setIP('10.0.6.2/24', intf='r6-eth2')
        router7.setIP('10.0.7.1/24', intf='r7-eth1')
        #router7.setIP('10.0.7.2/24', intf='r7-eth2')


        #Build the specified network
        info("Building network\n")
        r1.cmd( 'sysctl net.ipv4.ip_forward=1' )
        r2.cmd( 'sysctl net.ipv4.ip_forward=1' )
        r3.cmd( 'sysctl net.ipv4.ip_forward=1' )
        r4.cmd( 'sysctl net.ipv4.ip_forward=1' )
        r5.cmd( 'sysctl net.ipv4.ip_forward=1' )
        r6.cmd( 'sysctl net.ipv4.ip_forward=1' )
        r7.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def start_network(self):
        CLI( self )

if __name__ == '__main__':
    topo = topo1()
    topo.start_network()
    cleanup()