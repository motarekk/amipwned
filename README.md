# amipwned v2.1
A python tool that automates the process of using haveibeenpwned's API without exposing your passwords to the internet. Basically, it hashes the entered password with SHA1, then uses only the first 5 characters of the hash in the web request made to the API, and give back the number of that password has been found in previous data breaches, without sending your clear-text passwords or its full hashes within the web request to the internet.
You can either give it one password or a file of passwords, and it will do the work for you!
You can also check the full demonstration of v1.0 on youtube: https://youtu.be/dpbL-VvLhTA


https://user-images.githubusercontent.com/104282801/206707045-fdc3d43f-d297-4078-a260-86a02e8f71e3.mp4


# requirements
python requests library:

#### Linux
> \> pip install requests 

#### Windows
> \> python -m pip install requests

# usage
> \> python3 amipwned -p [PASSWORD] <br />
> \> python3 amipwned -f [FILE]

#### example
> \> python3 amipwned -p "hello world" <br />
> \> python3 amipwned -p "pswds.txt"

#### get help
> \> python3 amipwned --help <br />
> \> python3 amipwned -h
