from shiftapp import app, db
from shiftapp.models import User, Shift  # Import Shift model

with app.app_context():
    # Wipe and recreate database
    db.drop_all()
    db.create_all()

    # Create dummy users
    admin = User(username='admin', password='admin', role='admin')
    employee = User(username='john', password='pass', role='employee')

    db.session.add(admin)
    db.session.add(employee)
    db.session.commit()

    # Create dummy shifts assigned to 'john'
    shift1 = Shift(date='2025-05-15', startTime='09:00', endTime='17:00', assignedTo=employee.id)
    shift2 = Shift(date='2025-05-16', startTime='10:00', endTime='18:00', assignedTo=employee.id)

    db.session.add(shift1)
    db.session.add(shift2)
    db.session.commit()

    print("Dummies Generated with Shifts")
