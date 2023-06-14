from hashlib import sha1
from requests import get, Timeout
from argparse import ArgumentParser
#test
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
python3 amipwned [-p PASSWORD]
python3 amipwned [-f PASSWORDS_FILE]

> EXAMPLE: 
python3 amipwned -p "hello world"
python3 amipwned -f passwords.txt"""


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
    hashed = sha1(password.encode('utf-8')).hexdigest().upper()

    # take first 5 chars of hashed password
    head = hashed[0:5]
    tail = hashed[5:len(hashed)]

    try:
        req = get('https://api.pwnedpasswords.com/range/' + head)

        # clean api response
        req_content = req.content.decode("utf-8").replace('\r','').split('\n')

        # compare each hash in the response with the remaining hashed password
        leaked = False
        global totalLeaked
        for hash in req_content:
            if hash[0:35] == tail:
                totalLeaked += 1
                print(password + " has been leaked " + hash[36:len(hash)] + " times")
                leaked = True

        if not leaked:
            print(password + " has been leaked 0 times")

    # through an error if not connected to the internet
    except (ConnectionError, Timeout) as exception:
        print("No internet connection!")


# -------------------- output --------------------#
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
