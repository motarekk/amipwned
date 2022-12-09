'''
amipwned automates the process of using haveibeenpwned's API without exposing your passwords to the internet
By: Mohamed Tarek - https://www.linkedin.com/in/mohamed-tarek-159a821ba/
this is version 2.0 of the tool
'''

import hashlib
import requests
import sys

#-------------------- variables --------------------#
signature = ("""
                 _                              _ 
  __ _ _ __ ___ (_)_ ____      ___ __   ___  __| |
 / _` | '_ ` _ \| | '_ \ \ /\ / / '_ \ / _ \/ _` |
| (_| | | | | | | | |_) \ V  V /| | | |  __/ (_| |
 \__,_|_| |_| |_|_| .__/ \_/\_/ |_| |_|\___|\__,_|  v.20
                  |_|                      motarek

                  """)                            

description = "\nBY: Mohamed Tarek\nLinkedIn: https://www.linkedin.com/in/mohamed-tarek-159a821ba/\nGitHub: https://github.com/motarekk/amipwned\n\n>> Securely offline-check if your passwords have been leaked before\n\n"

help = "> USAGE: python .\\amipwned --help\n         python .\\amipwned -p [PASSWORD]\n         python .\\amipwned -f [PASSWORDS_FILE]\n\n> EXAMPLE: python .\\amipwned -p \"helloworld\"\n           python .\\amipwned -f passwords.txt"

totalLeaked = 0

#-------------------- main function --------------------#
def findPassword(password):
    #hash the password
    hashed = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    #take first 5 chars of hashed password
    first5 = hashed[0:5]
    remaining_hash = hashed[5:len(hashed)]

    try:
        r = requests.get('https://api.pwnedpasswords.com/range/' + first5)

	#clean api response in array
        mystr = r.content.decode("utf-8")
        myarr = []
        start = 0
        n = 2

        for i in mystr:
            if n >= len(mystr):
                break
            if mystr[n] == '\r':
                k = n
                for charachter in range(2):
                    mystr.replace(mystr[k], "")
                    k = k + 1
            
                myarr.append(mystr[start:n])
                n = n + 2
                start = n
            else:
                n = n + 1

        #compare each hash in the response with the remaining hashed password
        flag = 0
        global totalLeaked
        for hash in myarr:
            if hash[0:35] == remaining_hash:
                totalLeaked += 1
                print(password + " has been leaked " + hash[36:len(hash)] + " times")
                flag = 1

        if flag == 0:
            print(password + " has been leaked 0 times")

    #through an error if not connected to the internet
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection!")

#-------------------- main program --------------------#
if len(sys.argv) < 2:
    print(signature + description + help)

elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print(help)

elif sys.argv[1] == "-p":
    
    #take password from user
    password = ""

    for arg in ' '.join(sys.argv[2:]):
        password = password + arg

    #check if password is empty
    if password == "":
        print("Please enter a password!")
        exit()

    findPassword(password)

elif sys.argv[1] == "-f":
    
    #take file from user
    file = ""

    for arg in ' '.join(sys.argv[2:]):
        file = file + arg

    #check if no file has been entered
    if file == "":
        print("Please enter a file!")
        exit()

    try:
        #read the file
        f = open(file, "r")

        #loop through the lines and search for each password
        for i in f.readlines():
            findPassword(i[:len(i)-1])

        #report final total results
        print("\n>> total leaked passwords: " + str(totalLeaked))

    #through an error if entered file is not found
    except (FileNotFoundError) as exception:
        print("file not found!")

else:
    print(help)
