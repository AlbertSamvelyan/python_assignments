import feedparser

google_news_url="https://news.google.com/news/rss"

def get_headlines(rss_url):
    rss_feed = feedparser.parse(rss_url)
    headlines = []
    for item in rss_feed.entries:
        headlines.append(item.title)
    return headlines

print(get_headlines(google_news_url))