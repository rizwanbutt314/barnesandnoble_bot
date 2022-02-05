### Description:
This assignment consists of two parts which are:
* To get alert message via forgot password on `https://www.barnesandnoble.com`
* Get email content from Gmail using it's API against keyword: `barnesandnoble`

### PreReqs:
* Python: 3.8+
* Latest Chrome Browser for `barnesandnoble` automation
* GMAIL API credentials file with name `credentials.json` and this API should have following access scope:
```
https://www.googleapis.com/auth/gmail.readonly
```

### Setup:
* create a virtual environment: `virtualenv -p /usr/bin/python3 env` (Optional)
* activate the environemnt: `source ./env/bin/activate` (Optional when you don't need first step)
* install requirements: `pip install -r requirements.txt`
* Edit `utils.py` file to update the following variables, Set proxy variables if proxy is needed
```
EMAIL = "test@test.com"
SOCK_PROXY_HOST = "127.0.0.1"
SOCK_PROXY_PORT = "9050"
```
* Edit `gmail_reader.py` file to update the `QUERY` variable which will be used as search keyword to filter gmail emails
```
QUERY = "barnesandnoble"
```

### Run:
* Command to run barnesandnoble automation: `python barnesandnoble.py`
* Command to run gmail reader: `python gmail_reader.py`

### Note:
*  `requirements.txt` file contains the list of packages that are required to install.
* Extracted information will be saved in file: `output.csv`
* Plus the information will be saved in a MySQL database too.