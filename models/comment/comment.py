from pydantic import BaseModel

class Comment(BaseModel):
    username: str
    date: str
    msg: str
    oid: str
    def __str__(self):
        return f"Comment(id={self.id}, username={self.username}, date={self.date}, msg={self.msg}, oid={self.oid})"