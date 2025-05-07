from shiftapp import app, db
from shiftapp.models import User

with app.app_context():
    # Wipe and recreate
    db.drop_all()
    db.create_all()

    # Create dummies :D
    admin = User(username='admin', password='admin', role='admin')
    employee = User(username='john', password='pass', role='employee')

    # Add
    db.session.add(admin)
    db.session.add(employee)
    db.session.commit()

    print("Dummies Generated.")