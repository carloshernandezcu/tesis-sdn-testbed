#!/usr/bin/python

""" TESTBED
- Simulacion hibrida con Access-Points y Estaciones inalambricas
- Enlace a Access Point fisico por tarjeta USB WiFi
- Configuracion Mesh
- Comando: $ sudo tesis-sdn-testbed/Simulation3.py

            sta1 ->                    <- sta2

phyap. . . .ap1. . . .ap2. . . .ap3. . . .ap4
             .         .         .         .
             .         .         .         .
            sta1      sta2      sta3      sta4
"""

from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, OVSKernelAP, Controller, RemoteController
from mininet.link import TCLink, Intf
from mininet.cli import CLI
from mininet.log import setLogLevel
from functools import partial
import subprocess

def topology():

    print "\n*** Crear la red"
    net = Mininet(enable_wmediumd=True, controller=Controller, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, link=TCLink)

    print "\n*** Crear los nodos"
    c1 = net.addController('c1', controller=Controller)
    ap1 = net.addWirelessMeshAP('ap1', ssid='Campus', mode='n', channel= '1', position='50,150,0', ip='10.0.0.101/8')
    ap2 = net.addWirelessMeshAP('ap2', ssid='Campus', mode='n', channel= '1', position='115,150,0', ip='10.0.0.102/8')
    ap3 = net.addWirelessMeshAP('ap3', ssid='Campus', mode='n', channel= '1', position='180,150,0', ip='10.0.0.103/8')
    ap4 = net.addWirelessMeshAP('ap4', ssid='Campus', mode='n', channel= '1', position='245,150,0', ip='10.0.0.104/8')
    sta11 = net.addStation('sta11', mac='00:00:00:00:00:11', ip='10.0.0.11/8', position='50,100,0', range=5)
    sta21 = net.addStation('sta21', mac='00:00:00:00:00:21', ip='10.0.0.21/8', position='115,100,0', range=5)
    sta31 = net.addStation('sta31', mac='00:00:00:00:00:31', ip='10.0.0.31/8', position='180,100,0', range=5)
    sta41 = net.addStation('sta41', mac='00:00:00:00:00:41', ip='10.0.0.41/8', position='245,100,0', range=5)
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8', position='0,0,0', range=5)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8', position='0,0,0', range=5)
    phyap1 = Node('phyap1')
    net.plotNode(phyap1, position='10,150,0')

    print "\n*** Iniciar servidor Web"
    sta41.cmd("python -m SimpleHTTPServer 8080 &")

    print "\n*** Configurando los nodos WiFi"
    net.configureWifiNodes()

    print "\n*** Crear los enlaces red virtual"
    net.addMesh(ap1, ssid='meshNet')
    net.addMesh(ap2, ssid='meshNet')
    net.addMesh(ap3, ssid='meshNet')
    net.addMesh(ap4, ssid='meshNet')
    net.addMesh(sta1, ssid='meshNet')
    net.addMesh(sta2, ssid='meshNet')
    net.addMesh(sta11, ssid='meshNet')
    net.addMesh(sta21, ssid='meshNet')
    net.addMesh(sta31, ssid='meshNet')
    net.addMesh(sta41, ssid='meshNet')

    print "\n*** Crear enlace red virtual a red fisica"
    Intf('wlan0', node=ap1)

    print "\n*** Activar el control de asociacion -wifi strongest signal first-"
    net.associationControl('ssf')

    print "\n*** Iniciar la red"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])

    print "\n*** Iniciar la red fisica"
    # subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation-init.sh'])

    print "\n*** Dibujar el grafico"
    net.plotGraph(max_x=300, max_y=300)

    print "\n*** Iniciar movilidad"
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=5, position='195.0,240.0,0.0')
    net.mobility(sta2, 'start', time=5, position='195.0,50.0,0.0')
    net.mobility(sta1, 'stop', time=60, position='160.0,50.0,0.0')
    net.mobility(sta2, 'stop', time=60, position='160.0,250.0,0.0')
    net.stopMobility(time=61)

    print "\n*** Iniciar consola CLI"
    CLI(net)

    print "\n*** Detener la red"
    net.stop()

    print "\n*** Detener la red fisica"
    subprocess.check_call(['/home/wifi/mininet-wifi/tesis-sdn-testbed/Simulation-close.sh'])

if __name__ == '__main__':
    setLogLevel('info')
    topology()
