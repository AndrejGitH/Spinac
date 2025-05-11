#1. User enters credentials as parameters
#2. Try connet to the server by SSH
#3. Try download the file via sftp
#4. Try update and sent file back via sftp
#5. Close connection


#Library allowing us to connect to the linux server
import paramiko
#Module to allow us work with xml file
import xml.etree.ElementTree as ET

#Connection parameters - user provided
hostname = input("Enter hostname/IP adress: ")
user = input("Enter username: ")
password = input("Enter password: ")
linuxXML_path = input("Enter Linux file path: ")
local_path = input("Enter local file path: ")
port = 22

def process_xml_file(hostname, user, password, linuxXML_path, local_path, port=22):

try: 

    #Connecting to the server via SSH
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, user, password)

    print("SSH connection established!")

except Exception as e:
    print("Connection failed:", e)
    exit()

#XML downloading
try:
    sftp = client.open_sftp()
    sftp.get(linuxXML_path, local_path)
    print("XML downloaded!")
except FileNotFoundError:
    print("XML file not found!")
    exit()
except Exception as ex:
    print("File download failed! Details: ", ex)
    exit()

#Updating the file and sending to the linux server via sftp
try:
    tree = ET.parse(local_path)
    root = tree.getroot()

    updated = False

    for element in root.iter('light'):
        if element.text.lower() == "true":
            element.text = "false"
            updated = True

    if updated:
        tree.write(local_path)
        print("XML updated!")
        sftp.put(local_path, linuxXML_path)
        print("XML uploaded to the linux client!")

    else:
        print("No light element with true value found!")

except FileNotFoundError:
    print("Local path is wrong! No XML found.")
    exit()
except ET.ParseError:
    print("Error occured while parsing the file!")
    exit()
except Exception as exc:
    print("Error occured, details: ", exc)
    exit()

    
finally:
    sftp.close()
    client.close()