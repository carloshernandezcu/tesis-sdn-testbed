#!/usr/bin/python

""" TESTBED
- Simulacion hibrida con Access-Points y Estaciones inalambricas
- Enlace a Access Point fisico por tarjeta USB WiFi
- Comando: $ sudo tesis-sdn-testbed/Simulation2.py

                    .ap2.
                  .       .
                .           .
phyap. .  .ap1.               .ap4
                .
                  .
                    .ap3.
"""

from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, OVSKernelAP, Controller, RemoteController
from mininet.link import TCLink, Intf
from mininet.cli import CLI
from mininet.log import setLogLevel
from functools import partial
import subprocess

def topology():

    print "\n*** Creando la red"
    link = partial(TCLink, delay='2ms', bw=10)
    net = Mininet(controller=RemoteController, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, link=link)

    print "\n*** Creando los nodos"
    # c1 = net.addController('c1', controller=Controller)
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6653)
    ap1 = net.addAccessPoint('ap1', ssid='Campus1', mode='n', position='50,150,0', protocols='OpenFlow13')
    ap2 = net.addAccessPoint('ap2', ssid='Campus2', mode='n', position='150,215,0', protocols='OpenFlow13')
    ap3 = net.addAccessPoint('ap3', ssid='Campus3', mode='n', position='150,75,0', protocols='OpenFlow13')
    ap4 = net.addAccessPoint('ap4', ssid='Campus4', mode='n', position='250,150,0', protocols='OpenFlow13')
    sta11 = net.addStation('sta11', mac='00:00:00:00:00:11', ip='10.0.0.11/8', position='100,50,0', range=5)
    sta12 = net.addStation('sta12', mac='00:00:00:00:00:12', ip='10.0.0.12/8', position='130,50,0', range=5)
    sta13 = net.addStation('sta13', mac='00:00:00:00:00:13', ip='10.0.0.13/8', range=5)
    sta21 = net.addStation('sta21', mac='00:00:00:00:00:21', ip='10.0.0.21/8', position='100,250,0', range=5)
    sta22 = net.addStation('sta22', mac='00:00:00:00:00:22', ip='10.0.0.22/8', position='130,250,0', range=5)
    sta23 = net.addStation('sta23', mac='00:00:00:00:00:23', ip='10.0.0.23/8', range=5)
    sta41 = net.addStation('sta41', mac='00:00:00:00:00:41', ip='10.0.0.41/8', position='275,150,0', range=5)
    phyap1 = Node('phyap1')
    net.plotNode(phyap1, position='10,150,0')

    print "\n*** Iniciando servidor Web"
    sta41.cmd("python -m SimpleHTTPServer 8080 &")

    print "\n*** Configurando los nodos WiFi"
    net.configureWifiNodes()

    print "\n*** Creando los enlaces red virtual"
    net.addLink(ap1, ap2)
    net.addLink(ap1, ap3)
    net.addLink(ap2, ap4)

    print "\n*** Creando enlace red virtual a red fisica"
    Intf('wlan0', node=ap1)

    print "\n*** Activando el control de asociacion -wifi strongest signal first-"
    # net.associationControl('ssf')

    print "\n*** Iniciando la red"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])

    print "\n*** Iniciando la red fisica"
    # subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation-init.sh'])

    print "\n*** Dibujando el grafico"
    net.plotGraph(max_x=300, max_y=300)

    print "\n*** Iniciando movilidad"
    net.startMobility(time=0)
    net.mobility(sta13, 'start', time=5, position='195.0,240.0,0.0')
    net.mobility(sta23, 'start', time=5, position='195.0,50.0,0.0')
    net.mobility(sta13, 'stop', time=90, position='160.0,50.0,0.0')
    net.mobility(sta23, 'stop', time=90, position='160.0,250.0,0.0')
    net.stopMobility(time=91)

    print "\n*** Iniciar consola CLI"
    CLI(net)

    print "\n*** Deteniendo la red"
    net.stop()

    print "\n*** Deteniendo la red fisica"
    subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation-close.sh'])

if __name__ == '__main__':
    setLogLevel('info')
    topology()
