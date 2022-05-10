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
files = "{}_{}.csv".format(IP,dateformat.strftime("%m%d%y"))
with PLC(IP) as comm:
        
        comm.Micro800 = microstatus
       
        with open(files, 'w') as csvfile: 
            tags = comm.GetTagList()
            fieldnames = ['Time','IP','Tag','Value', 'Data Type', 'Status']
            tagdict = {IP: []}
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for t in tags.Value:
                tagread = comm.Read(t.TagName)
                tagdict[IP].append({tagread.TagName: {'Value': tagread.Value,'Data Type':t.DataType,'Status':tagread.Status}})
                writer.writeheader()
                writer.writerow({'IP':IP,'Tag': tagread.TagName,'Value': tagread.Value,'Data Type':t.DataType,'Status':tagread.Status})



        print('Tag Data written to {}'.format(files))
