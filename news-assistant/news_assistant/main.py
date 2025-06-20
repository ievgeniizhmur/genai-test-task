import textwrap
import os
from dotenv import load_dotenv

from news_assistant.web_scraping.tsn import TsnScrapper
from news_assistant.ai.openai import OpenAIConnector
from news_assistant.persistence.chroma_db import ChromaDBClient

print("\nLoading News AI Assistant...")
load_dotenv(override=True)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

scrapper = TsnScrapper()
chromadb_client = ChromaDBClient()
ai_connector = OpenAIConnector(chromadb_client)

def read_urls_from_file(file_path):
    print("Read urls from file:")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "resources", file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    return urls


def analyze_url(url):
    print(f"Loading url: {url}")
    article_from_url = scrapper.scrap_url(url)

    if article_from_url:
        print("Generating article summary...")
        ai_connector.generate_summary(article_from_url)
        print(f"Article details: \n{article_from_url}")

        print(f"Saving to DB...")
        chromadb_client.save([article_from_url])


def main():
    print("\nWelcome!")

    while True:
        print(textwrap.dedent("""
        =====================================
        Select operation:
        1 - Load news article from tsn.ua URL
        2 - Load news from URls file (resources/urls.txt)
        3 - AI powered search for news

        Developer menu:
        5 - Semantic search in DB
        6 - Clean DB
        0 - Exit
        ====================================
        """))

        try:
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                url = input("\nEnter url from tsn.ua: ")
                analyze_url(url)

            elif choice == "2":
                is_load = input("\nConfirm URLs loading from file. Enter 'Yes'")
                if is_load == 'Yes':
                    urls = read_urls_from_file("urls.txt")
                    print(f"Going to load {len(urls)} urls from file")
                    for url in urls:
                        analyze_url(url)

            elif choice == "3":
                query = input("\nEnter your search query: ")
                ai_connector.analyze_articles(query)

            elif choice == "5":
                query = input("\nEnter search query: ")
                print(f"Searching for: {query}")
                article_from_db = chromadb_client.semantic_search(query)

                print("News articles found:")
                for article in article_from_db:
                    print(article)

            elif choice == "6":
                is_delete = input("\nConfirm DB content deletion. Enter 'Yes'")
                if is_delete == 'Yes':
                    chromadb_client.clear()
                    print(f"DB content deleted")

            elif choice == "0":
                print("\nExiting News AI Assistant. Goodbye!")
                break
            else:
                print("Invalid input. Please try again.")

        except Exception as e:
            print(f"Unexpected error occurred! Message: {e}")
            print(f"Cause: {e.__cause__}")


if __name__ == "__main__":
    main()
