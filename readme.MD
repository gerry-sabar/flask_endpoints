Installation:
1. clone the project
2. inside root project directory: python3 -m venv venv
3. run the virtual environment using command . venv/bin/activate
4. install mysql & phpmyadmin
5. adjust database connection at app.py line 11 and create a database named endpoints
6. pip install -r requirements.txt
   - if you get error: mysql_config not found do this: 
     1. apt-get install build-essential
     2. apt-get install python3-dev 
     3. apt install default-libmysqlclient-dev
   - run pip again
7. remove migrations folder
8. flask db init
9. flask db upgrade
10. flask db migrate
11. to create seeder, execute: flask seeder 
12. to run the app: source activate.sh