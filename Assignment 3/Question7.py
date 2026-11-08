import time
# Normalize phone numbers
def norm_phone(p):
    digits = "".join(
        ch for ch in str(p or "") if ch.isdigit()
    )

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    return digits
# Normalize email addresses
def norm_email(e):
    return str(e).strip().lower() if e else ""
# Merge contacts using dictionary and set operations
def merge_contacts(contacts):
    groups = {}
    phone_index = {}
    next_id = 0
    for contact in contacts:
        phones = {
            norm_phone(p)
            for p in contact.get("phones", [])
        }
        phones.discard("")
        emails = {
            norm_email(e)
            for e in contact.get("emails", [])
        }
        emails.discard("")
        name = str(contact.get("name") or "").strip()

        matched = {
            phone_index[p]
            for p in phones
            if p in phone_index
        }
        if not matched:
            group_id = next_id
            next_id += 1
            groups[group_id] = {
                "name": name,
                "names": {name} if name else set(),
                "phones": set(),
                "emails": set()
            }
        else:
            group_id = min(matched)
            # Merge multiple matching groups
            for old_id in matched:
                if old_id != group_id:
                    groups[group_id]["names"].update(
                        groups[old_id]["names"]
                    )
                    groups[group_id]["phones"].update(
                        groups[old_id]["phones"]
                    )
                    groups[group_id]["emails"].update(
                        groups[old_id]["emails"]
                    )
                    del groups[old_id]

                    for phone, owner in list(phone_index.items()):
                        if owner == old_id:
                            phone_index[phone] = group_id
        group = groups[group_id]
        if name:
            group["names"].add(name)

        group["phones"].update(phones)
        group["emails"].update(emails)
        for phone in phones:
            phone_index[phone] = group_id
    result = []
    for group in groups.values():
        names = sorted(group["names"])
        result.append({
            "name": names[0] if names else "",
            "names": names,
            "phones": sorted(group["phones"]),
            "emails": sorted(group["emails"])
        })
    return result
# Pairwise comparison approach
def pairwise_same(a, b):
    phones_a = {
        norm_phone(x)
        for x in a.get("phones", [])
    } - {""}
    phones_b = {
        norm_phone(x)
        for x in b.get("phones", [])
    } - {""}
    return bool(phones_a & phones_b)
def pairwise_comparisons(contacts):
    matches = []
    for i in range(len(contacts)):
        for j in range(i + 1, len(contacts)):
            if pairwise_same(contacts[i], contacts[j]):
                matches.append((i, j))
    return matches
# Sample contact data
sample_contacts = [
    {
        "name": "Anu",
        "phones": ["+91 98400 12345"],
        "emails": ["ANU@example.com"]
    },
    {
        "name": "Anu Kumar",
        "phones": ["9840012345"],
        "emails": ["anu@example.com"]
    },
    {
        "name": "Ravi",
        "phones": ["+91 90000 11111"],
        "emails": ["ravi@example.com"]
    },
    {
        "name": "Priya",
        "phones": [],
        "emails": ["priya@example.com"]
    },
    {
        "name": "Kumar",
        "phones": ["9000011111"],
        "emails": ["kumar@example.com"]
    }
]
# Display merged sample contacts
print("MERGED SAMPLE CONTACTS:")
merged = merge_contacts(sample_contacts)
for contact in merged:
    print(contact)
# Validation tests
print("\nVALIDATION TESTS")
print(
    "Same phone, different formatting:",
    len(merge_contacts(sample_contacts)) == 3
)
print(
    "Empty input:",
    merge_contacts([]) == []
)
print(
    "Missing phone preserved:",
    any(
        "priya@example.com" in contact["emails"]
        for contact in merged
    )
)
print(
    "Duplicate email removed:",
    len(merged[0]["emails"]) == len(set(merged[0]["emails"]))
)
# Generate synthetic contact data
def make_data(n):
    data = []

    for i in range(n):
        person = i // 2

        data.append({
            "name": "Person " + str(person),
            "phones": [
                f"+91 90000 {person:05d}"
            ],
            "emails": [
                f"person{person}@example.com"
            ]
        })

    return data
# Dictionary merge benchmark
print("\nDICTIONARY MERGE BENCHMARK")
for n in (1000, 100000):
    data = make_data(n)

    start = time.perf_counter()
    result = merge_contacts(data)
    dictionary_time = time.perf_counter() - start

    print(
        n,
        "contacts |",
        len(result),
        "groups |",
        round(dictionary_time, 6),
        "seconds"
    )
# Pairwise benchmark
# 1000 contacts = 499,500 comparisons.
print("\nPAIRWISE COMPARISON BENCHMARK")
data = make_data(1000)
start = time.perf_counter()
matches = pairwise_comparisons(data)
pairwise_time = time.perf_counter() - start
print(
    "1000 contacts |",
    len(matches),
    "matches |",
    round(pairwise_time, 6),
    "seconds"
)
print(
    "100000 contacts | Pairwise comparison not run "
    "(4,999,950,000 comparisons would be required)"
)
