# gmail_rule_engine
Python intergration with Gmail API to perform some rule based operations on emails.

## DB design


A simple single table is enough to store the fetched mails from Gmail API services.

![Screenshot 2024-08-25 at 4 24 17 PM](https://github.com/user-attachments/assets/23d87751-c08a-41c9-b3bb-11d71f516f89)

## Code

Two scripts were written for two functionalities.
- First script to authenticate with Gmail API services and fetch emails from Gmail.
- Second script to generate rule actions that needs to be applied on stored emails and then apply the actions for filtered emails.

Code respository is defined in the below structure ,

- dockerfiles
- src
  - config
  - dao
  - entity
  - manager
  - script

## Setup

1. Create a python virtual environment (venv) and install the required packages mentioned in the requirements.txt file.
    ```{console}
   python -m venv venv
   source venv/bin/activate && pip install -r requirements.txt
   ```
2. Setup the python path
    ```{console}
   export PYTHONPATH=$PYTHONPATH:./
   ```
3. Setup and run the database server in the local. MySql engine is hosted in this implementation using docker compose.
    ```{console}
   docker-compose -f <path_to_docker_file> up -d 
   ```
3. Execute the below scripts to simulate the rule engine flow.
    ```{console}
    python3 src/scripts/mail_data_loader.py --flush True --limit 10
    ```
    ```{console}
    python3 src/scripts/operations_executor.py --json <path/to/jsonfile/>
    ```

## Author

- [Sharath Bhadrinath](https://github.com/iamLUCISTAR)
