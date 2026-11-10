class InvalidRegistration(Exception):
    """Raised when a fest registration record is invalid."""


def validate_email(email):
    email = email.strip()
    if any(ch.isspace() for ch in email):
        return False
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        return False
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    return True


def parse_registration(row):
    if len(row) != 5:
        raise InvalidRegistration(f"expected 5 fields, found {len(row)}")

    reg, name, department, email, event_text = [x.strip() for x in row]

    if not all([reg, name, department, email, event_text]):
        raise InvalidRegistration("all five fields are required")
    if not validate_email(email):
        raise InvalidRegistration("invalid email address")

    events = [event.strip() for event in event_text.split(";") if event.strip()]
    if not events:
        raise InvalidRegistration("at least one event is required")

    return {
        "register_no": reg,
        "name": name,
        "department": department,
        "email": email,
        "events": sorted(set(events)),
    }
