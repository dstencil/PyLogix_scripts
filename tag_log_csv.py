from pylogix import PLC
import time
from datetime import datetime
import csv
from datetime import date




now = datetime.now()
isMicro = input('Is this a Micro800?')
with PLC() as comm:
    
    comm.IPAddress = input('Enter Device Ip Address: ')
    tag = input('Enter Name of Tag to Log: ')
    read = True
    comm.Micro800 = isMicro
    fieldnames = [
        'Time',        
        'TagName',
        'Value',
        'Status'
        ]
        
    
    with open(f'{tag}_{date.today()}logged.csv', 'a+') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        f.writerow(fieldnames)
        
        while read == True:
            try:
                ret = comm.Read(tag) 
                f.writerow([datetime.now(), ret.TagName, ret.Value, ret.Status, ])
                print(str(ret)+ " " + str(datetime.now()))
                time.sleep(1)
            except KeyboardInterrupt:
                print('exiting')
                read = False
                
