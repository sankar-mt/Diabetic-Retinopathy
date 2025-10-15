from flask import jsonify,Flask,url_for,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_login import LoginManager, UserMixin , login_user ,logout_user, login_required
import base64
import json
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail,Message
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import current_user
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
app.secret_key= "wutyeihdhhasbnk"
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)


def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

def send_reset_email(user):
    token = get_reset_token(user)
    msg = Message('Password Reset Request',
                  sender='innovationlabpsg@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    user = User.query.filter_by(email='innovationlabpsg@gmail.com').first()
    send_reset_email(user)
    
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect('/login')
    

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
            user_id = s.loads(token)['user_id']
    except:
            user = None
    user = User.query.get(user_id)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/')
    else:
      return redirect(url_for('forgot',user=user.id))
@app.route('/resetform/<user>')
def resetform(user):
    return render_template('forgot_password.html',user=user)

@app.route('/resetpass/<user>',methods=['POST'])
def resetpass(user):
     hashed_password = generate_password_hash(request.form['password'])
     user_change=User.query.filter_by(id=user).first()
     user_change.password_hash = hashed_password
     db.session.commit()
     flash('Your password has been updated! You are now able to log in', 'success')
     return redirect('/')

class User(UserMixin,db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    password_hash = db.Column(db.String(30))
    username = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(255),nullable=False,unique=True)

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

def set_password(self,password):
    self.password_hash =generate_password_hash(password)

def check_password(self,password):
    return check_password_hash(self.password_hash,password)


class Patient(db.Model):
 __tablename__= "Patients"        
 id =db.Column(db.Integer,primary_key=True)
 mail =  db.Column(db.String)
 name =  db.Column(db.String)
 image =db.Column(db.LargeBinary)
 Result =db.Column(db.Integer)
 def __init__(self,name,image,mail,Result):
  self.image = image
  self.mail = mail
  self.Result= Result
  self.name = name

@app.route('/home')
@login_required
def home():
    return render_template('index.html')
    
@app.route('/Patient')
@login_required
def patient():
   patient =  Patient.query.all()
   
   image={}
   for x in Patient.query.all():
       dat = base64.b64encode(x.image)
       image[x.id] = dat.decode("UTF-8")
   return render_template('PatientHistory.html',patient = patient,image=image)
    
@app.route('/')
def login():
    return render_template('login.html')
    
@app.route('/profile')
@login_required
def profile():
    return render_template('/user_profile.html')
    
@app.route('/forgotpass')
def forgot(user):
    return render_template('forgot_password.html',user=user)
    
@app.route('/predict')
@login_required
def predict():
    return render_template('Predict.html')

@app.route('/', methods=['POST'])    
def login_post():
    if request.method == 'POST':
     pwd = request.form['password']
     user1 = User.query.all()
     for user in user1: 
      if(check_password(user,pwd)):
       login_user(user)
       db.session.commit()
       return redirect(url_for('home')); 
     flash("Invalid Credentials")
     return redirect(url_for("login"))

@app.route('/logout')
@login_required
def logout():
      logout_user()
      flash("Logged out")
      return render_template("login.html") 

@app.route('/submit',methods = ['POST'])
@login_required
def pred_submit():
 if request.method == 'POST':  

    import tensorflow as tf
    from PIL import Image
    import numpy as np
    CheckImage = request.files['input']
    name = request.form['name']
    mail = request.form['email']
    import os
    CheckImage.save(os.path.join("C://Users/Sanka/Downloads","image.png"))
    img = keras.preprocessing.image.load_img('C://Users/Sanka/Downloads/image.png',color_mode="grayscale", target_size=(256,256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)    
    print(predictions)
    for i in range(0,5):
        if(predictions[0][i]==np.max(predictions)):
            className = i
    
    confidence = 100 * np.max(predictions)
    Result =  className
    ImgMain= CheckImage.read()
    data= Patient(name,ImgMain,mail,Result)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for("patient"))


if __name__ == "__main__":
    from tensorflow import keras
    model = keras.models.load_model('Retino_CNN/templates/admin/main/source/static/Model/Model')
    app.run()    