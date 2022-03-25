#!/home/ardavey/opt/python-3.10.2/bin/python3

import time
import pickle

pickle_jar = "/home/ardavey/tmp/pickled_pool_programmes"

start_time = time.time()

with open( pickle_jar, "rb" ) as f:
    programme_svgs = pickle.load( f )

end_time = time.time()
duration = round( end_time - start_time, 4 )

print( "Content-type: text/html\n\n" )

print( """
<!doctype html>
<html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Midlothian Pool Timetables</title>
        <link rel="stylesheet" type="text/css" href="style.css" />
        <title>Midlothian Pool Timetables</title>
    </head>
    <body>
        <h1>Midlothian Pool Timetables</h1>
""" )

for venue, prog in programme_svgs.items():
    print( """
        <h2>%s</h2>
        <p><img src="data:image/png;base64,%s" /></p>
""" % ( venue, prog ) )

print( """
        <p><a href="https://www.midlothian.gov.uk/directory/3/leisure_centres_and_swimming_pools/category/9">Source page</a></p>
    </body>
</html>
""" )
