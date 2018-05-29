
##################################
#       AGENTE PRINCIPAL         #
##################################
'''
This is the most simple example about how
to send a message between 2 agents
'''

import os
import sys
import time
import string
import unittest

sys.path.append('..')

import spade

host = "127.0.0.1"


class Red(spade.Agent.Agent):

    def _setup(self):
		self.addBehaviour(self.RedMsgBehav())
		print "LANZADOR DE LA RED ENCENDIDO"
		
    class RedMsgBehav(spade.Behaviour.OneShotBehaviour):

        def _process(self):
            print("La red sera lanzada")
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.addReceiver(spade.AID.aid("b@"+host,["xmpp://b@"+host]))
            caudalE = input("Ingrese Caudal Entrada: ")
            caudalCh = input("Ingrese caudal de la chaqueta: ")
            msg.setContent([caudalE,caudalCh])#aca hay que poner los dados de caudales de entrada 
            self.myAgent.send(msg)
            print("Se enviaron las cosas al fuzzy:")
            print(msg.getContent())
            
            
            
            
class Fuzzy(spade.Agent.Agent):
    
    class FuzzyMsgBehav(spade.Behaviour.EventBehaviour):

        def _process(self):
            msg = self._receive(block=True,timeout=10)
            print "La fuzzy recibio el mensaje:"
            print(msg.getContent())
    
    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        t = spade.Behaviour.MessageTemplate(template)
        
        self.addBehaviour(self.FuzzyMsgBehav(),t)
        
	print "Fuzzy arrancada"
    
    
a = Red("a@"+host,"secret")
b = Fuzzy("b@"+host,"secret")

b.start()
import time
time.sleep(1)
a.start()

alive = True
import time
while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
a.stop()
b.stop()
sys.exit(0)
