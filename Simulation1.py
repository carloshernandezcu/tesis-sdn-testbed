#!/usr/bin/python

"Testbed - Simulacion #1 con Access-Points y Estaciones virtuales mas Enlace Fisico"
"ejecutar comando: sudo tesis-sdn-testbed/Simulation1.py"

import subprocess
from mininet.net import Mininet
from mininet.node import OVSSwitch, OVSKernelSwitch, OVSKernelAP, Controller, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():

    print "*** Creando la red"
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print "*** Creando los nodos"
    c1 = net.addController('c1', controller=Controller)
    s1 = net.addSwitch('s1')
    net.plotNode(s1, position='40,137,0')
    h1 = net.addHost ('h1', ip='10.0.0.3/8')
    net.plotNode(h1, position='10,137,0')
    ap1 = net.addAccessPoint('ap1', ssid='Campus', mode='n', channel='1', position='115,75,0')
    ap2 = net.addAccessPoint('ap2', ssid='Campus', mode='n', channel='4', position='115,200,0')
    ap3 = net.addAccessPoint('ap3', ssid='Campus', mode='n', channel='8', position='215,75,0')
    ap4 = net.addAccessPoint('ap4', ssid='Campus', mode='n', channel='11', position='215,200,0')
    sta11 = net.addStation('sta11', mac='00:00:00:00:00:11', ip='10.0.0.11/8', position='90,25,0', range=5)
    sta21 = net.addStation('sta21', mac='00:00:00:00:00:21', ip='10.0.0.21/8', position='90,250,0', range=5)
    sta31 = net.addStation('sta31', mac='00:00:00:00:00:31', ip='10.0.0.31/8', position='240,25,0', range=5)
    sta41 = net.addStation('sta41', mac='00:00:00:00:00:41', ip='10.0.0.41/8', position='250,250,0', range=5)
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8', range=5)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8', range=5)

    print "*** Iniciando servidores"
    h1.cmd("python -m SimpleHTTPServer 8080 &")

    print "*** Configurando los nodos WiFi"
    net.configureWifiNodes()

    print "*** Creando los enlaces y asociaciones"
    # net.addLink(ap1, ap2, bw='11Mbps', loss='0.1 %'', delay='15ms')
    net.addLink(s1, h1)
    net.addLink(s1, ap1)
    net.addLink(s1, ap2)
    net.addLink(s1, ap3)
    net.addLink(s1, ap4)

    print "*** Iniciando la red"
    net.build()
    c1.start()
    s1.start([c1])
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])

    print "*** Iniciando la red fisica"
    subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation1-init.sh'])

    print "*** Dibujando el grafico"
    net.plotGraph(max_x=300, max_y=300)

    print "*** Iniciando movilidad"
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=5, position='265.0,50.0,0.0')
    net.mobility(sta2, 'start', time=5, position='265.0,200.0,0.0')
    net.mobility(sta1, 'stop', time=60, position='265.0,200.0,0.0')
    net.mobility(sta2, 'stop', time=60, position='265.0,50.0,0.0')
    net.stopMobility(time=61)

    print "*** Iniciar consola CLI"
    CLI(net)

    print "*** Deteniendo la red"
    net.stop()

    print "*** Deteniendo la red fisica"
    subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation1-close.sh'])

if __name__ == '__main__':
    setLogLevel('info')
    topology()
