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

print(' ')
print('Here are the top three articles')
print('--------------------------------')
print(' ')

for title, views in article_results:
    print('"{}" - {} views.'.format(title, views))

# Who are the most popular article authors of all
# time (author name, number of views)

print(' ')
print('Here are the top three authors')
print('--------------------------------')
print(' ')

top_author_query = '''
    select authors.name, sum(adjusted_logs.views) as TotalViews
    from articles
    join adjusted_logs on (articles.slug = adjusted_logs.FixPath)
    join authors on (authors.id = articles.author)
    group by authors.name
    order by TotalViews desc
    limit 3
    '''
c.execute(top_author_query)
author_results = c.fetchall()


for author, views in author_results:
    print('{} - {} views.'.format(author, views))

# On which days did more than 1% of requests lead to errors (date, % of errors)

error_query = '''
    select FailRate.FailDate,
    ROUND(((FailRate.NumFail::decimal / TAccess.TCount::decimal) * 100), 2)
    from (
        select time::date as Date, count(status) as TCount
        from log
        group by Date
    ) as TAccess join (
        select time::date as FailDate, status, count(status) as NumFail
        from log
        where status = '404 NOT FOUND'
        group by FailDate, status
    ) as FailRate on TAccess.Date = FailRate.FailDate
    where ((FailRate.NumFail::decimal / TAccess.TCount::decimal) * 100) > 1
    group by FailRate.FailDate, FailRate.NumFail, TAccess.TCount
    '''

c.execute(error_query)
error_results = c.fetchall()

print(' ')
print('Here are the days where there were more that 1% errors')
print('-----------------------------------------------------')
print(' ')

for x in error_results:
    print('{} - {}% errors '.format(x[0], x[1]))


db.close()
