#!/home/ardavey/opt/python-3.10.2/bin/python3

import urllib.request
import re
import fitz
import gzip
import base64
from bs4 import BeautifulSoup
import pickle

base_url = "https://www.midlothian.gov.uk"
path = "/directory/3/leisure_centres_and_swimming_pools/category/9"
pickle_jar = "/tmp/pickled_pool_programmes"

# Grab the page that links out to all of the individual pool pages
# then grab the URLs for those pages from the links.
with urllib.request.urlopen( base_url + path ) as response:
    page_content = response.read()
 
soup = BeautifulSoup( page_content, "html.parser" )
pool_links = soup.find_all( href = re.compile("directory_record") )

# Visit each of the pool pages, grab the venue name and determine the URL for the PDF programme.
# Some pages link directly and some link to a page which offers the PDF download link. Luckily
# the direct PDF URLs can be determined directly from the d/l pages following a pattern so we
# can cheat a little and save some web page loads.
programme_svgs = {}

for pool_link in pool_links:
    with urllib.request.urlopen( base_url + pool_link[ "href" ] ) as response:
        pool_page = response.read()
    pool_soup = BeautifulSoup( pool_page, "html.parser" )
    pool_name = pool_soup.find( "h1" ).text.split( " - " )[1].strip()

    # Turn: <base URL>/downloads/file/1234/foobar
    # Into: <base URL>/download/downloads/id/1234/foobar.pdf
    programme_link = pool_soup.find( href = re.compile( "download", re.IGNORECASE ) )
    p = re.compile( "downloads/file/(.*)" )
    programme_url = p.sub( r"download/downloads/id/\1.pdf", programme_link[ "href" ] )

    # Download the data from the PDF file
    with urllib.request.urlopen( programme_url ) as pdf:
        programme_pdf = pdf.read()
    
    # Convert PDF to PNG
    # If we leave it to defaults one of the timetables ends up larger than the rest
    # so we're creating a new PDF at A4 size and slapping the source page into that.
    # Then when we convert to PNG they'll all be the same size.
    src_doc = fitz.open( "pdf", programme_pdf )
    new_doc = fitz.open()
    
    for src_page in src_doc:
        format = fitz.paper_rect( "a4-l" )  # landscape if input suggests
        page = new_doc.new_page( width = format.width, height = format.height )
        page.show_pdf_page( page.rect, src_doc, src_page.number )

    # Figure out the cropping nonsense.  The timetables don't share a common
    # template so we have to bugger about measuring each one separately.

    # Determine the coordinates of the top left and bottom right corners of our crop.
    # Count in from the left and right of the image map until we see a non-white pixel
    # to get the x values.
    # Follow the vertical line at the left x point up and down until we hit white again
    # to get the y values (then add on a buffer to account for the offset header and footer rows)
    map = new_doc[0].get_pixmap()
    xnow = 0
    ynow = round( map.height / 2 )
    dow_buffer = 10

    while map.pixel( xnow, ynow ) == ( 255, 255, 255 ):
        xnow += 1
    xtl = xnow

    xnow += 1
    while map.pixel( xnow, ynow ) != ( 255, 255, 255 ):
        ynow -= 1
    ytl = ynow - dow_buffer

    ynow += 1
    while map.pixel( xnow, ynow ) != ( 255, 255, 255 ):
        ynow += 1
    ybr = ynow + dow_buffer

    xnow = map.width - 1
    while map.pixel( xnow, ynow ) == ( 255, 255, 255 ):
        xnow -= 1
    xbr = xnow    

    clip = fitz.Rect( xtl, ytl, xbr, ybr )
    png = new_doc[0].get_pixmap( dpi = 96, clip = clip ).tobytes()
    programme_svgs[ pool_name ] = base64.b64encode( png ).decode( "utf-8" )

# Write this lot to file
file = open( pickle_jar, "wb" )
pickle.dump( programme_svgs, file )
file.close()