from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
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
    low=rank-200
    high=rank+200
    cur=mysql.connection.cursor()
    if (gender=="Male"):
        male="Gender-Neutral"
        cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s AND Gender = %s ORDER BY Closing_rank ASC",(rank,category,male))
    else:
        cur.execute(f"SELECT * FROM jee_adv WHERE closing_rank > %s AND seat_type = %s ORDER BY Closing_rank ASC",(rank,category,))

    fetchdata=cur.fetchall()
    cur.close()
    return fetchdata





@app.route('/',methods=["POST","GET"])
def hello_world():
    
    
    return render_template('index.html')


# def get_data():
#     engine = create_engine('mysql://root:@localhost/college_predictor')
#     with engine.connect() as conn:
#         data = conn.execute(f"SELECT * FROM `demo`")
#     # data = engine.execute('SELECT * FROM `demo`')
#     return data




@app.route('/result',methods=["POST","GET"])
def result():
    if request.method=="POST":
        print("this is a post method")
        u_name=request.form.get('name')
        rank=int(request.form.get('rank'))
        category=request.form.get('category')
        gender=request.form.get('gender')
        print(u_name,rank,category,gender)
        fetchdata = get_result(rank,category,gender)
    
    # with engine.connect() as conn:
    #     result = conn.execute(stmt)
    # query=db.engine.execute("SELECT * FROM `demo`")
    # us=Demo.query.filter_by(id=1)
    # print(us)
    # query=get_data()
    


    return render_template('result.html',query=fetchdata)

app.run(debug=True)