import datetime
tweet = "rt @harpersbazaar The top 7 swimsuit trends of the season—which will you wear? #pretty"
url_pattern = re.compile(r'(http(s?)://)[\w./]+')
linkcount = len(url_pattern.findall(tweet))
followers = 100
df2 = pandas.DataFrame.from_dict({ 'Text' : [tweet], 'LinkCount' : [linkcount], 
                                  'Followers' : [followers], 
                                  'DateTime' : [datetime.datetime.now().strftime("%d %m %Y %H:%M:%S")]})
print df2
pipeline.fit(df, df["Viral"])
predictions = pipeline.predict(df2)
if predictions[0] == 0:
    print "Not viral"
else:
    print "viral"