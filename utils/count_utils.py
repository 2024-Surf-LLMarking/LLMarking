import re


def count_points(text):
    # Regular expression to match point patterns
    pattern = r"<Point\d+:\d+>"

    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Count unique point numbers
    unique_points = set(match.split(":")[0] for match in matches)
    return len(unique_points)

def count_cases(text):
    # Regular expression to match case patterns
    pattern = r"<Point\d+_case\d+:\d+>"

    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Count unique case numbers
    unique_cases = set(matches)
    return len(unique_cases)


if __name__ == "__main__":
    # Example usage
    text = """<Point1_case1:1>Development testing<Point1_case1:1> <Point2_case1:1>where the system is tested during development to discover bugs and defects.<Point2_case1:1> <Point3_case1:1>Release testing<Point3_case1:1> <Point4_case1:1>where a separate testing team test a complete version of the system before it is released to users.<Point4_case1:1> <Point5_case1:1>User testing<Point5_case1:1> <Point5_case2:1>where users or potential users of a system test the system in their own environment.<Point5_case2:1>"""
    num_cases = count_cases(text)
    print(f"Number of cases detected: {num_cases}")
