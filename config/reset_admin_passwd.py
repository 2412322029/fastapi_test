from sqlalchemy import func

from api.password import hash_password
from config import Config
from sql.database import get_session
from sql.dbModels import User

if __name__ == '__main__':
    session = next(get_session())
    session.query(User) \
        .filter(User.username == Config['Default_Administrator']) \
        .filter(User.group_id == 1).update({
            'password': hash_password(Config['Default_Passwd']),
            'updated_at': func.now()
    })
    session.commit()
