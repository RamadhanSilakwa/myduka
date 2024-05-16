from flask import redirect,url_for,Flask,render_template,redirect,request,flash
import psycopg2
from mydb import *
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user

# other imports as necessary




conn = psycopg2.connect(
    host = "localhost",
    dbname ="myduka_db" ,
    user = 'postgres',
    password = "SILAKWA21",
    port = 5432
)
cur = conn.cursor()
app=Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
# login_manager = LoginManager(app)



app.secret_key="ramah"
# def load_user(user_id):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#     user = cursor.fetchone()
#     cursor.close()
#     return user
login_manager = LoginManager(app)
login_manager.login_view='login'

# @login_manager.user_loader
# def load_user(user_id):
#     return load_user (user_id)





 
class User(UserMixin):
    def __init__(self, user_id,email,password):
        self.id = user_id
        self.email=email
        self.password=password

@login_manager.user_loader
def load_user(id):
    cur.execute('''SELECT id, name, email, password
	FROM public."Users"
	where id= %s; ''',(id,))
    user_data = cur.fetchone()

    if user_data:
        # Create a User object based on the database data
        user = User(user_data[0], user_data[1], user_data[2])
        return user

    return None  # Return None if the user is not found



@app.route("/")
def hello():
    return render_template("index.html")
@app.route("/home")
def home():
    return render_template("index.html")
@app.route("/products")
def products():
    cur.execute('select * from products')
    prods=cur.fetchall()
    return render_template('products.html',prods=prods)
    # return "prod"

@app.route("/sales")
def sales():
    cur.execute('select * from sales')
    sale=cur.fetchall()
    cur.execute('select * from products')
    prods=cur.fetchall()

    return render_template('sales.html',sale=sale,prods=prods)


@app.route("/add sales", methods=["post"])
def addsales():
    pid=request.form['pid']
    quantity=request.form['quantity']
    value=(pid,quantity)
    insert_sale="""INSERT INTO sales(
	 pid, quantity, created_at)
	VALUES ( %s, %s,now());"""
    cur.execute(insert_sale,value)
    conn.commit()
    return redirect("/sales")


@app.route("/add-p", methods=["post"])
def add_products():
    product_name=request.form['name']
    buyingprice=request.form['bp']
    sellingprice=request.form['sp']
    quant=request.form['sq']
    values=(product_name,buyingprice,sellingprice,quant)
    insert_query="INSERT INTO products(name, buying_price, selling_price, stock_quantity)VALUES ( %s, %s, %s, %s);"
    cur.execute(insert_query,values)
    # conn.commit()
    flash('product is added')
    return redirect("/products")

   

# @app.route("/register", methods=["POST", "GET"])
# def register():
#     if request.method == 'POST':
#         # Extracting data from the form
        
#         email = request.form["email"]
#         password = request.form["password"]

#         # Values to be inserted into the database
#         values = ( email, password)


#         # SQL query for inserting user data
#         register_user = """INSERT INTO public."Users"(
# 	                    name, email, password)
# 	                    VALUES ( %s, %s, %s);"""

#         # Execute the query and commit changes to the database
#         cur.execute(register_user, values)
#         conn.commit()

#     return render_template('register.html')
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        # Extracting data from the form
        name=request.form['name']
        email = request.form["email"]
        password = request.form["password"]

        # Values to be inserted into the database
        values = (name, email, password)


        # SQL query for inserting user data
        register_user =''' INSERT INTO public."Users"(
	     name, email, password)
	     VALUES ( %s, %s, %s);'''

        # Execute the query and commit changes to the database
        cur.execute(register_user, values)
        conn.commit()
    return render_template('register.html')

@app.route("/login",methods= ["POST","GET"])

def login():
       if request.method == 'POST':
          email=request.form['email']
          password=request.form['password']
          user_data=check_email(email,password)
          if user_data:
            user=load_user(user_data[0])
            login_user(user)
            flash("login successfull", 'success')
            return redirect('/dashboard')
          else:
            flash("invalid email or password", 'danger')
            return redirect('/login') 
       return render_template('login.html')

     

#  cur.execute("SELECT * FROM users WHERE email = %s AND passwords = %s", (email, password))
#         user_data = cur.fetchone()
#         if user_data:
#             user = load_user(user_data[0])
#             login_user(user)
#             flash("You are successfully logged in", 'success')
#             return redirect('/dashboard')
#         else:
#             flash("Invalid email or password", 'danger')
#             return redirect('/login')


# @app.route ('/me')
# def dashboard():
#     return render_template('me.html')


# @app.route('/dashboard')
# def dashboard():
#     cursor=conn.cursor()
#     sales_query="""SELECT products.name,SUM(sales.quantity) AS total_sales
#     FROM sales
#     JOIN products ON products.id=sales.pid
#     GROUP BY products.name;"""
#     cursor.execute(sales_query)
#     list_sales=cursor.fetchall()
#     productss=[]
#     tts=[]
#     for i in list_sales:
#         productss.append(str(i[0]))
#         tts.append(str(i[1]))
#     return render_template("dashboard.html",productss=productss,tts=tts)

# @app.route('/login',methods=['POST','GET'])
# def login():
#     if request.method== 'POST':
#         email=request.form['email']
#         password=request.form['password']
#         user=check_email(email,password)
#         if user:
#             return redirect('/dashboard')
#         else:
#             return redirect('/register')
#     return render_template('login.html')


# @app.route("/login" ,methods=["POST","GET"])
# def login():
#     if request.method == 'POST':
#         email=request.form['email']
#         password=request.form['password']
#         user=check_email(email,password)
#         if user:
#             return redirect('/dashboard')
#         else:
#             return redirect('/register')
#     return render_template("login.html")
@app.route('/dashboard')
# @login_required          
def dashboard():
    
    cursor=conn.cursor()
    sales_query="""SELECT products.name,SUM(sales.quantity) AS total_sales
    FROM sales
    JOIN products ON products.id=sales.pid
    GROUP BY products.name;"""
    cursor.execute(sales_query)
    list_sales=cursor.fetchall()
    productss=[]
    tts=[]
    for i in list_sales:
        productss.append(str(i[0]))
        tts.append(str(i[1]))

    return render_template("dashboard.html",productss=productss,tts=tts)
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/home")



# conn.commit()



app.run(debug=True)