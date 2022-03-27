#!/home/ardavey/opt/python-3.10.2/bin/python3

import pickle
import os
from datetime import datetime as dt
from time import strftime
import pytz

pickle_jar = "/home/ardavey/tmp/pickled_pool_programmes"

with open( pickle_jar, "rb" ) as f:
    programme_imgs = pickle.load( f )

file_stats = os.stat( pickle_jar )
file_datetime = dt.fromtimestamp( file_stats.st_mtime, pytz.timezone( "Europe/London" ) )
file_time = file_datetime.strftime( "%d/%m/%Y at %H:%H:%S" )

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

for venue, prog in programme_imgs.items():
    print( """
        <h2>%s</h2>
        <p><img src="data:image/png;base64,%s" /></p>
""" % ( venue, prog ) )

print( """
        <p>These timetables are automatically extracted from the PDFs which are available to download via the <a href="https://www.midlothian.gov.uk/directory/3/leisure_centres_and_swimming_pools/category/9">Midlothian Council website</a>.</p>
        <p>They are updated every hour and presented here for convenience, but no guarantees are given for their contents.</p>
        <p><small>Data last updated: %s</small></p>
<p></p>
    </body>
</html>
""" % file_time )
