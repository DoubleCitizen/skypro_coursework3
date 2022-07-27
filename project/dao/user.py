from project.dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.title = user_d.get("title")
        user.description = user_d.get("description")
        user.trailer = user_d.get("trailer")
        user.year = user_d.get("year")
        user.rating = user_d.get("rating")
        user.genre_id = user_d.get("genre_id")
        user.director_id = user_d.get("director_id")

        self.session.add(user)
        self.session.commit()
