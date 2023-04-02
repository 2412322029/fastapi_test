from api.password import hash_password
from config import Config
from sql.database import get_session
from sql.dbModels import User

if __name__ == '__main__':
    session = next(get_session())
    session.add(User(
        username=Config['Default_Administrator'],
        password=hash_password(Config['Default_Passwd']),
        group_id=1, )
    )
    session.commit()
