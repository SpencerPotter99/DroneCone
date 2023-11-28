# DroneCones - Online Ice Cream Delivery App

## Installation

[**Python 3.8 or higher is required**](https://www.python.org/)

### To install and run locally:

1. Clone the project:
    ```shell
    git clone https://github.com/SpencerPotter99/DroneCone
    ```

2. Change directory:
    ```shell
    cd DroneCone
    ```

3. Create a virtual environment with venv called **venv**:
    - Windows
      ```shell
      py -m venv .venv
      ```
    
    - Linux/macOS
      ```shell
      python3 -m venv .venv
      ```

4. Activate the virtual environment:
    - Windows 
      ```shell
      .\.venv\Scripts\activate
      ```
    
    - Windows **(Git-Bash)**
      ```shell
      source ./.venv/Scripts/activate
      ```
    
    - Linux/macOS
      ```shell
      source ./.venv/bin/activate
      ```
    
    - **Note:** To exit the virtual environment, type
      ```shell
      deactivate
      ```

5. Install dependencies:
    > **_NOTE:_** For Windows, when you activate the virtual environment, 
    It will add an executable of python and pip from your virtual environment to your terminal path despite your os.
    So for Windows, you don't want to use py, since py might point to your global installation of python.

    ```shell
    pip install -r requirements.txt
    ```

6. Migrate & Runserver:
    ```shell
    python DroneCone/manage.py migrate
    python DroneCone/manage.py runserver
    ```

7. Finally, go to the locally hosted [**website**](http://127.0.0.1:8000/):
    ```html
    http://127.0.0.1:8000/
    ```

## Creating a User

- To create a **normal user account**, just go to the Sign-Up page while the server is running and fill out the form.

- To create a **superuser account**, use this command:
    ```shell
    python DroneCone/manage.py createsuperuser
    ```

## Seeding with Dummy Data

- To seed the database with dummy data use this command:
    ```shell
    python DroneCone/manage.py loaddata DroneCone/fixtures/seed_db
    ```

- Logging in as one of the dummy users
    - **Superuser**
        - Username
          ```text
          admin007
          ```
        - Password
          ```text
          Secr3t#789
          ```
    
    - **Normal user**
        - Username
          ```text
          chocoFan
          ```
        - Password
          ```text
          Ch0c0L@te!
          ```

> **_Note:_** Optionally, you can log in as a normal user on Chrome and as a superuser on firefox,
and see how the site behaves for different users