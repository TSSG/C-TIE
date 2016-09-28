"""
GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2016, TSSG, WIT.
"""
import subprocess

# Execute a shell command and return the output
def run_command(command):
  p = subprocess.Popen(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
  return iter(p.stdout.readline, b'')
  
