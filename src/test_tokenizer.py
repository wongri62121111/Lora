import json
from lua_tokenizer import LuaTokenizer

def sort_report(report):
    sorted_report = dict(report)
    for key in ["literals", "operators", "variables", "reserved_words"]:
        if "values" in sorted_report[key]:
            sorted_report[key]["values"] = sorted(sorted_report[key]["values"])
        if key == "variables" and "duplicates" in sorted_report[key]:
            sorted_report[key]["duplicates"] = sorted(sorted_report[key]["duplicates"])
    return sorted_report

def run_test(test_file, expected_report):
    tokenizer = LuaTokenizer()
    tokenizer.tokenize(test_file)
    report = tokenizer.generate_report()

    sorted_expected = sort_report(expected_report)
    sorted_actual = sort_report(report)

    print(f"Testing {test_file}...")
    print("Expected:", json.dumps(sorted_expected, indent=4))
    print("Actual:  ", json.dumps(sorted_actual, indent=4))
    assert sorted_actual == sorted_expected, f"Test failed for {test_file}"
    print("✅ Test Passed\n")

# Test 1
run_test("example.lua", {
    "literals": {
        "count": 2,
        "values": ["10", "\"hello\""]
    },
    "operators": {
        "count": 6,
        "values": ["=", "+", "(", ")", ","]
    },
    "variables": {
        "count": 5,
        "values": ["x", "y", "add", "a", "b"],
        "duplicates": ["a", "b"]
    },
    "reserved_words": {
        "count": 5,
        "values": ["local", "function", "end", "return"]
    },
    "total_lines_processed": 6
})
