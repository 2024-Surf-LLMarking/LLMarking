import re

def extract_info(data):
    Teacher_Marklist = []
    Model_Marklist = []
    mismatch_count = 0
    total = 0

    for key, value in data.items():
        teacher_mark = build_diction_from_teacher(value.get("teacherMark"))
        total += len(teacher_mark)
        
        feedbacks = [value.get(f"feedback_{i}") for i in range(1, 4) if value.get(f"feedback_{i}")]
        
        model_mark, mismatch_count_per_question, num_of_total_points = build_diction_from_model(feedbacks, len(teacher_mark), teacher_mark)
        if mismatch_count_per_question:
            mismatch_count += mismatch_count_per_question
        total += num_of_total_points
        
        Teacher_Marklist.append(teacher_mark)
        Model_Marklist.append(model_mark)

    mismatch_percentage = (mismatch_count / total) * 100 if mismatch_count > 0 else 0
    return Model_Marklist, Teacher_Marklist, mismatch_percentage

def build_diction_from_model(feedbacks, length, teacher_mark):
    points_dict = {point: [] for point in teacher_mark}
    mismatch_count = 0
    num_of_total_points = length*len(feedbacks)
    pattern = re.compile(r'<(Point\d+)\s*:\w+\s*>\s*\*?(True|False)\*?\s*\n?\(?([^)]*?)\)?')
    
    for feedback in feedbacks:

        matches = list(re.finditer(pattern, feedback))
        num_matches = len(matches)
        if num_matches > length:
            mismatch_count += length
        elif num_matches <= length:
            mismatch_count += length - num_matches

        points_matched_per_feedback = []

        for match in re.finditer(pattern, feedback):
            point, type_, comment = match.groups()
            points_matched_per_feedback.append(point)
            points_dict[point].append(type_)

        for point in teacher_mark:
            if point not in points_matched_per_feedback:
                if teacher_mark[point] == 'True':
                    points_dict[point].append('False')
                else:
                    points_dict[point].append('True')

    for point in points_dict:
        assert len(points_dict[point]) == len(feedbacks), f"Length of points_dict[{point}] is not equal to the number of feedbacks!\n\nFeedbacks: {feedbacks}\n\nPoints_dict: {points_dict[point]}"

    final_points_dict = {}
    for point, values in points_dict.items():
        true_count = values.count('True')
        false_count = values.count('False')
        final_points_dict[point] = 'True' if true_count > false_count else 'False'
    
    return final_points_dict, mismatch_count, num_of_total_points

def build_diction_from_teacher(input_str):
    points_dict = {}
    pattern = re.compile(r'<(Point\d+):(\w+)>')
    for match in re.finditer(pattern, input_str):
        point, type_ = match.groups()
        points_dict[point] = type_
    return points_dict