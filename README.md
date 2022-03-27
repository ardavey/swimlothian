# swimlothian
A scraper for Midlothian swimming pool programmes to present cropped down versions on a single page.

Currently deployed at https://swim.ardavey.com

`swim_programme_fetcher.py` runs in the background every hour and does the following:
 * Browses through the relevant Midlothin Leisure web pages (for each swimming venue)
 * Works out all of the applicable venue names and determines the download links for their programmes
 * Downloades each PDF programme and keeps only the timetable page
 * Crops the pages down to the minimum necessary size, removing all the info that's not part of the timetable itself (this varies due to inconsistent templating)
 * Resizes to a consistent image size
 * Converts to PNG
 * Stores in a data file on disk
 
 `index.cgi.py` runs whenever the site is opened and does the following:
 * Loads the data file
 * Generates some HTML including the processed PNG images all on one page
