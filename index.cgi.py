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
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
<head>
<title>Midlothian Pool Timetables</title>
<link rel="stylesheet" type="text/css" href="style.css" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
</head>
<body>

<h2>Midlothian Pool Timetables</h2>
""" )

for venue, prog in programme_svgs.items():
    print( "<h3>" + venue + "</h3>" )
    print( '<p><img src="data:image/png;base64,' + prog + '" /></p>' )

print( """
<p><a href="https://www.midlothian.gov.uk/directory/3/leisure_centres_and_swimming_pools/category/9">Source page</a></p>
<p><small>Page generated in %s seconds</small></p>
</body>
</html>
""" % ( duration ) )
