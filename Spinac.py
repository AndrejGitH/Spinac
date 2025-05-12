#1. User enters credentials as parameters
#2. Try connect to the server by SSH
#3. Try download the file via sftp
#4. Try update and send file back via sftp
#5. Close connection
#6. Structure it into methods

# Library allowing us to connect to the linux server
import paramiko
# Module to allow us to work with xml files
import xml.etree.ElementTree as ET

def update_xml_file_linux(hostname, user, password, linuxXML_path, local_path, element_tag, port=22):
    """Connects to a Linux server via SSH, downloads an XML file, updates element, and uploads it back."""

    try:
        # Connecting to the server via SSH
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, user, password)
        print("SSH connection established!")
    except Exception as e:
        print("Connection failed:", e)
        return

    try:
        # XML downloading
        sftp = client.open_sftp()
        sftp.get(linuxXML_path, local_path)
        print("XML downloaded!")
    except FileNotFoundError:
        print("XML file not found!")
        return
    except Exception as ex:
        print("File download failed! Details: ", ex)
        return

    # Updating the file and sending it back to the linux server via SFTP
    try:
        tree = ET.parse(local_path)
        root = tree.getroot()

        updated = False

        for element in root.iter(element_tag):
            if element.text and element.text.lower() == "true":
                element.text = "false"
                updated = True

        if updated:
            tree.write(local_path)
            print("XML updated!")
            sftp.put(local_path, linuxXML_path)
            print("XML uploaded to the Linux client!")
        else:
            print("No light element with true value found!")
    except FileNotFoundError:
        print("Local path is wrong! No XML found.")
    except ET.ParseError:
        print("Error occurred while parsing the file!")
    except Exception as exc:
        print("Error occurred, details: ", exc)
    finally:
        sftp.close()
        client.close()

def main():
    # User provided connection parameters
    hostname = input("Enter hostname/IP address: ")
    user = input("Enter username: ")
    password = input("Enter password: ")
    linuxXML_path = input("Enter Linux file path: ")
    local_path = input("Enter local file path: ")
    element_tag = input("Enter XML element tag to update: ")

    #Def call
    update_xml_file_linux(hostname, user, password, linuxXML_path, local_path, element_tag)
