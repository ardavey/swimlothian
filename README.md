# swimlothian
A scraper for Midlothian swimming pool programmes to present cropped down versions on a single page.

Currently deployed at https://swim.ardavey.com

`swim_programme_fetcher.py` runs hourly scrapes programme download links from several pages of the bloated Midlothian Leisure site.

It then:
 * Grabs the timetable page from each PDF
 * Crops the pages down to the minimum necessary (this varies due to inconsistent templating)
 * Converts to PNG
 * Stores in a data structure on disk
 
 `index.cgi.py` opens the saved file and serves up the contents to a browser.  All timetables on a single page.
