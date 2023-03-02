# RandomRestaurant

## This app was created with the intention to help indecisive consumers choose their next restaurant!

**Steps to run**
1. Clone the github repository using `git clone https://github.com/jcng75/RandomRestaurant/`

2. Please confirm that you have python installed, by running the command `python --version`.
If not installed, please do so by downloading it on https://www.python.org/downloads/.

3. In your preferred terminal, make sure the django library is installed by running the command:
`pip install django`

4. Within the *settings.py* in `src/src/settings.py`, please make the following modifications:
Please delete the line: load_dotenv(find_dotenv())
Add your own secret key to this line:
SECRET_KEY = os.environ['SECRET_KEY']
It should look something like this: SECRET_KEY = '$b9a(z6pzrn)enuk==3+up@t)q0eknd&m#@n9%5nmsl+mpdaem'
NOTE: The secret key should be a 50 character randomly generated key.
If you are not sure how to generate this key, you can run the following code snippet into your python compiler:
`
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
`
5. Within the *src* directory (the outer one), run the following command: `python manage.py runserver`

From there, you should be able to view the webserver in a browser entering the URL: *http://127.0.0.1:8000/*
