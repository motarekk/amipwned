"""
amipwned automates the process of using haveibeenpwned's API without exposing your passwords to the internet
By: Mohamed Tarek - https://www.linkedin.com/in/mohamed-tarek-159a821ba/
this is version 2.0 of the tool
"""

import hashlib
import requests
from argparse import ArgumentParser

# -------------------- variables --------------------#
signature = ("""
                 _                              _ 
  __ _ _ __ ___ (_)_ ____      ___ __   ___  __| |
 / _` | '_ ` _ \| | '_ \ \ /\ / / '_ \ / _ \/ _` |
| (_| | | | | | | | |_) \ V  V /| | | |  __/ (_| |
 \__,_|_| |_| |_|_| .__/ \_/\_/ |_| |_|\___|\__,_|  v.2.1
                  |_|                      motarek

                  """)

description = "\nBY: Mohamed Tarek\nLinkedIn: https://www.linkedin.com/in/mohamed-tarek-159a821ba/\nGitHub: https://github.com/motarekk/amipwned\n\n>> Securely offline-check if your passwords have been leaked before\n"
usage = f"""{signature}{description}
python amipwned [-p PASSWORD]
python amipwned [-f PASSWORDS_FILE]

> EXAMPLE: 
python amipwned -p "helloworld"
python amipwned -f passwords.txt"""


def parse_arguments():
    parser = ArgumentParser(
        description="Securely offline-check if your passwords have been leaked before BY: Mohamed Tarek",
        add_help=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--password', help='search for a single password')
    group.add_argument('-f', '--file', help='search for a passwords file')
    return parser.parse_args()


totalLeaked = 0


# -------------------- main function --------------------#
def findPassword(password):
    # hash the password
    hashed = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # take first 5 chars of hashed password
    first5 = hashed[0:5]
    remaining_hash = hashed[5:len(hashed)]

    try:
        r = requests.get('https://api.pwnedpasswords.com/range/' + first5)

        # clean api response in array
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

        # compare each hash in the response with the remaining hashed password
        flag = 0
        global totalLeaked
        for hash in myarr:
            if hash[0:35] == remaining_hash:
                totalLeaked += 1
                print(password + " has been leaked " + hash[36:len(hash)] + " times")
                flag = 1

        if flag == 0:
            print(password + " has been leaked 0 times")

    # through an error if not connected to the internet
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection!")


if __name__ == "__main__":
    args = parse_arguments()
    if args.password:
        findPassword(args.password)
    elif args.file:
        try:
            for line in open(args.file, 'r').readlines():
                findPassword(line.replace('\n', ''))

            print("\n>> total leaked passwords: " + str(totalLeaked))
        except FileNotFoundError:
            print('file not found!')
        except ValueError as e:
            print(e)
    else:
        print(usage)
