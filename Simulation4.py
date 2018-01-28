#!/usr/bin/python

""" TESTBED
- Simulacion hibrida con Access-Points y Estaciones inalambricas
- Enlace a Access Point fisico por tarjeta USB WiFi
- Controlador remoto (OpenDayLight) http://127.0.0.1:8181/index.html
- Comando: $ sudo tesis-sdn-testbed/Simulation4.py

                .ap2    .ap4
                .     .
  phyap1. . .   .  .
             .s1.
      h1. . .   .  .
                .     .
                .ap1    .ap3
"""

from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, OVSKernelAP, RemoteController
from mininet.link import TCLink, Intf
from mininet.cli import CLI
from mininet.log import setLogLevel
from functools import partial
import subprocess

def topology():
    setLogLevel('info')

    print "\n*** Creando la red"
    link = partial(TCLink, delay='2ms', bw=10)
    net = Mininet(controller=RemoteController, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, link=link)

    print "\n*** Creando los nodos"
    c1 = net.addController('c1', RemoteController, ip='127.0.0.1', port=6653)
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    net.plotNode(s1, position='40,137,0')
    h1 = net.addHost('h1', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    net.plotNode(h1, position='10,125,0')
    ap1 = net.addAccessPoint('ap1', ssid='Campus', mode='n', position='115,75,0', range=60, protocols='OpenFlow13')
    ap2 = net.addAccessPoint('ap2', ssid='Campus', mode='n', position='115,200,0', range=60, protocols='OpenFlow13')
    ap3 = net.addAccessPoint('ap3', ssid='Campus', mode='n', position='215,75,0', range=60, protocols='OpenFlow13')
    ap4 = net.addAccessPoint('ap4', ssid='Campus', mode='n', position='215,200,0', range=60, protocols='OpenFlow13')
    sta11 = net.addStation('sta11', mac='00:00:00:00:00:11', ip='10.0.0.11/8', position='90,25,0', range=5)
    sta21 = net.addStation('sta21', mac='00:00:00:00:00:21', ip='10.0.0.21/8', position='90,250,0', range=5)
    sta31 = net.addStation('sta31', mac='00:00:00:00:00:31', ip='10.0.0.31/8', position='240,25,0', range=5)
    sta41 = net.addStation('sta41', mac='00:00:00:00:00:41', ip='10.0.0.41/8', position='250,250,0', range=5)
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8', range=5)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8', range=5)
    phyap1 = Node('phyap1')
    net.plotNode(phyap1, position='10,150,0')

    print "\n*** Iniciando servidores"
    h1.cmd("python -m SimpleHTTPServer 8080 &")

    print "\n*** Configurando los nodos WiFi"
    net.configureWifiNodes()

    print "\n*** Creando los enlaces red virtual"
    #net.addLink(ap1, ap2, bw='11Mbps', loss='0.1 %'', delay='15ms')
    net.addLink(s1, h1)
    net.addLink(s1, ap1)
    net.addLink(s1, ap2)
    net.addLink(s1, ap3)
    net.addLink(s1, ap4)

    print "\n*** Creando enlace red virtual a red fisica"
    Intf('wlan0', node=s1)

    print "\n*** Activando el control de asociacion -wifi strongest signal first-"
    net.associationControl('ssf')

    print "\n*** Iniciando la red"
    net.build()
    c1.start()
    s1.start([c1])
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])

    print "\n*** Iniciando la red fisica"
    subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation-init.sh'])

    print "\n*** Dibujando el grafico"
    net.plotGraph(max_x=300, max_y=300)

    print "\n*** Iniciando movilidad"
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=5, position='265.0,50.0,0.0')
    net.mobility(sta2, 'start', time=5, position='265.0,200.0,0.0')
    net.mobility(sta1, 'stop', time=60, position='265.0,200.0,0.0')
    net.mobility(sta2, 'stop', time=60, position='265.0,50.0,0.0')
    net.stopMobility(time=61)

    print "\n*** Iniciar consola CLI"
    CLI(net)

    print "\n*** Deteniendo la red"
    net.stop()

    print "\n*** Deteniendo la red fisica"
    subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation-close.sh'])

if __name__ == '__main__':
    setLogLevel('info')
    topology()
