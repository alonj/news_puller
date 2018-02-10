import sqlite3
import scraper


def get_html():
    raw_html = scraper.simple_get('https://www.ynet.co.il/home/0,7340,L-187,00.html')
    html = scraper.BeautifulSoup(raw_html, 'html.parser')
    return html.select('.art_headlines_item_content')


def main():
    sqlfile = '/Users/alonj/Databases/newsflow'
    conn = sqlite3.connect(sqlfile)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM headlines ORDER BY head_ID DESC LIMIT 1")
    result = cursor.fetchone()
    newsblock = get_html()
    if result is not None:
        index = int(str(result[0]), 16)
    else:
        index = 0
    for obj in newsblock:
        key = hex(index)
        hl_text = str(obj.select_one('a').get_text())
        content = str(obj.select_one('.art_headlines_sub_title').get_text())
        print(key, hl_text)
        cursor.execute('INSERT INTO headlines(head_ID, headline, subhead) VALUES(?,?,?)', (key, hl_text, content))
        index += 1
    conn.commit()
    conn.close()
    print(index)


if __name__ == "__main__":
    main()

