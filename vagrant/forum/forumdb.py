#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    pg = psycopg2.connect("dbname=forum")
    c = pg.cursor()

    c.execute("select * from posts order by time desc;")
    table = c.fetchall()

    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in table]

    print posts

    pg.close()

    #posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    t = time.strftime('%c', time.localtime())
    #DB.append((t, content))

    pg = psycopg2.connect("dbname=forum")
    c = pg.cursor()

    #c.execute("insert into posts (content, time) values ('%s', '%s')" % (content,t))
    clean = bleach.clean(content)
    c.execute("insert into posts (content) values (%s)" , (clean,))
    pg.commit()
    pg.close()
