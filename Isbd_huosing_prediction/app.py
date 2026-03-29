from flask import Flask, render_template, request
import pandas as pd
import pickle
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/'
data = pd.read_csv("isb_data.csv")
model = pickle.load(open("isb_house_price_pred.pkl", "rb"))

@app.route('/')
def home():
    locations = sorted(data["location"].unique())
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'house_image.jpeg')
    return render_template("index.html", locations=locations, house_image=pic1)

@app.route("/display" , methods=['GET', 'POST'])
def uploader():    
    if request.method=='POST':
        location = request.form["location"]
        marla = 273*(float(request.form["marla"]))
        marla_entered_by_user = float(request.form["marla"])
        bathrooms = float(request.form["bathrooms"])
        bathrooms_entered_by_user = int(bathrooms)
        bedrooms = float(request.form["bedrooms"])
        bedrooms_entered_by_user = int(bedrooms)

        input = pd.DataFrame([[location,bathrooms,bedrooms,marla]], columns=['location','baths','bedrooms','Total_Area'])
        result = model.predict(input)[0]
        result = "{:.2f}".format(result)
        pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'house_image.jpeg')
        return render_template("display.html", price=result,location=location, marla_entered_by_user=marla_entered_by_user, bathrooms_entered_by_user=bathrooms_entered_by_user, bedrooms_entered_by_user=bedrooms_entered_by_user, house_image=pic1)

if __name__ == '__main__':
    app.run(debug=True) 