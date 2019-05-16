import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug import secure_filename
from xml.etree import ElementTree as ET
import xmltodict



app = Flask(__name__)
db = SQLAlchemy(app)


app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
UPLOAD_FOLDER = '/home/narendra/narendra/myrepository/ectproject/data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'xml', 'jpeg'])

login = LoginManager(app)

from app.models import User, Order, Organization, Clerk, Customer


@app.route('/home')
def home():
	return render_template("home.html")


@app.route('/upload')
def upload():
	return render_template('upload.html')

def allowed_file(filename):
	return '.' in filename and \
	        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
	if request.method == "POST":
		file = request.files['file']
		if file.filename == '':
			flash('No file selected')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('parse_xml',filename=filename))



@app.route('/parse/<filename>')
def parse_xml(filename):
	Order_file = '/home/narendra/narendra/myrepository/ectproject/data/' + filename
	
	dom = ET.parse(Order_file)
	
	data = dom.getroot()
	with open(Order_file) as fd:
		doc = xmltodict.parse(fd.read())	
	
	date = data.find('Date').text

	Time = data.find('Time').text

	# dateTime = date+" "+Time
	# print(dateTime)
	dateTime = '2004-10-19 10:23:54'
	tableNumber = data.find('TableNo').text
	clerkId = data.find('ClerkNo').text
	customerId = doc['Order']['Customer']['CustomerID']
	consecutiveNumber = data.find('ConsecutiveNo').text
	cover = data.find('Cover').text
	status = data.find('Status').text
	mode = data.find('Mode').text
	clerkName = data.find('ClerkName').text
	print('clerkNameoooooooooooo', clerkName)
		
	
	# print('date_time:{}  table_number:{} clerk_id:{} customer_id:{} consecutive_umber:{} cover:{} status:{} mode:{}'.format(
	# 	            dateTime, tableNumber, clerkId, customerId, consecutiveNumber,cover, status, mode
	
	# 	            ))
	try:
		result = Order(
			date_time=dateTime,
			table_number=tableNumber,
			clerk_id=clerkId,
			customer_id=customerId,
			consecutive_number=consecutiveNumber,
			cover=cover,
			status=status,
			mode=mode
		)

		# clerkdetail = Clerk(
		# 	name=clerkName
		# 	)
		db.session.add(result)
		# db.session.add(clerkdetail)
		db.session.commit()
		return redirect(url_for("admin.base"))
	except:
		return("Unable to add item to database.")



from app.mod_admin.controllers import mod_admin as admin_module


app.register_blueprint(admin_module)