from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path='')

@app.route('/', methods=['GET'])
@app.route('/hello_maps', methods=['GET'])
def homepage():
    return render_template('hello_maps.html', key=os.environ["GOOGLE_MAPS_API_KEY"])

if __name__ == "__main__":
    app.run(debug=True)



