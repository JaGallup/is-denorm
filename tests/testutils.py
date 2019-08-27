def assert_strings(strings, parser, tokanizer):
    for s, target in strings:
        try:
            parsed = parser.parse(tokanizer(s), s)
            assert parsed == target
            print("Success: ", parsed, "==", target)
        except AssertionError:
            print("Failed: ", parsed, "!=", target)
