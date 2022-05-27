import os
import sys
import time


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
from traci.connection import Connection

traci.init(port=8813, label="sim2")

conn2: Connection = traci.getConnection("sim2")
conn2.setOrder(2)

time.sleep(5)

print(traci.inductionloop.getSubscriptionResults('e1_0'))
traci.inductionloop.unsubscribe('e1_0')
print(traci.inductionloop.getSubscriptionResults('e1_0'))
