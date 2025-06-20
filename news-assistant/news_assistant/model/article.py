class Article:

    def __init__(self, title, content, summary, topics, url):
        self.title = title
        self.content = content
        self.summary = summary
        self.topics = topics
        self.url = url

    def __str__(self):
        return (f'----------------------------------------------\n' +
                f'Title: {self.title} \nUrl:{self.url} \nTopics:{self.topics} \nSummary:{self.summary} ' +
                f'\nContent:{self.content}.\n ----------------------------------------------')
