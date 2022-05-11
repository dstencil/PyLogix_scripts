import datetime
import csv
from pylogix import PLC

IP = input('Enter AB PLC IP Address xxx.xxx.xxx.xxx \n')
microstatus = input('is PLC a Micro800 series? (y or n) def(n) \n')
if microstatus == 'y':
    microstatus = True
else:
    microstatus = False
dateformat = datetime.datetime.now()
date_formatted = dateformat.strftime("%m%d%y")
files = f"{IP}_{date_formatted}.csv"
with PLC() as comm:
        comm.IPAddress = IP
        tags = comm.GetTagList()
        fieldnames = [        
        'TagName',
        'InstanceID',
        'SymbolType',
        'DataTypeValue',
        'DataType',
        'Array',
        'Struct',
        'Size',
        'AccessRight',
        'Internal',
        'Meta',
        'Scope0',
        'Scope1',
        'Bytes']
       
        comm.Micro800 = microstatus

       
        with open(files, 'w') as f: 
            f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
            f.writerow(fieldnames)
            for t in tags.Value:
                f.writerow([        
                    t.TagName,
                    t.InstanceID,
                    t.SymbolType,
                    t.DataTypeValue,
                    t.DataType,
                    t.Array,
                    t.Struct,
                    t.Size,
                    t.AccessRight,
                    t.Internal,
                    t.Meta,
                    t.Scope0,
                    t.Scope1,
                    t.Bytes])
            


        print('Tag Data written to {}'.format(files))
