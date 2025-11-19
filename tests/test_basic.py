from toonlite import loads, dumps


def test_roundtrip_simple():
    data = {
        "name": "Alice",
        "age": 30,
        "address": {"city": "Bengaluru", "zip": 560001},
        "skills": ["Python", "ML"],
        "active": True,
        "pi": 3.14,
        "notes": None,
    }

    text = dumps(data)
    parsed = loads(text)

    assert parsed == data
