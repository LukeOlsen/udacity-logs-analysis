#!/usr/bin/env python3
import psycopg2

# Connect to news database

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# Creating view that will be used in the
# 3 most popular articles and authors queries

create_view = '''create view adjusted_logs as
    select RIGHT(path, length(path) - 9) as FixPath, count(path) as views
    from log
    where path <> '/'
    group by FixPath
    order by views desc
    '''

# Creating the view in the database

c.execute(create_view)

# 3 most popular articles of all time (title, number of views)

top_article_query = '''
    select title, views
    from articles join adjusted_logs on (articles.slug = adjusted_logs.FixPath)
    group by title, views
    order by views desc
    limit 3
    '''

c.execute(top_article_query)
article_results = c.fetchall()

# For loop to have results print in plain text

print('Here are your top three articles')
print('--------------------------------')
print(' ')

for x in article_results:
    print('"{}" - {} views.'.format(x[0], x[1]))

# Who are the most popular article authors of all
# time (author name, number of views)
print(' ')

print('Here are your top three authors')
print('--------------------------------')
print(' ')

top_author_query = '''
    select authors.name, views
    from articles
    join adjusted_logs on (articles.slug = adjusted_logs.FixPath)
    join authors on (authors.id = articles.author)
    group by authors.name, views
    order by views desc
    limit 3
    '''
c.execute(top_author_query)
author_results = c.fetchall()


for x in author_results:
    print('{} - {} views.'.format(x[0], x[1]))

# On which days did more than 1% of requests lead to errors (date, % of errors)
print(' ')

error_query = '''
    select FailureRate.FailureDate,
    ROUND(((FailureRate.NumFailure::decimal / TotalAccess.TotalCount::decimal) * 100), 2)
    from (
        select time::date as Date, count(status) as TotalCount
        from log
        group by Date
    ) as TotalAccess join (
        select time::date as FailureDate, status, count(status) as NumFailure
        from log
        where status = '404 NOT FOUND'
        group by FailureDate, status
    ) as FailureRate on TotalAccess.Date = FailureRate.FailureDate
    where ((FailureRate.NumFailure::decimal / TotalAccess.TotalCount::decimal) * 100) > 1
    group by FailureRate.FailureDate, FailureRate.NumFailure, TotalAccess.TotalCount
    '''

c.execute(error_query)
error_results = c.fetchall()

print('Here are the days where there were more that 1% errors')
print('-----------------------------------------------------r')
print(' ')
for x in error_results:
    print('{} - {}% errors '.format(x[0], x[1]))


db.close()
