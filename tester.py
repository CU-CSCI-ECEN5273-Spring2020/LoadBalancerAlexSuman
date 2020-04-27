import requests
import time
from _thread import *
import threading
import sys

succ_count = 0
fail_count = 0

count_lock = threading.Lock()

def threaded_get():
     global succ_count
     global fail_count

     try:
          resp = requests.get("http://localhost:8081", verify=False)

          if resp.status_code == 200:
               with count_lock:
                    succ_count += 1
          else:
               with count_lock:
                    fail_count += 1

     except Exception as e:
          with count_lock:
               fail_count += 1

          print(e)


if __name__ == "__main__":
     runs = int(sys.argv[1])

     if len(sys.argv) == 3:
          delay = float(sys.argv[2])
     else:
          delay = -1

     start_time = time.time_ns()

     threads = [None] * runs

     for i in range(0, runs):
          threads[i] = threading.Thread(target=threaded_get)
          threads[i].start()
          
          if delay > 0:
               time.sleep(delay)

     for i in range(0, runs):
          threads[i].join()

     end_time = time.time_ns()

     total_time = end_time - start_time
     time_ms = total_time / 1000000

     print("Success count: " + str(succ_count))
     print("Fail Count: " + str(fail_count))
     print(str(total_time) + " (" + str(time_ms) + " ms)")
          



