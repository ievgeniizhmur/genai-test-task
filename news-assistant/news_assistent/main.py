import textwrap

from web_scraping.tsn import TsnScrapper
from ai.openai import OpenAIConnector
from persistence.chroma_db import ChromaDBClient


print("\nLoading News AI Assistant...")
scrapper = TsnScrapper()
chromadb_client = ChromaDBClient()
ai_connector = OpenAIConnector(chromadb_client)


def main():
    print("\nWelcome!")

    while True:
        print(textwrap.dedent("""
        =====================================
        Select operation:
        1 - Load news article from tsn.ua URL
        2 - AI powered search for news

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
                print("Reading url...")
                article_from_url = scrapper.scrap_url(url)

                if article_from_url:
                    print("Generating article summary...")
                    ai_connector.generate_summary(article_from_url)
                    print(f"Article details: \n{article_from_url}")

                    print(f"\nSaving to DB...")
                    chromadb_client.save([article_from_url])

            elif choice == "2":
                query = input("\nEnter your search query: ")
                ai_connector.analyze_articles2(query)

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
