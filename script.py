from flask import Flask,render_template,request
from flask_pymongo import PyMongo
import datetime

app=Flask(__name__)


app.config["MONGO_DBNAME"]="user_data"
app.config["MONGO_URI"]="mongodb://admin:admin123@ds145184.mlab.com:45184/user_data"
mongo=PyMongo(app)


@app.route('/')
def index():
	user=mongo.db.user_data
	users=""
	for document in mongo.db.user_data.find():
		print(document['name']+'\n')
		if document['name'] not in users:
			users+=document['name']+','
	users=users.split(',')
	users.pop()
	return render_template('welcome.html',users=users)

@app.route('/',methods=['POST'])
def list():
	conn=mongo.db.user_data

	real_name=request.form['name']
	name=real_name
	name=name.split(' ')
	name=name[0].upper()
	mail=request.form['mail']
	data=request.form['data']
	conn.insert({"name":name,"email":mail,"shop_list":data,"datetime":datetime.datetime.now()})
	shopping_list=data.split(',')
	return render_template('show_list.html',name=name,mail=mail,date=datetime.datetime.now(),shopping_list=shopping_list)


@app.route('/search')
def search():
	return render_template('search.html')

@app.route('/search',methods=['POST'])
def search_post():
	user=mongo.db.user_data
	
	check=user.find_one({'email':request.form['email']})
	if check is None:
		return render_template('oops.html')
	else:
		return render_template('search.html',name=check['name'],mail=check['email'],datetime=check['datetime'],shopping_list=check['shop_list'].split(','))


if __name__=="__main__":
	app.run(debug=True)



