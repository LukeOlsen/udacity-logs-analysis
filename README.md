# Logs Analysis
## Introduction 

This is a simple SQL exercise using Postgres and the Python DB-API. Its querying a ficitonal 
newspaper database to figure out:
1. Which 3 articles had the most views
2. Which 3 authors had the most views
3. On what days did more than 1% of HTTP requests lead to errors.

## Views

This report makes use of exactly 1 view. It's main purpose is to create a modification of the 
logs table so that it can be joined with the articles table. The main way it goes about this
is taking the path column and removing all the home path ('/') rows while removing '/article/' from the beginning article paths (for exmaple, changing '/article/candidate-is-jerk' to 'candidate-is-jerk'). This allowed the article column of the view to be matched with the slug column from the articles table. With this connection it was possible to count the views and link that data with the article table. Below you can find the view used:

`CREATE VIEW adjusted_logs as
    select RIGHT(path, length(path) - 9) as FixPath, count(path) as views
    from log
    where path <> '/'
    group by FixPath
    order by views desc `

## Running the report

If you're running this report in the vagrantfile provided by Udacity the news database should already be set up for you. In which case all you will need to do is:
    1. Copy [this file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) into your database.
    2. Run `psql -d news -f newsdata.sql` to load the data into the database.
    3. Create a `create_views.sql` file with the above view copied into it. 
    4. Run `psql -d news -f create_views.sql` to add the view into your databse.
    5. Run `python newsdatadb.py` to see results printed to your terminal.