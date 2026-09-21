import src
from src.tools.tools import web_search, scrape_url

results = scrape_url.invoke("https://www.scientificamerican.com/article/ai-labs-are-claiming-agi-is-imminent-but-does-that-mean-what-we-think-it-means/")
print(results)
