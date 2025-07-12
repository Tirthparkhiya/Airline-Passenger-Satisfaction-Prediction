from flask import Flask,render_template,request
import joblib
from config.path_config import *

app=Flask(__name__)

model=joblib.load(MODEL_SAVE_PATH)

@app.route("/", methods=["GET",'POST'])
def home():
    if request.method=="POST":
        try:
            departure_delay=float(request.form["Departure Delay"])
            arrival_delay=float(request.form['Arrival Delay'])
            
            flight_distance=float(request.form['Flight Distance'])
            
            delay_ratio=(departure_delay+arrival_delay)/(flight_distance+1)
            
            
            data=[
                int(request.form["Online Boarding"]),
                delay_ratio,
                int(request.form['Inflight WiFi Service']),
                int(request.form['Class']),
                int(request.form['Type of Travel']),
                flight_distance,
                int(request.form['Inflight Entertainment']),
                int(request.form['Seat Comfort']),
                int(request.form['Leg Room Service']),
                int(request.form['On-Board Service']),
                int(request.form['Ease of Online Booking']),
                int(request.form['Cleanliness'])
                
            ]
            prediction=model.predict([data])
            output=prediction[0]
            
            return render_template("index.html",prediction=output)
        
        except Exception as e:
            return render_template("index.html",error=str(e))
    
    return render_template("index.html")


if __name__=='__main__':
    app.run(debug=True)    
        
        