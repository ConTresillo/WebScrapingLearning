from newspaper import Article

url = "https://www.hindustantimes.com/india-news/some-news"
article = Article(url)
article.download()
article.parse()
print(article.title)
print(article.text)
