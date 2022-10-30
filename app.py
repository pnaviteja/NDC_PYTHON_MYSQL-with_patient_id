
from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL
from random import randint


app = Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'navi'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'teja'
 
mysql = MySQL(app)

def gb(fm):
    global firstname1
    firstname1=fm

@app.route('/', methods=['GET',"POST"])
def reg():
    return render_template('register.html')

@app.route('/register', methods=['GET',"POST"])
def register():
    
    firstname=" "
    lastname = " "
    gender = " "
    birthday = " "
    pin = " "
    score=" "
    remarks=""
    patient_id=" "
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        pin = request.form["pin"]
        gb(firstname)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT patient_id from navi')
        pid=cursor.fetchall()
    
        if(len(pid)>0):
            for i in pid:
                id=random_n_digits(14)
                if(id!=i):
                    cursor.execute(' INSERT INTO navi VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(firstname,lastname,gender,birthday,pin,score,remarks,id))

                    mysql.connection.commit()
                    msg='You have successfully registered !'
                    break
                else:
                    continue
                
    else:
        id=random_n_digits(14)
        cursor.execute(' INSERT INTO navi VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(firstname,lastname,gender,birthday,pin,score,remarks,id))
        mysql.connection.commit()
    cursor.execute('SELECT patient_id from navi WHERE firstname=%s',[firstname])
    patient_id= cursor.fetchone()
    return render_template('navi.html',id=id)
def random_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    
    

@app.route('/navi', methods=['GET',"POST"])
def home():
    
    if request.method == "POST":
        # while True:
        first = request.form.get('first')
        Second = request.form.get('second')
        third = request.form.get('third')
        fourth = request.form.get('fourth')
        fifth = request.form.get('fifth')
        sixth = request.form.get('sixth')
    
    
        score = int(first) + int(Second)+int(third)+int(fourth) + int(fifth)+int(sixth)
        # global add
        add=score  
        # global res
        res=" "
        if score>4:
            res="screening needed"
            
        else:
            res="no need to screen"

        cursor = mysql.connection.cursor()
        #cursor.execute(''' INSERT INTO user VALUES(%f)''',(add))
        cursor.execute('UPDATE navi SET score = %s, remarks =%s  WHERE firstname=%s',(score,res,firstname1))
        #cursor.execute('UPDATE user SET  username =% s, password =% s, email =% s,  WHERE id =% s', (username, password, email(session['id'], ), ))
        mysql.connection.commit()
        return render_template('result.html', add1=add,res=res,fnm=firstname1)
    return render_template('navi.html')



@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('register.html')


if __name__ == "__main__":
  
     app.run(debug=True)