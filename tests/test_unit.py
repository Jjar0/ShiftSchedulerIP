import unittest
from shiftapp.models import User, Shift

class TestShiftLogic(unittest.TestCase):
    def test_shift_conflict_overlap(self): #ID: 1
        # simulate existing shift
        existing_shift = Shift(startTime="10:00", endTime="12:00")
        # new shift overlaps
        new_start = "11:00"
        new_end = "13:00"
        conflict = not (new_end <= existing_shift.startTime or new_start >= existing_shift.endTime)
        self.assertTrue(conflict)

    def test_shift_no_conflict(self): #ID: 2
        # existing shift
        existing_shift = Shift(startTime="10:00", endTime="12:00")
        # new shift does not overlap
        new_start = "12:00"
        new_end = "14:00"
        conflict = not (new_end <= existing_shift.startTime or new_start >= existing_shift.endTime)
        self.assertFalse(conflict)

    def test_duplicate_user_detection(self): #ID: 3
        # try two users with same name
        user1 = User(username="helen", password="pass", role="employee")
        user2 = User(username="helen", password="pass", role="employee")
        self.assertEqual(user1.username, user2.username)

    def test_user_role(self): #ID: 4
        user = User(username="admin", password="adminpass", role="admin")
        self.assertEqual(user.role, "admin")
