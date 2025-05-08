from datetime import datetime

class News:
    title: str
    url: str
    earliest_post_time: datetime
    latest_post_time: datetime

    def __init__(self, title : str, url : str, earliest_post_time: str, latest_post_time: str):
        self.title = title
        self.url = url
        self.earliest_post_time = datetime.strptime(earliest_post_time)
        self.latest_post_time = datetime.strptime(latest_post_time)

