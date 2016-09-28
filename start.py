"""
GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2016, TSSG, WIT.
"""

from __future__ import print_function
import os, sys, inspect, time, threading
from twisted.internet import defer, reactor

# Add the lib folder as a location where modules maybe imported from
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + "/lib")
if cmd_folder not in sys.path:
  sys.path.insert(0, cmd_folder)

from ctie_queue_manager import CTIE_Queue_Manager

'''
Launch the Twisted reactor and the C-TIE application
'''
def main(config):
  qm = CTIE_Queue_Manager(config)
  qm.start()
  reactor.run()


'''
Application Entrypoint
'''
if __name__ == '__main__':
  config = {
    'activemq':{
      'user':'admin',
      'password':'admin',
      'host':'localhost',
      'port':61613,
      'ingress':'/queue/ctie.ingress', # ingress queue to the C-TIE application
      'egress':'/queue/ctie.egress' # egress queue from the C-TIE application
    }
  }

  print("Loading config:")
  print(config)

  # Launch the application
  main(config)
