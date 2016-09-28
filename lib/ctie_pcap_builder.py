"""
GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2016, TSSG, WIT.
"""
import time, hashlib, os
from random import randint


'''
Generate the pcap file path from the payload hex file path
'''
def generate_file_paths(payload_hex_file_path):
    dir_path = os.path.dirname(payload_hex_file_path)
    print dir_path

    file_name = os.path.basename(payload_hex_file_path)
    print file_name

    file_name_without_extension = os.path.splitext(file_name)[0]
    print file_name_without_extension

    pcap_file_name = file_name_without_extension + ".pcap"
    print pcap_file_name

    json_file_name = file_name_without_extension + ".json"
    print json_file_name

    pcap_file_path = os.path.join(dir_path, pcap_file_name)
    print pcap_file_path

    json_file_path = os.path.join(dir_path, json_file_name)
    print json_file_path

    return [pcap_file_path, json_file_path]

'''
Write the payload to a file suitable for passing to text2pcap utility
'''
def write_payload(payload):
  script_location = "tmp"
  print script_location
  directory = "./tmp"

  if not os.path.exists(directory):
    os.makedirs(directory)

  timestamp = str(int(time.time()))
  print timestamp

  salt = 'dpi_pcap_generation_salt' + str(randint(0,100000000))
  salt_time_hash = hashlib.sha512( salt + timestamp ).hexdigest()
  final_hash = salt_time_hash[0:10]

  final_file_name = "dpi_input_%s_%s.txt" % (final_hash, timestamp)
  final_file_path =  os.path.abspath(os.path.join(script_location, final_file_name))
  print final_file_path

  f = open(final_file_path, "w")
  f.truncate()
  f.write(payload)
  f.write("\n")
  f.close()

  return final_file_path


'''
Split the payload string into groups of size n
'''
def pairs(payload, n):
  print "pairs"
  return [payload[i:i+n] for i in range(0, len(payload), n)]

'''
Function will split a list l into chunks of size n
'''
def chunks(l, n):
  '''Yield successive n-sized chunks from l'''
  print "chunks"
  for i in range(0, len(l), n):
    yield l[i:i+n]

'''
Function will print the payload content in the format expected by the text2pcap utility
for more information see: https://www.wireshark.org/docs/man-pages/text2pcap.html
'''
def text2pcap_formatter(payload, n):
  print "text2pcap_formatter"
  print n
  # Split the payload string into hex character pairs eg: 0d ff
  hex_pairs = pairs(payload, 2)
  print hex_pairs

  #split the packet into chunks of size n
  hex_chunks = list(chunks(hex_pairs, n))
  print hex_chunks

  count = 0
  final_size = ""
  payload_response = ""

  for i in hex_chunks:
    if len(i) < n:
      line_size = format(count, '06x')
      final_size = format(count + len(i), '06x')
      line = ""

      for j in i:
        line += " " + j
        count += 1

      payload_response += line_size + line + "\n"
      payload_response += final_size
    else:
      line_size = format(count, '06x')
      line = ""

      for j in i:
        line += " " + j
        count += 1

      payload_response += line_size + line + "\n"

  return payload_response
