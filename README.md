# Introduction 

This is a simple SQL exercise using Postgres and the Python DB-API. Its querying a ficitonal 
newspaper database to figure out which 3 articles had the most views, which 3 authors had the most
views and on what days did more than 1% of HTTP requests lead to errors.

# Views

This report makes use of exactly 1 view. It's main purpose is to create a modification of the 
logs table so that it can be joined with the articles table. The main way it goes about this
is taking the path column and removing all the home path ('/') rows while removing '/article/' from the beginning article paths (for exmaple, changing '/article/candidate-is-jerk' to 'candidate-is-jerk'). This allowed the article column of the view to be matched with the slug column from the articles table. With this connection it was possible to count the views and link that data with the article table. 

# Running the report

This report can simply be run by entering `python newsdatadb.py` into the command line and the results will print to the terminal in plain text.