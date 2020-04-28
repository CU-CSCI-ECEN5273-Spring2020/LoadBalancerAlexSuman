import sys
import time

from balancer import Balancer
from daemon import daemon

class BalancerDaemon(daemon):

     LoadBalancer = None

     def run(self):
          try:
               BALANCER_HOST = "0.0.0.0"
               BALANCER_PORT = 8888
               SERVERS = [
                              {"protocol": "http://", "host": "35.247.73.142",  "port":8080},
                              {"protocol": "http://", "host": "34.106.248.143", "port":8080},
                              {"protocol": "http://", "host": "34.125.74.70",   "port":8080}
                         ]
               LoadBalancer = Balancer(BALANCER_HOST, BALANCER_PORT, SERVERS)
               LoadBalancer.mode = Balancer.MODE_ROUNDROBIN
               LoadBalancer.verbose = False
               LoadBalancer.start()
          except Exception as e:
               print(e)

if __name__ == "__main__":
     daemon = BalancerDaemon('/tmp/balancer-daemon.pid')
     if len(sys.argv) == 2:
          if 'start' == sys.argv[1]:
               daemon.start()
          elif 'stop' == sys.argv[1]:
               daemon.stop()
          elif 'restart' == sys.argv[1]:
               daemon.restart()
          else:
               print("Unknown command")
               sys.exit(2)
          sys.exit(0)
     else:
          print("Usage: %s start|stop|restart" % sys.argv[0])
          sys.exit(2)