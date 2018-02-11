import sqlite3
import scraper
import feedparser


def update_hl_db():
    sqlfile = '/Users/alonj/Databases/newsflow'
    conn = sqlite3.connect(sqlfile)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM headlines ORDER BY head_ID DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.execute("SELECT * FROM feeds")
    sources = cursor.fetchall()
    if result is not None:
        index = int(str(result[0]), 16)
    else:
        index = 0
    for feed in sources:
        url = feed[1]
        feedID = feed[0]
        url_parsed = feedparser.parse(url)
        for item in url_parsed['items']:
            key = hex(index)
            title = item['title']
            summary = scraper.BeautifulSoup(item['summary'], 'html.parser').get_text()
            published = item['published']
            insert_arr = (key, title, summary, published, feedID)
            cursor.execute(
                'INSERT OR IGNORE INTO headlines(head_ID, headline, subhead, timestamp, feedID) VALUES(?,?,?,?,?)',
                insert_arr)
            index += 1
    conn.commit()
    conn.close()


def update_word_bank():
    pass


def update_centroids():
    pass


def main():
    update_hl_db()


if __name__ == "__main__":
    main()
