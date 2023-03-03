from flask import Flask, request, render_template
import pandas as pd
import pickle
import numpy as np

# Create Flask app
app = Flask(__name__)

# Load the trained machine learning model
model = pickle.load(open('model.pkl', 'rb'))

# Define an endpoint to receive input data and return predictions
@app.route('/', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        age = int(request.form['age'])# in form format value return in string form and model required in numerical form 
        sex = request.form['sex']
        bmi = float(request.form['bmi']) # in form format value return in string form and model required in numerical form 
        children = int(request.form['children']) # in form format value return in string form and model required in numerical form 
        smoker = request.form['smoker']
        region = request.form['region']

        # Define conversion functions
        def cnvt_1(sex):
            if sex == 'male':
                return 1
            else:
                return 0

        def cnvt_2(smoker):
            if smoker == 'yes':
                return 1
            else:
                return 0

        def cnvt_3(region):
            if region == 'southeast':
                return 1
            elif region == 'southwest':
                return 2
            elif region == 'northwest':
                return 3
            else:
                return 4

        # Convert input data to appropriate format
        sex = cnvt_1(sex)
        smoker = cnvt_2(smoker)
        region = cnvt_3(region)

        # Make Data Frame of user input data (of above data)
        test_df = pd.DataFrame({'age': [age], 'sex': [sex], 'bmi': [bmi], 'children': [children], 'smoker': [smoker], 'region': [region]})
        prediction_expense = model.predict(test_df)
        print(prediction_expense)# Just for testing
        print('Sucsess_1')
        # Render prediction results in template
        return render_template('result.html', prediction=np.around(prediction_expense[0],2))

    # Render input form template
    return render_template('index.html') ##################################### very IMP #######################

if __name__ == '__main__':
    app.run(debug=True)
