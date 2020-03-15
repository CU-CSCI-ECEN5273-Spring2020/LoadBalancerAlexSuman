import sys
from random import randint
import os

ADDR = "localhost"
PORT1 = randint(2000,3000)
PORT2 = randint(3001,4000)
PORT3 = randint(4001,5000)

#print(PORT1, type(PORT1))
os.system('python3 server.py PORT1')
