
import psycopg2

# Connect to news database

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# Creating view that will be used in the
# 3 most popular articles and authors queries

create_view = '''create view topthree as 
    select RIGHT(path, length(path) - 9) as FixPath, count(path) as views
    from log
    where path <> '/'
    group by FixPath
    order by views desc
    limit 3
    '''

# Creating the view in the database

c.execute(create_view)

# 3 most popular articles of all time (title, number of views)

top_article_query = '''
    select title, views
    from articles join topthree on (articles.slug = topthree.FixPath)
    '''

c.execute(top_article_query)
article_results = c.fetchall()

# For loop to have results print in plain text

for x in article_results:
    print('"{}" - {} views.'.format(x[0], x[1]))


# Who are the most popular article authors of all time (author name, number of views)

top_author_query = '''
    select authors.name, views
    from articles join topthree on (articles.slug = topthree.FixPath) join authors on (authors.id = articles.author)
    '''
c.execute(top_author_query)
author_results = c.fetchall()


for x in author_results:
    print('{} - {} views.'.format(x[0], x[1]))

# On which days did more than 1% of requests lead to errors (date, % of errors)

error_query = '''
    select FailureRate.FailureDate, ROUND(((FailureRate.NumFailure::decimal / SuccessRate.NumSuccess::decimal) * 100), 1)
    from (
        select to_char(time, 'MM-DD-YYYY') as SuccessDate, status, count(status) as NumSuccess
        from log
        where status = '200 OK' 
        group by SuccessDate, status
    ) as SuccessRate join (
        select to_char(time, 'MM-DD-YYYY') as FailureDate, status, count(status) as NumFailure
        from log
        where status = '404 NOT FOUND' 
        group by FailureDate, status
    ) as FailureRate on SuccessRate.SuccessDate = FailureRate.FailureDate
    where ((FailureRate.NumFailure::decimal / SuccessRate.NumSuccess::decimal) * 100) > 1
    group by FailureRate.FailureDate, FailureRate.NumFailure, SuccessRate.NumSuccess
    '''

c.execute(error_query)
error_results = c.fetchall()
for x in error_results:
    print('{} - {}% errors '.format(x[0], x[1]))


db.close()
