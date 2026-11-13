def mask_card_number(number):
    """
    Hides all but the last four digits of a card number.
    Safely handles None, non-strings, and strings shorter than 4 characters.
    """
    if not isinstance(number, str):
        return None

    digits = "".join(ch for ch in number if ch.isdigit())
    if len(digits) < 4:
        return None

    return "*" * 12 + digits[-4:]


def parse_transaction(line):
    """
    Parses 'date,category,amount' into a (category, amount) tuple.
    Safely handles malformed strings, missing fields, and invalid amounts.
    """
    if not isinstance(line, str):
        return None

    parts = line.split(",")
    if len(parts) < 3:
        return None

    date_str = parts[0].strip()
    category = parts[1].strip().lower()
    amount_str = parts[2].strip().replace(",", "")

    if not date_str or not category or not amount_str:
        return None

    try:
        amount = int(amount_str)
    except ValueError:
        return None

    return category, amount


def parse_statement_total(text):
    """
    Reads the amount from a line such as 'Total: 12,500'.
    Safely handles missing colons, None, and non-numeric values.
    """
    if not isinstance(text, str) or ":" not in text:
        return None

    amount_part = text.split(":", 1)[1].strip().replace(",", "")
    if not amount_part:
        return None

    try:
        return int(amount_part)
    except ValueError:
        return None


def main():
    print("==== Running mask_card_number ====")
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    print("Masked card number:", mask_card_number(value))

    print("\n==== Running parse_transaction ====")
    value = input("Enter a transaction as DATE,CATEGORY,AMOUNT (e.g. 2026-11-05,dining,1550): ")
    print("Category and amount:", parse_transaction(value))

    print("\n==== Running parse_statement_total ====")
    value = input("Enter the statement total line (e.g. Total: 12,500): ")
    print("Statement total:", parse_statement_total(value))


if __name__ == "__main__":
    main()