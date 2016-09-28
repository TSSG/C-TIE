"""
GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2016, TSSG, WIT.
"""
import threading, os, sys, time, json

from twisted.internet import defer, reactor
from stompest.config import StompConfig
from stompest.async import Stomp
from stompest.async.listener import SubscriptionListener
from stompest.async.listener import ReceiptListener
from ctie_pcap_builder import text2pcap_formatter, pairs, chunks, write_payload, generate_file_paths
from ctie_util import run_command


'''
'''
class CTIE_Queue_Manager(threading.Thread):

  def __init__(self, queue_config):
    threading.Thread.__init__ (self)

    self.queue_config = queue_config
    config = StompConfig('tcp://%s:%s' % (queue_config['activemq']['host'], queue_config['activemq']['port']),
                                          login=queue_config['activemq']['user'],
                                          passcode=queue_config['activemq']['password'],
                                          version='1.1')
    self.client = Stomp(config)


  @defer.inlineCallbacks
  def run(self):
    yield self.client.connect(host='mybroker')

    self.client.subscribe(self.queue_config['activemq']['ingress'],
                     listener=SubscriptionListener(self.handle_frame),
                     headers={'ack': 'auto', 'id': 'required-for-STOMP-1.1'})


  @defer.inlineCallbacks
  def send_frame(self, message):
    print "send_frame"
    self.client.send(destination=self.queue_config['activemq']['egress'],
                     body=message,
                     headers={'persistent': 'false'})


  @defer.inlineCallbacks
  def handle_frame(self, client, frame):
    print "handle_frame"
    print "Frame.body: " + frame.body

    try:
        data = json.loads(frame.body)
    except Exception as e:
        print type(e)
        print e.args
        print e
        print traceback.format_exc()


    data_payload = data["payload"]

    response = text2pcap_formatter(data_payload, 16)
    print "Packet payload: \n" + response

    payload_hex_file_path = write_payload(response)
    print "payload hex file path: \n" + payload_hex_file_path

    paths = generate_file_paths(payload_hex_file_path)
    pcap_file_path = paths[0]
    json_file_path = paths[1]
    print "pcap file path: \n" + pcap_file_path
    print "json file path: \n" + json_file_path

    command_text2pcap = ("./bin/text2pcap %s %s" % (payload_hex_file_path, pcap_file_path)).split()
    for line in run_command(command_text2pcap):
      print line

    command_nDPI = ("./bin/ndpiReader -i %s -j %s" % (pcap_file_path, json_file_path)).split()
    for line in run_command(command_nDPI):
      print line

    with open(json_file_path) as ndpi_json_file:
        response = json.load(ndpi_json_file)

    data["dpi_response"] = response

    self.send_frame(json.dumps(data))

######################################


  @defer.inlineCallbacks
  def stop(self, client):
    print 'Disconnecting. Waiting for RECEIPT frame ...'
    yield client.disconnect(receipt='bye')
    print 'ok'
