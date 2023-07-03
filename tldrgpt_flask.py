from flask import Flask
from flask import request
from tldrgpt import main_runner


# create the Flask app
app = Flask(__name__)

@app.route('/tldr_article')
def tldr_article():
    # if key doesn't exist, returns None
    url = request.args.get('url')

    if not url:
        return 'Missing Article URL'

    response = main_runner(url).replace('\n', '<br>')

    return response

def main():
    app.run(debug=False, host='0.0.0.0', port=5000)

main()