import os, time

NUM_PROCESSES = 7

def timeConsumingFunction():
    x = 1
    for n in xrange(10000000):
        x += 1

children = []

start_time = time.time()
for process in range(NUM_PROCESSES):
    pid = os.fork()
    if pid:
        children.append(pid)
    else:
        timeConsumingFunction()
        os._exit(0)

for i, child in enumerate(children):
    os.waitpid(child, 0)

print time.time() - start_time