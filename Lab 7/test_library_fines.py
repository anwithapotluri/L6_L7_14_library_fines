from hypothesis import given, strategies as st
from library_fines import parse_member_id, total_fine, shelf_code


@given(st.text() | st.none())
def test_parse_member_id_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_total_fine_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_shelf_code_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed with: {e!r} on input {s!r}"