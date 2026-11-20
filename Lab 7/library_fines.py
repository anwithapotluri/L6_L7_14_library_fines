import re

LOAN_PERIOD_DAYS = 14
FINE_PER_DAY = 2

_MEMBER_ID_PATTERN = re.compile(r"([A-Za-z]+)-([0-9]+)")
_DAYS_PATTERN = re.compile(r"[0-9]+")


def parse_member_id(member_id):
    """Parse an ID like 'STU-1023' into ('STU', 1023).

    Returns None if the input is not a string or not in LETTERS-DIGITS form.
    """
    if not isinstance(member_id, str):
        return None
    match = _MEMBER_ID_PATTERN.fullmatch(member_id.strip())
    if match is None:
        return None
    member_type, number = match.groups()
    try:
        return member_type.upper(), int(number)
    except ValueError:  # e.g. absurdly long digit strings
        return None


def total_fine(days_csv):
    """Total fine for a CSV of days-kept values (e.g. '10,20,30').

    Entries that are empty, negative, or not whole numbers are skipped.
    Returns 0 if the input is not a string.
    """
    if not isinstance(days_csv, str):
        return 0
    fine = 0
    for token in days_csv.split(','):
        token = token.strip()
        if not _DAYS_PATTERN.fullmatch(token):
            continue
        try:
            days = int(token)
        except ValueError:
            continue
        if days > LOAN_PERIOD_DAYS:
            fine += (days - LOAN_PERIOD_DAYS) * FINE_PER_DAY
    return fine


def shelf_code(title):
    """Two-letter shelf code from the first letters of the first two words.

    Returns None if the title is not a string or has fewer than two words.
    """
    if not isinstance(title, str):
        return None
    words = title.split()
    if len(words) < 2:
        return None
    return (words[0][0] + words[1][0]).upper()


def main():
    print("==== Running parse_member_id ====")
    user_input = input("Enter a member ID (e.g. STU-1023): ")
    result = parse_member_id(user_input)
    if result is None:
        print("Invalid member ID. Use letters, a dash, then digits (e.g. STU-1023).")
    else:
        print("Member Type and Number:", result)

    print("\n==== Running total_fine ====")
    user_input = input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    result = total_fine(user_input)
    print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    user_input = input("Enter a book title with at least two words: ")
    result = shelf_code(user_input)
    if result is None:
        print("Invalid title. Please enter at least two words.")
    else:
        print("Shelf Code:", result)


if __name__ == "__main__":
    main()