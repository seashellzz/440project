from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)

app.secret_key = '23SummerComp440'

# mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Comp440'

mysql = MySQL(app)


# 127.0.0.1:5000/home
# home is where a user is rediected after they have succesfully logged in, will ultimately make this store and add a logged_in checker
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html',title="Home")


# 127.0.0.1:5000/register
# register allows a new user to write and save their credentials to the users table, we also check for duplicate username and email, and then check if the passwords match. After they successfuly create record, they are redirected to /home
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstName' in request.form and 'lastName' in request.form and 'pwmatch' in request.form:
        username = request.form['username']
        password = request.form['password']
        pwmatch = request.form['pwmatch']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        sql.execute( "SELECT * FROM users WHERE username LIKE %s", [username] )
        curr_username = sql.fetchone()      # pulling first record (ie. if username found, pulls that record, in none found, no records pulled)
        sql.execute( "SELECT * FROM users WHERE email LIKE %s", [email] )
        curr_email = sql.fetchone()
        if curr_username:
            print("Username already exists!")
            return redirect(url_for('register'))
        elif curr_email:
            print("Email already exists!")
            return redirect(url_for('register'))
        else:
            if password == pwmatch:
                sql.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s)', (username, email, password, firstName, lastName))
                mysql.connection.commit()
                session['username'] = username 
                print("You have successfully registered!")
                return redirect(url_for('store'))
            else:
                print("Passwords do not match!")

    elif request.method == 'POST':
        print("Need to fill out the form!")
    return render_template('register.html',title="Register")


# 127.0.0.1:5000/login
# login allows a previously registered user to login. It finds the matching credentials in the db, if found, logged in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))

        curr_user = sql.fetchone() # if credentials match -> pulls that record
        if curr_user: # ff user exists in accounts table in out database
            session['username'] = curr_user['username'] 
            print("You have been logged in!")
            return redirect(url_for('store'))
        else:
            print("Incorrect username/password!")
    return render_template('login.html',title="Login")


@app.route('/item-store', methods=['GET', 'POST'])
def store():
    if request.method == 'POST' and 'title' in request.form and 'description' in request.form and 'price' in request.form and 'cat1' in request.form and'cat2' in request.form and 'cat3' in request.form:
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        cat1 = request.form['cat1']
        cat2 = request.form['cat2']
        cat3 = request.form['cat3']
        post_date = datetime.now().strftime('%Y-%m-%d') # grabbing current date

        username = session.get('username') # saving username to store in db later

        if username: # checking is user has submitted 3 items
            sql = mysql.connection.cursor()
            sql.execute('SELECT COUNT(*) FROM items WHERE post_date = %s AND username = %s', (post_date, username))
            count = sql.fetchone()[0]

            if count >= 3: 
                print('You can only post 3 items a day.', 'error')
                return redirect(url_for('store'))

            sql.execute('INSERT INTO items (title, description, post_date, price, username) VALUES (%s, %s, %s, %s, %s)', (title, description, post_date, price, username))
            mysql.connection.commit()

            sql.execute('SELECT LAST_INSERT_ID()') # pulling last auto-incremented value (will always be item just inserted)
            item_id = sql.fetchone()[0]

            if cat1 == "":
                print('Need at least 1 category (fill left to right)')
                return redirect(url_for('store'))

            if cat1 != "" and cat2 == "" and cat3 == "":
                sql.execute('INSERT INTO item_categories (item_id, category_name) VALUES (%s, %s)', (item_id, cat1))
            if cat1 != "" and cat2 != "" and cat3 == "":
                sql.execute('INSERT INTO item_categories (item_id, category_name) VALUES (%s, %s)', (item_id, cat1))
                sql.execute('INSERT INTO item_categories (item_id, category_name) VALUES (%s, %s)', (item_id, cat2))
            if cat1 != "" and cat2 != "" and cat3 != "":  
                sql.execute('INSERT INTO item_categories (item_id, category_name) VALUES (%s, %s)', (item_id, cat1))
                sql.execute('INSERT INTO item_categories (item_id, category_name) VALUES (%s, %s)', (item_id, cat2))
                sql.execute('INSERT INTO item_categories (item_id, category_name) VALUES (%s, %s)', (item_id, cat3))
            mysql.connection.commit()

            print('Item added successfully!', 'success')
        else:
            print('You need to log in first.', 'error')
            return redirect(url_for('login'))

    elif request.method == 'POST':
        print('Please fill out the form completely, with at least 1 category :)', 'error')

    return render_template('store.html', title="Store")


@app.route('/item-search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST' and 'category_name' in request.form:
        category_name = request.form['category_name']

        sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql.execute('SELECT * FROM items WHERE item_id IN (SELECT item_id FROM item_categories WHERE category_name = %s)', [category_name])
        search_results = sql.fetchall()

        return render_template('category_search.html', title="Search Results", results=search_results)

    return render_template('category_search.html', title="Search")


@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    if request.method == 'POST' and 'rating' in request.form and 'description' in request.form:
        rating = request.form['rating']
        description = request.form['description']
        username = session.get('username')
        review_date = datetime.now().strftime('%Y-%m-%d') # grabbing current date

        sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql.execute('SELECT * FROM items WHERE item_id = %s', (item_id,))
        item = sql.fetchone()
        sql.execute('SELECT COUNT(*) FROM reviews WHERE username = %s AND review_date = %s', (username, review_date))
        count = sql.fetchone()['COUNT(*)']

        if item['username'] == username:
            print('You cannot review your own item.')
            return redirect(url_for('item_details', item_id=item_id))
        elif count >= 3:
            print('You have already submitted 3 reviews today.')
            return redirect(url_for('item_details', item_id=item_id))
        else:
            sql = mysql.connection.cursor()
            sql.execute('INSERT INTO reviews (item_id, username, rating, description, review_date) VALUES (%s, %s, %s, %s, %s)',
                        (item_id, username, rating, description, review_date))
            mysql.connection.commit()
            
            print('Review submitted successfully!')
            return redirect(url_for('item_details', item_id=item_id))
    
    # Fetch item details and reviews from the database
    sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql.execute('SELECT * FROM items WHERE item_id = %s', (item_id,))
    item = sql.fetchone()
    
    sql.execute('SELECT * FROM reviews WHERE item_id = %s', (item_id,))
    reviews = sql.fetchall()
    
    return render_template('item_details.html', item=item, reviews=reviews)

#returns empty set, although it exists in database, unsure why, chatgpt unhelpful
@app.route('/user-search', methods=['GET', 'POST'])
def user_search():
    if request.method == 'POST' and 'user_name' in request.form:
        username = request.form['user_name']

        sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql.execute('SELECT items.username AS item_username, items.item_id, items.title, reviews.rating FROM items, reviews WHERE (items.item_id = reviews.item_id AND (rating = "Excellent" OR rating = "Good")) AND items.username = %s', [username])
        search_results = sql.fetchall()
        return render_template('user_search.html', title="Search Results", results=search_results)

    return render_template('user_search.html', title="User Reviews")
    

@app.route('/most-expensive', methods=['GET'])
def most_expensive_items():
    sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    sql.execute('''SELECT items.*, item_categories.category_name
                    FROM items
                    JOIN item_categories ON items.item_id = item_categories.item_id
                    WHERE (item_categories.category_name, items.price) IN
                        (SELECT item_categories.category_name, MAX(items.price)
                         FROM items
                         JOIN item_categories ON items.item_id = item_categories.item_id
                         GROUP BY item_categories.category_name)
                    ORDER BY item_categories.category_name;''')
                  
    results = sql.fetchall()

    return render_template('most_expensive_items.html', title="Most Expensive Items", results=results)

@app.route('/positive-users', methods=['GET'])
def positive_users():
    sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    sql.execute("SELECT DISTINCT items.username FROM items, reviews WHERE NOT (rating = 'poor') ")

    search_results = sql.fetchall()
    return render_template('positive_users.html', title="Search Results", results=search_results)

@app.route('/negative-reviewers', methods =['GET'])
def negative_reviewers():
    sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    sql.execute("SELECT DISTINCT username FROM reviews WHERE NOT (rating ='Excellent' or rating = 'Fair' or Rating = 'Good')")

    search_results = sql.fetchall()
    return render_template('negative_reviewers.html', title="Search Results", results=search_results)

@app.route('/max-items', methods = ['GET'])
def max_items():
    sql = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    sql.execute("SELECT username FROM items WHERE post_date = '2023-07-26'")
    
    result1 = sql.fetchall()

    if result1 is None:
        print("There is no items being posted in 7/26/2023")
    
    else:
        sql.execute(''' SELECT username, COUNT(*) AS posted_items_count 
                    FROM items
                    WHERE post_date = '2023-07-26'
                    GROUP BY username
                    ORDER BY posted_items_count DESC;''')
        result2 = sql.fetchall()

    return render_template('max_items.html', title = "Max Items", result2=result2)

if __name__ =='__main__':
	app.run(debug=True)
