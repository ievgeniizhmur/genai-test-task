from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser
from langchain.output_parsers import ResponseSchema
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain

from news_assistant.model.article import Article
from news_assistant.persistence.chroma_db import ChromaDBClient


class OpenAIConnector:

    def __init__(self, vectorstore_client: ChromaDBClient, config):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-4", )
        self.vectorstore_client = vectorstore_client
        self.config = config

    def generate_summary(self, article: Article):
        try:
            response_schemas = [
                ResponseSchema(name="summary", description="A brief summary of the news article. Use 3-5 sentences"),
                ResponseSchema(name="topics", description="A string of main topics covered in the article " +
                                                          "separated by coma. Example: 'war', 'people', 'politic'")
            ]

            parser = StructuredOutputParser.from_response_schemas(response_schemas)
            format_instructions = parser.get_format_instructions()

            template = ("""Your purpose to read news article title and content and create summary in 3-5 sentences."
                                Article title is <{title}>, Article content is <{content}>.
                                
                                {format_instructions}
                                """).strip()

            prompt = PromptTemplate(input_variables=["title", "content"],
                                    template=template,
                                    partial_variables={"format_instructions": format_instructions})
            chain = prompt | self.llm
            raw_response = chain.invoke({
                "title": article.title,
                "content": article.content,
            })

            parsed_output = parser.parse(raw_response.content)
            article.summary = parsed_output["summary"]
            article.topics = parsed_output["topics"]
        except Exception as e:
            raise RuntimeError("An error occurred during summary generation") from e

    def analyze_articles(self, query):
        try:
            prompt = PromptTemplate.from_template("""
            You are News AI assistant.
            Use the following news articles to answer the question. Each includes URL and summery.
            In addition to answer at the end of response Return list of articles URLs that are connected to the question.
            If there is no relevant articles - return message 'No relevant articles are found'.
            Leave list without any test description. Last sentence of the response must be just a list.
            Example: 
            Relevant articles URLs: 
            url_1
            url_1
            
            
            {context}

            Question: {question}
            Answer:
            """)

            verbose = self.config["llm"]["verbose"]
            stuff_chain = StuffDocumentsChain(
                llm_chain=LLMChain(llm=self.llm, prompt=prompt, verbose=verbose),
                document_variable_name="context",
            )

            docs = self.vectorstore_client.get_documents_enriched_with_id(query)
            response = stuff_chain.run(input_documents=docs, question=query)

            print(response)

        except Exception as e:
            raise RuntimeError("An error occurred during analysis") from e



