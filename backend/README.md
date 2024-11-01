# Promotion With Peers

## Team (F15 Group 7)

| Name | Unikey | SID |
| ---- | ---- | ---- |
| Baocheng Wang | bwan3675 | 480508977 |
| Jian Kang | jkan0240 | 490582066 |
| Yanhao Xu | yaxu5503 | 490147935 |


## Setup 

### if you have already had virtualenv, please skip to step 3 ###


1.  Install `virtualenv` to create virtual environment

   > `pip3 install virtualenv`


2. Create Virtual Environment

   > `python3 -m venv venv`


3. Activate the Virtual Environment

   > `source venv/bin/activate`


4. Install the Dependencies

   > `pip3 install -r requirement.txt`


## How To Run? 

1. Activate the Virtual Environment

   > `source venv/bin/activate`


3. Run the server

    > `python3 manage.py runserver`


5. The server

    > `http://127.0.0.1:8000/...`


## How to Quit?

1. Quit the server

   > `Ctrl C`

2. Deactive the virtual environment

   > `deactive`


## Database

| DBMS | DB Type | Role |
| ---- | ---- | ---- |
| MySQL | Tencent Cloud database instacne | Main |
| Redis | AWS Cloud Redis instance | Cache |


## How to change the database configuration?

Check `goal_project/settings.py`

with reference to https://docs.djangoproject.com/en/3.2/ref/settings/#databases

## How To Sign Up User Account without a valid USYD student unikey?
User can sign up, by entering his or her unikey as the username, and the system will send a verification code via email, the sign up process would not proceed, until a correct verification code is entered.

In order to prevent malicious users who are not USYD students from signing up for an active account, the registration process will send the verification code to the university account generated by the system based on the username. For example, if the username you are signing up is test1234, then the verification code will be sent to the email “test1234@uni.sydney.edu.au”

For marking and testing purpose, in case users might not have the university student email in the required format, 
sample accounts are provided:

  | User Type | Username | Password |
  | ---- | ---- | ---- |
  | Standard User | timi1234 | 1234 |
  | Admin | bwan3675 | bwan3675 |
