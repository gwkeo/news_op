class Comments:
    likes: int
    dislikes: int
    count: int

    def __init__(self, likes: int, dislikes: int):
        self.likes = likes
        self.dislikes = dislikes
        self.count = likes + dislikes

class Article:
    title: str
    url: str
    comments: Comments

    def __init__(self, title: str, url: str, likes: int, dislikes: int):
        self.title = title
        self.url = url
        self.comments = Comments(likes, dislikes)

