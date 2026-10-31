import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------
def test_returned_on_time():
    assert late_fine("student", 10, False) == 0

def test_unknown_member():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("alien", 5, False)

def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)

def test_zero_days_valid():
    assert late_fine("student", 0, False) == 0

def test_student_exactly_at_limit():
    assert late_fine("student", 14, False) == 0

def test_student_one_day_late():
    assert late_fine("student", 15, False) == 2

def test_student_late_fine():
    assert late_fine("student", 20, False) == 12

def test_faculty_exactly_at_limit():
    assert late_fine("faculty", 30, False) == 0

def test_faculty_one_day_late():
    assert late_fine("faculty", 31, False) == 1

def test_faculty_late_fine():
    assert late_fine("faculty", 40, False) == 10

def test_guest_fine_exactly_200_not_capped():
    assert late_fine("guest", 54, False) == 200

def test_guest_fine_over_200_capped():
    assert late_fine("guest", 55, False) == 200

def test_damaged_no_late_fine():
    assert late_fine("student", 10, True) == 150

def test_damaged_with_late_fine():
    assert late_fine("student", 15, True) == 152

def test_damaged_with_capped_fine():
    assert late_fine("guest", 100, True) == 350


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

def test_fine_exactly_100_allowed():
    assert can_borrow(1, 100, "student") is True

def test_fine_over_100_denied():
    assert can_borrow(1, 101, "student") is False

def test_fine_over_100_denied_faculty():
    assert can_borrow(1, 101, "faculty") is False

def test_student_two_books_allowed():
    assert can_borrow(2, 0, "student") is True

def test_student_three_books_denied():
    assert can_borrow(3, 0, "student") is False

def test_faculty_nine_books_allowed():
    assert can_borrow(9, 0, "faculty") is True

def test_faculty_ten_books_denied():
    assert can_borrow(10, 0, "faculty") is False


# ---------- renewal_status ----------
def test_renewal_denied_reservation():
    assert renewal_status(0, True, 5) == "denied"

def test_reservation_overrides_limit():
    assert renewal_status(5, True, -3) == "denied"

def test_renewal_limit_reached_exact():
    assert renewal_status(2, False, 5) == "limit reached"

def test_renewal_limit_reached_above():
    assert renewal_status(3, False, 5) == "limit reached"

def test_renewal_overdue():
    assert renewal_status(1, False, -1) == "overdue"

def test_renewal_zero_days_left_ok():
    assert renewal_status(1, False, 0) == "renewed"

def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"