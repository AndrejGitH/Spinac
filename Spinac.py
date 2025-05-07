#1. Download XML config from linux
#2. Change element light from true to false in the xml config file
#3. Upload xml file back to the linux


#Library allowing us to connect to the linux server
import paramiko
#Module to allow us work with xml file
import xml.etree.ElementTree as ET

#Connection variables
hostname = "127.0.0.1"
port = 22
user = "Siemens"
password = "Python"


try: 

    #Connection logic
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, user, password)

    print("SSH connection established!")

#Parsing and updating the xml config file
    sftp = client.open_sftp()
    linuxXML_path = "path/config.xml"
    local_path = "C:/Desktop/config.xml" 
    
    sftp.get(linuxXML_path, local_path)
    print("XML downloaded!")

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

    sftp.close()
    client.close()

except Exception as e:
    print("Connection failed,:", e)