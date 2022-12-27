from flask import Flask , render_template , request
from utils import predictor_class

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction' ,  methods = ['POST', 'GET'])
def prediction():
    data = request.form
    obj = predictor_class(data)
    result = obj.remove_special_char(data)

    return render_template('index.html' , res =result)




if __name__ == '__main__':
    app.run(debug=True)