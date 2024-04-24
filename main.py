#!/usr/bin/python3
import etcd3
import time
from sys import argv
import random

processo = (int) (argv[1])
client = etcd3.client()
chave = 'latest'
locks = []
lock = ""
pre_lock = ""

def getValor(chave):
    return ((int)(client.get(chave)[0])) 

def callback(_):
    latest = getValor(chave)
    print(f'latest={latest}|processo={processo}')
    if(latest >= processo):
        pre_lock.release()

for i in range(processo):
    locks.append(client.lock((str)(i)))
pre_lock = client.lock("pre")
if not(pre_lock.is_acquired()):
    pre_lock.acquire(0)

for i in locks:
    if i.acquire(timeout = 0.1):
        lock = i
        client.add_watch_callback(chave, callback)
        client.put(chave, (str)(locks.index(i)+1))
        break

print(f'\tprocesso #{((int)(client.get(chave)[0]))}')
for i in range(10):
    print(i+1)
    time.sleep(1)

print(f"Esperando todos os {processo} processos começarem")
pre_lock.acquire(None)
pre_lock.release()
print("Chegou na barreira")
lock.release()

for i in locks:
    i.acquire()
    i.release()

print("Saiu da Barreira")

