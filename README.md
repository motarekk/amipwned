# amipwned
A python tool that uses haveibeenpwned's API to securely offline-check if a password has been leaked before. Basically, it hashes the entered password, then uses only the first 5 characters of the hash in the web request made to the API, and give back the number that a password has been found in previous data breaches.
You can also check the full description on youtube: https://www.youtube.com/watch?v=dpbL-VvLhTA&t=965s

# requirements
python requests library:

#### Linux
> $ pip install requests 

#### Windows
> python -m pip install requests

# usage
> python amipwned [password]

#### example
> python amipwned mypass123

#### get help
> python amipwned --help
