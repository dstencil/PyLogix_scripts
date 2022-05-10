from pylogix import PLC
import time
from datetime import datetime

now = datetime.now()

with PLC() as comm:
    
    comm.IPAddress = input('Enter Device Ip Address: ')
    tag = input('Enter Name of Tag to Log: ')
    read = True
    comm.Micro800 = True
    with open('tagstore.txt', 'w') as f:
        while read == True:
            try:
                ret = comm.Read(tag) 
                f.write(f'{ret} {datetime.now()}\n')
                print(str(ret)+ " " + str(datetime.now()))
                time.sleep(1)
            except KeyboardInterrupt:
                print('exiting')
                read = False
                f.close()
