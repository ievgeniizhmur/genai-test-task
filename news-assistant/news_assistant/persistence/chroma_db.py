from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document

from news_assistant.model.article import Article

class ChromaDBClient:

    def __init__(self, config):
        self.embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = self.init_vectorstore()
        self.config = config

    def init_vectorstore(self):
        return Chroma(
            persist_directory="./chroma_store",
            embedding_function=self.embedding_model
        )

    def save(self, articles):
        try:
            new_doc_objs = [self.article_to_document(article) for article in articles]
            self.vectorstore.add_documents(new_doc_objs)
        except Exception as e:
            raise RuntimeError("An error occurred during saving to DB") from e

    def clear(self):
        try:
            self.vectorstore.delete_collection()
            self.vectorstore = self.init_vectorstore()
        except Exception as e:
            raise RuntimeError("An error occurred during clearing DB") from e

    def semantic_search(self, query):
        try:
            k = self.config["vectorstore"]["search_docs_number"]
            results = self.vectorstore.similarity_search(query, k=k)

            return [self.document_to_article(doc) for doc in results]
        except Exception as e:
            raise RuntimeError("An error occurred during DB search") from e

    def get_documents_enriched_with_id(self, query):
        k = self.config["ai_assistant"]["articles_number"]
        docs = self.vectorstore.as_retriever(search_kwargs={"k": k}).get_relevant_documents(query)
        return self.format_docs_with_metadata(docs)


    def format_docs_with_metadata(self, docs):
        formatted = []
        for doc in docs:
            meta = doc.metadata
            text = f"URL: {doc.metadata.get("url")}\n{doc.page_content}"
            formatted.append(Document(page_content=text, metadata=meta))
        return formatted

    def article_to_document(self, article: Article) -> Document:
        search_text = f"Summary: {article.summary}\nTopics: {article.topics}"

        return Document(
            page_content=search_text,
            metadata={
                "title": article.title,
                "summary": article.summary,
                "topics":  article.topics,
                "url":  article.url,
                "content": ', '.join(article.content)
            }
        )

    def document_to_article(self, document: Document) -> Article:
        return Article(title=document.metadata.get("title"),
                       content=document.metadata.get("content"),
                       url=document.metadata.get("url"),
                       topics=document.metadata.get("topics"),
                       summary=document.metadata.get("summary"))

