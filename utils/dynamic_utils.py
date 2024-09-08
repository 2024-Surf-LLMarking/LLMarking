from prompt.prompt_template import dynamic_prompt_for_feedback
import numpy as np
import requests
import json
import re


def extract_dynamic_info(data, long=False):
    Teacher_Marklist = []
    Model_Marklist = []
    mismatch_count = 0
    total = 0

    for key, value in data.items():
        teacher_mark = build_diction_from_teacher(value.get("teacherMark"), long=long)
        model_mark = value.get("feedback_dict")
        total += value.get("num_of_total_points")
        mismatch_count += value.get("mismatch_count")

        Teacher_Marklist.append(teacher_mark)
        Model_Marklist.append(model_mark)

    if mismatch_count > 0:
        mismatch_percentage = (mismatch_count / total) * 100
    else:
        mismatch_percentage = 0
    return Model_Marklist, Teacher_Marklist, mismatch_percentage


def build_diction_from_model(
    feedbacks,
    length,
    teacher_mark,
    thread,
    question,
    ref_answer,
    stu_answer,
    long=False,
):
    teacher_mark_dict = build_diction_from_teacher(teacher_mark, long=long)
    points_dict = {point: [] for point in teacher_mark_dict}
    points_dict_value = {}
    mismatch_count = 0
    has_diff = False
    num_of_total_points = length * len(feedbacks)
    pattern = re.compile(
        r"<(Point\d+)\s*:(\w+)\s*>\s*\*?(True|False)\*?\s*\n?\(?([^)]*)\)?"
    )

    if long:
        pattern = re.compile(
            r"<\s*([^>]+)\s*:\s*(\d+)\s*>\s*\*?(True|False)\*\s*\(?(.*)\)?"
        )

    for feedback, model_name in feedbacks:
        matches = list(re.finditer(pattern, feedback))
        num_matches = len(matches)
        if num_matches > length:
            mismatch_count += length
        elif num_matches <= length:
            mismatch_count += length - num_matches

        points_matched_per_feedback = []

        try:
            for match in re.finditer(pattern, feedback):
                point, point_value, type_, comment = match.groups()
                points_matched_per_feedback.append(point)
                # The number (3) here can vary depending on the number of feedbacks (threads)
                if len(points_dict[point]) < thread:
                    points_dict[point].append(type_)
                points_dict_value[point] = point_value
        except:
            print(
                f"Error! points_dict: {points_dict}, points_dict_value: {points_dict_value}, teacher_mark_dict: {teacher_mark_dict}, feedback: {feedback}"
            )

        for point in teacher_mark_dict:
            if point not in points_matched_per_feedback:
                if teacher_mark_dict[point] == "True":
                    points_dict[point].append("False")
                else:
                    points_dict[point].append("True")

    for point in points_dict:
        assert (
            len(points_dict[point]) == len(feedbacks)
        ), f"Length of points_dict[{point}] is not equal to the number of feedbacks!\n\nFeedbacks: {feedbacks}\n\nPoints_dict: {points_dict[point]}"

    final_points_dict = None
    final_feedback = None
    if fleiss_kappa(points_dict) >= 0.6:
        final_points_dict = {}
        final_feedback = ""

        for point, values in points_dict.items():
            true_count = values.count("True")
            false_count = values.count("False")
            # # Note: The number there (2) can vary depending on the number of feedbacks (threads)
            # if true_count != thread and false_count != thread:
            #     has_diff = True
            final_points_dict[point] = "True" if true_count > false_count else "False"

            try:
                final_feedback += f"<{point}:{points_dict_value[point]}> "
            except:
                print(
                    f"Point values not found! point: {point}, points_dict_value: {points_dict_value}, feedbacks: {feedbacks} | using default value 2"
                )
                final_feedback += f"<{point}:2> "
            if final_points_dict[point] == "True":
                final_feedback += "*True* "
            else:
                final_feedback += "*False* "

            for feedback, model_name in reversed(feedbacks):
                try:
                    match = re.finditer(pattern, feedback)
                except:
                    print(f"Error! feedback: {feedback}")
                for m in match:
                    if m and m.group(1) == point:
                        comment = m.group(4).strip()
                        if comment:
                            final_feedback += f"({comment})\n\n"
                            break
                break

        final_feedback = final_feedback.rstrip("\n\n")
    else:
        has_diff = True
        final_points_dict = teacher_mark_dict
        query = dynamic_prompt_for_feedback.format(
            question=question,
            ref_answer=ref_answer,
            stu_answer=stu_answer,
            teacher_mark=teacher_mark,
        )
        response = requests.post(
            # "http://192.168.0.72:8000/chat",
            "http://localhost:8888/chat",
            json={
                "query": query,
                "stream": False,
                "history": None,
            },
            stream=False,
        )
        final_feedback = json.loads(response.text)["text"]
    return (
        has_diff,
        final_feedback,
        final_points_dict,
        mismatch_count,
        num_of_total_points,
    )


def build_diction_from_teacher(input_str, long=False):
    points_dict = {}
    pattern = re.compile(r"<(Point\d+):(\w+)>")
    if long:
        pattern = re.compile(r"<\s*([^>]+)\s*:\s*(\w+)\s*>")
    for match in re.finditer(pattern, input_str):
        point, type_ = match.groups()
        points_dict[point] = type_
    return points_dict


def fleiss_kappa(points_dict):
    ratings = []
    for point, values in points_dict.items():
        row = [values.count("True"), values.count("False")]
        ratings.append(row)
    ratings = np.array(ratings)
    n, c = ratings.shape
    P_i = np.sum(ratings * (ratings - 1), axis=1) / (
        ratings.sum(axis=1) * (ratings.sum(axis=1) - 1)
    )
    P_bar = np.mean(P_i)
    p_j = ratings.sum(axis=0) / (n * ratings.sum())
    P_e = np.sum(p_j**2)
    kappa = (P_bar - P_e) / (1 - P_e)
    return kappa


if __name__ == "__main__":
    points_dict = {
        "Point1": ["True", "True", "False"],
        "Point2": ["True", "False", "False"],
        "Point3": ["False", "False", "False"],
        "Point4": ["False", "False", "False"],
    }
    print(fleiss_kappa(points_dict))
