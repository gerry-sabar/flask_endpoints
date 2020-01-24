Installation:
1. clone the project
2. inside root project directory: python3 -m venv venv
   - if you got error because not installed python3 venv yet, please install python3 venv & remove prevously created venv directory then repeat the step
3. run the virtual environment using command . venv/bin/activate
4. install mysql & phpmyadmin
   - apt install mysql-server
   - mysql_secure_installation
5. adjust database connection at app.py line 11 and create a database named endpoints
6. pip install -r requirements.txt
   - if you get error: mysql_config not found do this: 
     1. apt install build-essential
     2. apt install python3-dev 
     3. apt install default-libmysqlclient-dev
   - if you get error "cannot find -lssl; cannot find -lcrypto"
     1. apt install libssl-dev 
   - run pip again
7. remove migrations folder: rm -rf migrations
8. flask db init
9. flask db upgrade
10. flask db migrate
11. to create seeder, execute: flask seeder 
12. to run the app: source activate.sh


VPS Deployment Ubuntu with Nginx:

1. Complete the installation step first & make sure you aren't in virtual envionrment mode.
2. Reference: https://medium.com/@gerrysabar/deploy-a-flask-application-to-ubuntu-18-04-server-69b414b10881 follow until install pip3 & then install gunicorn3
3. inside root project: pip3 install -r requirements.txt 
4. after intalling all dependencies: gunicorn3 wsgi:application