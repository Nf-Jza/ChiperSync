#!/usr/bin/env python3

import sys
from io import BytesIO
import os

# ["ChiperSync.py","-h"]
# ["ChiperSync","-U","file.txt","Passphrase"]
import subprocess
import importlib

def ConfirmQ(question:str):
    final = bool()

    inp = input(f"{question} [Y/n] : ")
    passed = [['Y','y'],['N','n']]

    if inp[0] in passed[0]:
        return True
    elif inp[0] in passed[1]:
        return False
    else:
        print('Unknown option!')
        final = ConfirmQ(question)
        return final



def importPkg(packages:list):
    noPkg = []
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ImportError:
            noPkg.append(pkg)

    if len(noPkg)==0:
        pass
    elif len(noPkg)>0:
        print('Required to install the following package/s :\n')
        [print(f'    - {_}') for _ in noPkg]
        install = ConfirmQ('\nContinue to install?')
        if install == True:
            print(noPkg)
            subprocess.check_call(["pip3","install"]+noPkg)
        elif install == False:
            pass

importPkg(["pycurl","python-gnupg"])


gpg = gnupg.GPG()
c = pycurl.Curl()


if __name__ == "__main__":
    listArgs = sys.argv
    helpString = """
[ ChiperSync ]
A program for upload and download file with encryption support. And try to connect to VPN first if this doesn't work.

    How to use :
        ChiperSync [-U]/[-D] [filename]/[link] [passphrase]
        ex.
            ChiperSync -D https://transfer.sh/file.txt YourPassphrase

    Actions:
        -U,--upload | Upload a file
        -D,--download | Download a file
        -h, --help | Print this message
"""
    unknownCMD = 'Unknown command, use -h or --help for how to use.'

    def Upload(file:str,passp:str):

        tmpFile = ".ChiperSyncU.enc.tmp"
        returnStr = {}
        
        try:
            with open(file,"rb") as f:
                data = f.read()
                encrypted_data = gpg.encrypt(data, recipients=None, symmetric='AES256', passphrase=passp,armor=False).data

                with open(tmpFile,"wb") as tmpEnc:
                    tmpEnc.write(encrypted_data)

            
            filePath = file.split("/")[-1]
            buffer = BytesIO()
            upload_url = 'https://free.keep.sh/' + filePath
            c.setopt(c.URL, upload_url)
            c.setopt(c.UPLOAD, 1)
            c.setopt(c.READDATA, open(tmpFile, 'rb'))
            c.setopt(c.WRITEDATA,buffer)
            c.perform()
            c.close()
            os.remove(tmpFile)
            final =  buffer.getvalue().decode()
            returnStr["Status"] = True
            returnStr["StatusMessage"] = f"Successfully upload and encrypt -> {filePath}\n\nThe Url : {final}"

        except Exception as e:
            returnStr["Status"] = False
            returnStr["StatusMessage"] = f'An Error occured : {e}'

        return returnStr

    def Download(link:str,passp:str):

        tmpFile = ".ChiperSyncD.enc.tmp"
        filename = link.split("/")[-1]
        returnStr = {}
        try:
            c.setopt(c.URL, link)
            c.setopt(c.FOLLOWLOCATION,True)
            c.setopt(c.WRITEDATA, open(tmpFile,"wb"))
            c.perform()
            c.close()

            with open(tmpFile,"rb") as dec:
                decrypted_data = gpg.decrypt(dec.read(),passphrase=passp)
                with open(filename,"wb") as final:
                    final.write(decrypted_data.data)

            returnStr["Status"] = True
            returnStr["StatusMessage"] = f"Successfully download and decrypt -> {filename}"
            os.remove(tmpFile)
        except Exception as e:
            returnStr["Status"] = False
            returnStr["StatusMessage"] = f'An Error occured : {e}'
            
        return returnStr



    if len(sys.argv) == 1:
        print(helpString)
    elif listArgs[1]=='-h' or listArgs[1]=='--help':
        print(helpString)
    elif listArgs[1]=='-U' or listArgs[1]=='--upload':
        if len(listArgs)==2 or len(listArgs)==3:
            uploadStr = """
How to upload :
    ChiperSync [-U]/[--upload] [filename] [passphrase]
"""
            print(uploadStr)
        else:
            done = Upload(listArgs[2],listArgs[3])
            
            if done["Status"] == True:
                print(done["StatusMessage"])
            else:
                print(done["StatusMessage"])

    elif listArgs[1]=='-D' or listArgs[1]=='--download':
        if len(listArgs)==2 or len(listArgs)==3:
            downloadStr = """
How to download :
    ChiperSync [-D]/[--download] [link] [passphrase]

"""
            print(downloadStr)
        else:
            done = Download(listArgs[2],listArgs[3])

            if done["Status"] == True:
                print(done["StatusMessage"])
            else:
                print(done["StatusMessage"])

    else :
        print(unknownCMD)
