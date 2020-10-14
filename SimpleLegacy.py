import csv
import netmiko

'''
Below is a very basic script that is built to connect to cisco_ios devices via ssh and the cli.
You will provide the list of networking devices in a .csv file that should follow the below format:

   ip, devicename, id
   10.10.100.248, SW-1, 1
   10.10.100.247, SW-2, 2

A simple for loop will iterate through the .csv file and issue the intended CLI command.
The result from the command will be saved in Output.csv file along with any errors that may have occured.
'''

# Opening of our devicelist.csv file. Please load this file with your own data.
# Should you not have any Lab equipment to test with then reference the devnet sandboxes(Devnet peeps can review this) 
csv_file = open('devicelist.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
next(csv_reader)

#Specifying the output file for our data. Giving it write access
output = open('Output.csv','w')

userName = "NetworkTruck" #Change what is inbetween the "" to your username
passWord = "Truck123" # Make sure to keep this a bit safer :P
command = "show cdp n" # Change this to what command you are wanting to run

#Opening the for loop and telling it to do the below code for each row in our devicelist.csv
for row in csv_reader:
   ip, devicename, id = row #assigning the variables to each row.
   
   # Using the try:/except to catch any common errors
   try:

       # Creating our connection to the device. netmiko.ConnectHandler does all the heavy lifting for us here
       # Username and password is here to keep this simple, but really should be moved for better security
         connection = netmiko.ConnectHandler(ip= ip, device_type="cisco_ios",username=userName, password=passWord,timeout=30)
        
        
         print(id, devicename,file=output) #Adds the id and device name to our output file
         
         #Below code is the actual execution of the cli command. We specify that it will return the information to our output file
         print(connection.send_command(command),file=output)
         print(devicename + " completed")
         connection.disconnect() # Always good to disconnect :)
      
      # Exceptions to catch errors and save them rather than it interrupt the for loop.
      # Creates a place to try different things once exceptions are hit.   
   except netmiko.ssh_exception.NetMikoAuthenticationException:
       print(id,'@ Authentication Failed',devicename,file=output)
       print("Was  unable to connect to" + devicename)
   except netmiko.NetMikoTimeoutException:
       print(id,'@ Timed out',devicename,file=output)
       print("Was  unable to connect to" + devicename)
   except (ValueError): 
       print(id,'@ value error', devicename,file=output)
       print("Was  unable to connect to" + devicename)
   except netmiko.ssh_exception.SSHException:
       print(id,'@ ssh exception', devicename,file=output)
       print("Was  unable to connect to" + devicename)
       # example would be to try connect here with telnet rather than the default ssh should a SSHException be hit
       """connection = netmiko.ConnectHandler(ip= ip, device_type="cisco_ios_telnet",username="NetworkTruck", password="Truck123",timeout=30)
         time.sleep(2)
        """
   except (OSError): 
       print (id,'@ OS error', devicename,file=output)
       print("Was  unable to connect to" + devicename)