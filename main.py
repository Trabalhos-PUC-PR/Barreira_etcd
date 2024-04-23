#!/usr/bin/python3
import etcd3
import time
from sys import argv

processo = (int) ( argv[1])

client = etcd3.client()

locks = []
lock = ""
for i in range(processo):
 locks.append(client.lock((str)(i)))

for i in locks:
 if i.acquire(timeout = 0):
     lock = i
     break

print(locks[0].is_acquired())
for i in range(10):
 print(i+1)
 time.sleep(1)



print("Chegou na barreira")
cout = 0

lock.release()

for i in locks:
 i.acquire()
 i.release()

print("Saiu da Barreira")
