from flask import Flask,render_template,request,redirect
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
from flask_mysqldb import MySQL

# My db connection
# local_server = True
# app = Flask(__name__)
# app.secret_key='manthan'

# # app.config['SQLALCHEMY_DATABASE_URL'] ='mysql://username:password@localhost/satabase_name'

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/college_predictor'
# db=SQLAlchemy(app)

# Create db model



app = Flask(__name__)

mysql=MySQL(app)

# app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
# app.config['MYSQL_USER'] = 'sql12616044'
# app.config['MYSQL_PASSWORD'] = '2NnaQKUvcW'
# app.config['MYSQL_DB'] = 'sql12616044'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'college_predictor'



# class User(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(50)) 
#     rank=db.Column(db.Integer )
#     gender=db.Column(db.String(50)) 
#     category=db.Column(db.String(50)) 


# class Demo(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     college_name=db.Column(db.String(50)) 
#     branch=db.Column(db.String(50))
#     cutoff=db.Column(db.Integer )


def get_result(rank, category ,gender ):
    # low=rank-200
    # high=rank+200
    cur=mysql.connection.cursor()
    if (gender=="Male"):
        male="Gender-Neutral"
        cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Gender = %s ORDER BY Closing_rank ASC",(rank,category,male))
    else:
        cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s ORDER BY Closing_rank ASC",(rank,category,))

    fetchdata=cur.fetchall()
    cur.close()

    cur=mysql.connection.cursor()
    cur.execute("SELECT DISTINCT Academic_Program FROM jee_adv")
    academic=cur.fetchall()
    cur.close()

    cur=mysql.connection.cursor()
    cur.execute("SELECT DISTINCT Institute FROM jee_adv")
    institute=cur.fetchall()
    cur.close()
    return fetchdata,academic,institute

def get_result_from_filters(rank, category ,gender,college,program ):
    # low=rank-200
    # high=rank+200
    cur=mysql.connection.cursor()
    if (gender=="Male"):
        male="Gender-Neutral"
        if (college and program):
            cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Gender = %s AND Institute = %s AND Academic_Program = %s ORDER BY Closing_rank ASC",(rank,category,male,college,program))
        elif(college):
            cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Gender = %s AND Institute = %s  ORDER BY Closing_rank ASC",(rank,category,male,college))
        elif(program):
            cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Gender = %s AND Academic_Program = %s ORDER BY Closing_rank ASC",(rank,category,male,program))
    else:
        if (college and program):
            cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Institute = %s AND Academic_Program = %s ORDER BY Closing_rank ASC",(rank,category,college,program))
        elif(college):
            cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Institute = %s  ORDER BY Closing_rank ASC",(rank,category,college))
        elif(program):
            cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Academic_Program = %s ORDER BY Closing_rank ASC",(rank,category,program))

    fetchdata=cur.fetchall()
    cur.close()

    cur=mysql.connection.cursor()
    cur.execute("SELECT DISTINCT Academic_Program FROM jee_adv")
    academic=cur.fetchall()
    cur.close()

    cur=mysql.connection.cursor()
    cur.execute("SELECT DISTINCT Institute FROM jee_adv")
    institute=cur.fetchall()
    cur.close()
    return fetchdata,academic,institute




@app.route('/',methods=["POST","GET"])
def hello_world():
    
    
    return render_template('index.html')


# def get_data():
#     engine = create_engine('mysql://root:@localhost/college_predictor')
#     with engine.connect() as conn:
#         data = conn.execute(f"SELECT * FROM `demo`")
#     # data = engine.execute('SELECT * FROM `demo`')
#     return data
class user_details():
    u_name="u_name"
    rank=0
    category="none"
    gender="none"

a=user_details()


@app.route('/result',methods=["POST","GET"])
def result():
    print("apply pressed")
    if request.method=="POST":
        print("this is a post method")
        a.u_name=request.form.get('name')
        a.rank=int(request.form.get('rank'))
        a.category=request.form.get('category')
        a.gender=request.form.get('gender') 
        print(a.u_name,a.rank,a.category,a.gender)
        fetchdata,academic,institute = get_result(a.rank,a.category,a.gender)
        return render_template('result.html',query=fetchdata,branch=academic,college=institute)
    if request.method=="GET":
        print("this is get method")
        college=str(request.args.get('college'))
        program=str(request.args.get('branch'))
        print(college,program)
        fetchdata,academic,institute = get_result_from_filters(a.rank,a.category,a.gender,college,program)
        return render_template('result.html',query=fetchdata,branch=academic,college=institute)

app.run(debug=True)