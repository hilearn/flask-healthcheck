from api.app import app
from store.models import Reply, GreetingType
from store.database import db
from sqlalchemy.exc import OperationalError


if __name__ == '__main__':
    with app.app_context():
        try:
            Reply.__table__.drop(db.engine)
        except OperationalError:
            print("No car_stats table in database. Creating table car_stats")
        Reply.__table__.create(db.engine)

        db.session.add(Reply(category=GreetingType.FORMAL.value,
                             reply_msg='Hello'))
        db.session.add(Reply(category=GreetingType.CAUSAL.value,
                             reply_msg='Hi'))
        db.session.commit()
        print('done')
