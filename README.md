## Group participation breakdown:

- Grant Freedman: Added the item, item_categories, and reviews tables with there respective parameters, created the methods for the add-item, category-search, and item-review pages, and created the html pages for each. Made sure full functionalioty was met with each

- Hannah Xie: editing tables in sql and review page for the html

- Samuel Hernandez: Worked with group members to add new tables and columns for database management. Created dropdown selections in html for inserting user reviews to database.

## Phase 1 Demo Link:
- https://youtu.be/w2jzU8lqBWo
## Phase 2 Demo Link:
- https://youtu.be/Yy94vQRTVt0


## Docker run (need to modify to your path to 440db_project)
```
docker run -it -p 5000:5000 -v /Users/gfreedman/Desktop/440db_project:/440db_project ubuntu:22.04 bash
```

## When inside container terminal, run commands, access server through '127.0.0.1:5000':
```
apt-get update
apt-get install -y git nano
apt install -y mysql-server
cd 440db_project
apt-get install -y python3 python3-dev python3.10-venv python3-pip libmysqlclient-dev pkg-config gcc-aarch64-linux-gnu
python3 -m venv venv
. venv/bin/activate
pip3 install --upgrade wheel
pip install -r requirements.txt
service mysql start
***NEED TO SEED DB:
	mysql -> all create tables in .sql file
chmod 777 run
./run
```

## When you make a code change
```
ctrl+c
cd 440db_project
. venv/bin/activate
service mysql start
./run
```

## If want to see tables in database:
for users:
```
mysql -h localhost -e "use Comp440; select * from users;"
```
for other...
