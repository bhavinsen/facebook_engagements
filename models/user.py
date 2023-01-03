from db import Model
import bcrypt


class User(Model):

    def setPassword(self,password):
        self.password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode("utf-8")