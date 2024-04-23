#!/usr/bin/python3
import etcd3
import time
from sys import argv

processo = (int) (argv[1])
client = etcd3.client()

chave = 'latest'
locks = []
lock = ""
for i in range(processo):
    locks.append(client.lock((str)(i)))

for i in locks:
    if i.acquire(timeout = 0.1):
        lock = i
        client.put(chave, (str)(locks.index(i)+1))
        break

print(f'processo #{((int)(client.get(chave)[0]))}')
for i in range(10):
    print(i+1)
    time.sleep(1)

print("Esperando outros processos começarem para chegar na barreira")

while(((int)(client.get(chave)[0])) != processo):
    pass
    
print("Chegou na barreira")
lock.release()

for i in locks:
    i.acquire()
    i.release()

print("Saiu da Barreira")
