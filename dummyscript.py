from shiftapp import app, db
from shiftapp.models import User, Shift

with app.app_context():
    # wipe existing data
    db.drop_all()
    db.create_all()

    # create users
    admin = User(username='admin', password='admin', role='admin')
    john = User(username='john', password='pass', role='employee')
    helen = User(username='helen', password='pass', role='employee')
    mark = User(username='mark', password='pass', role='employee')

    db.session.add_all([admin, john, helen, mark])
    db.session.commit()

    # create shifts
    shifts = [
        # helen
        Shift(date='2025-05-21', startTime='09:00', endTime='13:00', assignedTo=helen.id),
        Shift(date='2025-05-22', startTime='14:00', endTime='18:00', assignedTo=helen.id),

        # john
        Shift(date='2025-05-21', startTime='10:00', endTime='16:00', assignedTo=john.id),

        # mark
        Shift(date='2025-05-23', startTime='08:00', endTime='12:00', assignedTo=mark.id)
    ]

    db.session.add_all(shifts)
    db.session.commit()

    print("Dummy users and shifts created.")
