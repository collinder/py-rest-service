# About
Job test project to: 
1. Set up postgresql database.
2. Populate it with some tables and records.
3. Launch python service, which lets us grab records from database. 

Terminal promts is for Arch Linux. 
If you have another Linux distribution, feel free to google 'how to install pip', 'how to install with pip' and 'how to install postgresql' for your distribution!

# 1. Set up postgresql database.
## Install
```bash
sudo pacman -S postgresql
```

## Init db
```bash
sudo su - postgres
initdb --locale en_US.UTF-8 -D /var/lib/postgres/data
exit```

## Start postgresql and check if it is running
```bash
sudo systemctl start postgresql
```

```bash
sudo systemctl status postgresql 
```
* check if service is actually running

## Create user and database, grant privileges

```bash
sudo -u postgres psql
```

```PLSQL
CREATE USER uno WITH ENCRYPTED PASSWORD '8.B(P8pDQeMH!';
CREATE DATABASE prueba;
GRANT ALL PRIVILEGES ON DATABASE prueba TO uno;
\c prueba postgres
GRANT ALL PRIVILEGES ON SCHEMA public TO uno;
\q
```
**do not configure your db for remote access if you exposed your password somewhere!**

* restart postgresql
```bash
sudo systemctl restart postgresql
```
* connect to postgresql
```bash
psql -h localhost -d prueba -U uno -p 5432
\q
```
# 2. Populate it with some tables and records.
## install pip, Flask and psycopg
```bash
sudo pacman -S python-pip
python -m pip install --break-system-packages psycopg2
python -m pip install --break-system-packages psycopg
python -m pip install --break-system-packages flask
python -m pip install --break-system-packages jsonify
```
## create schema, tables and populate tables with good books
```bash
git clone '<адрес этого гит проекта>' ~/sencillo
cd ~/sencillo
python serv.py init
```
* CTRL - C
# 3. Launch python service, which lets us grab records from database. 
## launch service
```bash
cd ~/sencillo
python serv.py
```
## check how it is working
0. Open your browser
1. Go to http://127.0.0.1:5000/ - can you see all authors in json format?
2. Go to http://127.0.0.1:5000/3 - can you see all books of that author?
