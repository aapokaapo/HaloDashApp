# HaloDashApp
HaloDashApp is a web app for Halo Infinite. It pulls player's match history straight from Xbox servers and presents them in human-readable form, meaning lots of colors and graphs. 
The app uses [SPNKr.py](https://github.com/acurtis166/spnkr) to authenticate with Halo Infinite API

## How-To: Get Started
Clone the repository
```
git clone https://github.com/aapokaapo/HaloDashApp.git
```
Install the required python packages
```
pip3 install -r requirements.txt
```
Create Azure AD app and acquire refresh token using the instructions found [here](https://acurtis166.github.io/SPNKr/getting-started/)

Put the required variable into `app/tokens.py`
```
AZURE_CLIENT_ID = "string"
AZURE_CLIENT_SECRET = "string"
REDIRECT_URI = "https://localhost"
AZURE_REFRESH_TOKEN = "string"
```
For local development you can run the python script with
```
python3 main.python3
```
For production level deployement you should use a WSGI, such as `gunicorn`
```
gunicorn -w 2 main:servers
```

