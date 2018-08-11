import sqlite3
import scraper
import feedparser
import stopwords_heb
from datetime import datetime, timedelta
import kmeans

from nltk.tokenize import word_tokenize

hl_dict_binary = {}


def connect_db():
    database = '/Users/alonj/Databases/newsflow'
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return cursor, conn


def format_as_date(datestring):
    date_tokens = word_tokenize(datestring)
    year = date_tokens[4]
    leap_year = abs(2020-int(year)) % 4 == 0
    if leap_year:
        feb_days = 29
    else:
        feb_days = 28
    days_in_month = {
        "jan": ("01", 31),
        "feb": ("02", feb_days),
        "mar": ("03", 31),
        "apr": ("04", 30),
        "may": ("05", 31),
        "jun": ("06", 30),
        "jul": ("07", 31),
        "aug": ("08", 31),
        "sep": ("09", 30),
        "oct": ("10", 31),
        "nov": ("11", 30),
        "dec": ("12", 31)
    }
    day = date_tokens[2]
    if len(day) == 1:
        day = "0"+day
    month_str = str(date_tokens[3])
    month_raw = month_str.lower()[:3]
    month = days_in_month[month_raw][0]
    hour = date_tokens[5]
    new_hour = hour
    if len(date_tokens) > 6:
        offset = int(date_tokens[6][1:]) / 100
        offset = int(offset)
        if date_tokens[6][0] == "-":
            offset = offset*(-1)
        hour_h = int(hour[:2])+offset
        if int(hour_h) < 10:
            hour_h = "0" + str(hour_h)
        if int(hour_h) > 23:
            hour_h = str(int(hour_h)-24)
            if int(hour_h) < 10:
                hour_h = "0" + str(hour_h)
            else:
                hour_h = str(hour_h)
            day = str(int(day)+1)
            if len(day) == 1:
                day = "0"+day
            if int(day) > days_in_month[month_raw][1]:
                month = int(month)+1
                day = "01"
                if month < 10:
                    month = "0"+str(month)
                if int(month) > 12:
                    year = str(int(year)+1)
                    month = "01"
        new_hour = str(hour_h) + hour[2:]
    hour = new_hour
    time_format = str(year+"-"+month+"-"+day+" "+hour+".000")
    return time_format


def update_hl_db():
    cursor, conn = connect_db()
    cursor.execute("SELECT * FROM headlines ORDER BY head_ID DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.execute("SELECT * FROM feeds")
    sources = cursor.fetchall()
    if result is not None:
        index = int(str(result[0]))
    else:
        index = 0
    for feed in sources:
        feed_id = feed[0]
        url = feed[1]
        feed_last_updated = feed[3]
        url_parsed = feedparser.parse(url)
        for item in url_parsed['items']:
            key = index
            title = item['title']
            summary = scraper.BeautifulSoup(item['summary'], 'html.parser').get_text()
            published = item['published']
            publish_date_formatted = format_as_date(published)
            insert_arr = (key, title, summary, publish_date_formatted, feed_id)
            if publish_date_formatted > feed_last_updated:
                cursor.execute(
                    'INSERT OR IGNORE INTO headlines(head_ID, headline, subhead, timestamp, feedID) VALUES(?,?,?,DATETIME(?),?)',
                    insert_arr)
            index += 1
    conn.commit()
    conn.close()
    

def feed_update_date():
    cursor, conn = connect_db()
    cursor.execute("SELECT feedID, MAX(timestamp) FROM headlines GROUP BY feedID")
    dates = cursor.fetchall()
    for date in dates:
        sql_q = "UPDATE feeds SET last_update='"+date[1]+"' WHERE feedID="+str(date[0])
        cursor.execute(sql_q)
    conn.commit()
    conn.close()


def gather_docs():
    cursor, conn = connect_db()
    cursor.execute("SELECT subhead from headlines WHERE subhead IS NOT NULL")
    docs = cursor.fetchall()
    kmeans.clusterify(docs)


# def update_word_bank():
#     cursor, conn = connect_db()
#     stopwords = stopwords_heb.stopwords
#     cursor.execute("SELECT * FROM headlines")
#     headlines = cursor.fetchall()
#     hl_dict = {}
#     bag_of_words = {}
#     bag_index = 1
#     for hl in headlines:
#         hl_tokens = word_tokenize(hl[1])
#         hl_dict[hl[0]] = hl_tokens
#         for word in hl_tokens:
#             if word not in bag_of_words.keys() and word not in stopwords:
#                 bag_of_words[word] = bag_index
#                 bag_index += 1
#     vec_len = bag_index - 1
#     for key in hl_dict.keys():
#         new_vec = [0, ] * vec_len
#         for word in hl_dict[key]:
#             if word not in stopwords:
#                 new_vec[bag_of_words[word]-1] = 1
#         hl_dict_binary[key] = new_vec
#     conn.close()


# def update_centroids():
#     pass


def main():
    feed_update_date()
    update_hl_db()
    gather_docs()
    # update_word_bank()
    # update_centroids()


if __name__ == "__main__":
    main()


