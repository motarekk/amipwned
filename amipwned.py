import hashlib
import requests
import sys

signature = ("""
                 _                              _ 
  __ _ _ __ ___ (_)_ ____      ___ __   ___  __| |
 / _` | '_ ` _ \| | '_ \ \ /\ / / '_ \ / _ \/ _` |
| (_| | | | | | | | |_) \ V  V /| | | |  __/ (_| |
 \__,_|_| |_| |_|_| .__/ \_/\_/ |_| |_|\___|\__,_|  v.10
                  |_|                      motarek

                  """)                            
#help
if len(sys.argv) < 2:
    print(signature + "\nby: motarek\nLinkedIn: https://www.linkedin.com/in/mohamed-tarek-159a821ba/\n\n[+]securely offline-check if your password has been leaked before\n\nusage------ python .\\amipwned <password>\nexample------ python .\\amipwned p@$$W0rd")

elif len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("[+]securely offline-check if your password has been leaked before\n\nusage------ python .\\amipwned <password>\nexample------ python .\\amipwned p@$$W0rd")

else:
    
    #take password from user
    password = ""
    for arg in range(1, len(sys.argv)):
        password = password + sys.argv[arg]

    #hash password
    hash = hashlib.sha1(password.encode('utf-8'))
    hashed = hash.hexdigest().upper()

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
        for hash in myarr:
            if hash[0:35] == remaining_hash:
                print("This password has been leaked " + hash[36:len(hash)] + " times")
                flag = 1

        if flag == 0:
            print("This password has been leaked 0 times :)")

    #throuh an error if not connected to the internet
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection!")
