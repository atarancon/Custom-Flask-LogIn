from myproject import app,db
from flask import render_template,redirect,request,url_for,flash,abort
from flask_login import login_user,login_required,logout_user 

from myproject.models import User 
from myproject.forms import LoginForm,RegistrationForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():
     
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
        #grab user based on email 
            user = User.query.filter_by(email=form.email.data).first()

        #check if correct password and user found in table
            if user  is not None and user.check_password(form.password.data):   
                login_user(user)

                flash("logged in Successfully")

                #figure out if user was somewhere else 

                next = request.args.get('next')


                #user wasn;t redirected to login  
                if next == None or not next[0] ==  '/':
                    next = url_for('welcome_user')

                #user was redirected 
                
                return redirect(next)

     
        error = "Incorrect Email and/or Password !!"
        return render_template("login.html" , form = form , error = error)
   
    return render_template("login.html" , form = form , error = error)

@app.route('/register' , methods = ['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data , username=form.username.data , password = form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering !")
        return redirect(url_for('login'))
    
    return render_template("register.html",form=form)


if __name__ == "__main__":
    app.run(debug=True)