import datetime
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# TODO insert training here 
from model import *
pipeline.fit(df, df["Viral"])

# TODO insert api endpoint here
url_pattern = re.compile(r'(http(s?)://)[\w./]+')
    
@app.route('/predict')
def predict():
    tweet = request.args.get('tweet', '')
    print tweet
    tweet = r"rt @ harpersbazzar The top 7 swimsuit trends of the season-which will you wear? #pretty"
    linkcount = len(url_pattern.findall(tweet))
    followers = 100
    df2 = pandas.DataFrame.from_dict({ 'Text' : [tweet], 'LinkCount' : [linkcount],
                                      'Followers' : [followers],
                                      'DateTime' : [datetime.datetime.now().strftime("%d %m %Y %H:%M:%S")]})
    predictions = pipeline.predict(df2)
    if predictions[0] == 1:
        return "Viral!"
    else:
        return "Not viral"

if __name__ == '__main__':
    app.debug = True
    app.run()
