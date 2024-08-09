import re

def count_points(text):
    # Regular expression to match point patterns
    pattern = r'<Point\d+:\d+>'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Count unique point numbers
    unique_points = set(match.split(':')[0] for match in matches)
    return len(unique_points)


if __name__ == "__main__":
    # Example usage
    text = """The key phases of the SDLC are: <Point1:1>Requirement Gathering<Point1:1>: <Point2:1>Collecting requirements from stakeholders to understand what needs to be developed<Point2:1>. <Point3:1>System Analysis and Design<Point3:1>: <Point4:1>Analyzing the requirements and creating a blueprint of the system<Point4:1>. <Point5:1>Implementation (Coding) <Point5:1>: <Point6:1>Writing the code as per the design documents<Point6:1>. <Point7:1>Testing<Point7:1>: <Point8:1>Verifying the system against the requirements to identify and fix defects<Point8:1>. <Point9:1>Deployment<Point9:1>: <Point10:1>Releasing the software to the production environment for users<Point10:1>. <Point11:1>Maintenance<Point11:1>: <Point12:1>Ongoing support and enhancement of the software post-deployment<Point12:1>."""

    num_points = count_points(text)
    print(f"Number of points detected: {num_points}")