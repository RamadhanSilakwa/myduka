


 # #!/usr/bin/env python
# #
# # Small script to show PostgreSQL and Pyscopg together
# #

# # import psycopg2

# # try:
# #     conn = psycopg2.connect("dbname='myduka_db' user='postgres' host='localhost' password='Tony41943318' 'portid=5432'")
# # except:
# #     print("I am unable to connect to the database")

# # cur= conn.cursor()
# # cur.execute('''INSERT INTO public.products(
# # 	id, name, buying_price, selling_price, stock_quantity)
# # 	VALUES (6, 'chocolate', 100, 150,50);''')
# # conn.commit
# # rows=cur.fetchall()
# # print(rows)
import psycopg2





conn = psycopg2.connect(
    host = "localhost",
    dbname ="myduka_db" ,
    user = 'postgres',
    password = "SILAKWA21",
    port = 5432
)
cur = conn.cursor()

def check_email(email,password):
    query="""SELECT id, name
	FROM public."Users" WHERE email=%s AND password =%s"""
    cur.execute(query,(email,password))
    result=cur.fetchone()
    if result is not None:
        id=result[0]
        name=result[1]
        return id,name
    else: 
        return None
    
    
def create_user(full_name,email,password):
    cursor=conn.cursor()
    insert_query= "INSERT INTO users (full_name, email, password) VALUES(%s, %s, %s)"
    conn.commit()

def calculate_sales():
    cursor=conn.cursor()
    sales_query="""SELECT products.name,SUM(sales.quantity) AS total_sales
    FROM sales
    JOIN products ON products.id=sales.product_id
    GROUP BY products.product_name;"""
    cursor.execute(sales_query)
    list_sales=cursor.fetchall()
    return list_sales
# insert_script=('''INSERT INTO products(
# 	id, name, buying_price, selling_price, stock_quantity)
# 	VALUES (4,'potato chips', 170, 240,50);''')

# cur.execute(insert_script)
    
    


# """cur.execute("select products.name,sales.quantity,sales.created_at from products join sales on products.id=sales.pid;")
# for records in cur.fetchall():
#     print(records)""