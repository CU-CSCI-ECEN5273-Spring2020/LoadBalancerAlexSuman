import sys
import time

from intensive_server import IntensiveServer
from daemon import daemon

class BalancerDaemon(daemon):
     def run(self):
          try:
               int_server = IntensiveServer()
               int_server.start()
          except Exception as e:
               print(e)

if __name__ == "__main__":
     daemon = BalancerDaemon('/tmp/intensive-server-daemon.pid')
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