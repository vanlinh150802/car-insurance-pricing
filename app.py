#import flask
# pip install flask
from flask import Flask, render_template, request
from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
import pickle
z = pd.read_excel('C:/Users/fna/Downloads/App/App/z.xlsx')
X = pd.read_excel('C:/Users/fna/Downloads/App/App/X.xlsx')
def TEST(test,z):
    listtest=[]
    for k in X.columns:
        l=k.split('_')
        if len(l)==1:
            x=(test[l[0]]-z[k][1])/z[k][2]
        else:
            if test[l[0]]==l[1]:
                x=(1-z[k][1])/z[k][2]
            else:
                x=(0-z[k][1])/z[k][2]           
        listtest.append(x)
    import numpy as np
    user_input=np.array([listtest])
    return user_input
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        age= int(request.form["Age"])
        mar= request.form["Marital"]
        emp= request.form["Employed"]
        loc= request.form["Location"]
        sta= request.form["State"]
        veh= request.form["Vehicle"]
        dri= int(request.form["Driving"])
        cla= int(request.form["Claim"])
        cov= request.form["Coverage"]
        test={'Months Since Driving':dri,'Vehicle Class':veh,'Age':age,'Coverage':cov,'Marital Status':mar,
      'Location Code':loc,'EmploymentStatus':emp,'Months Since Last Claim':cla,'State':sta}
        dl=TEST(test,z)
        class_model = pickle.load(open('C:/Users/fna/Downloads/App/App/classifier.pkl', 'rb'))
        gr=class_model.predict(dl)[0]
        if gr==0:
            reg_model = pickle.load(open('C:/Users/fna/Downloads/App/App/xgb0.pkl', 'rb'))
        elif gr==1:
            reg_model = pickle.load(open('C:/Users/fna/Downloads/App/App/xgb1.pkl', 'rb'))
        elif gr==2:
            reg_model = pickle.load(open('C:/Users/fna/Downloads/App/App/xgb2.pkl', 'rb')) 
        elif gr==3:  
            reg_model = pickle.load(open('C:/Users/fna/Downloads/App/App/xgb3.pkl', 'rb'))
        elif gr==4:
            reg_model = pickle.load(open('C:/Users/fna/Downloads/App/App/xgb4.pkl', 'rb'))
        elif gr==5:   
            reg_model = pickle.load(open('C:/Users/fna/Downloads/App/App/xgb5.pkl', 'rb'))
        price = reg_model.predict(dl)[0]
        return render_template('results.html', pricing=price)
    
if __name__ == '__main__':
#     # app.run(host="127.0.0.1:5000", port=8080, debug=True)
    app.run(debug=True)