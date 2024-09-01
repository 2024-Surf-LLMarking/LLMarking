from sklearn.metrics import f1_score, precision_score, recall_score
from .dynamic_utils import extract_dynamic_info
import json
import re
import os


def extract_info(data):
    Teacher_Marklist = []
    Model_Marklist = []
    mismatch_count = 0
    total = 0

    for key, value in data.items():
        teacher_mark = build_diction_from_teacher(value.get("teacherMark"))
        total += len(teacher_mark)
        model_mark, mismatch_count_per_question = build_diction_from_model(
            value.get("feedback"), len(teacher_mark), teacher_mark
        )
        if mismatch_count_per_question:
            mismatch_count += mismatch_count_per_question

        Teacher_Marklist.append(teacher_mark)
        Model_Marklist.append(model_mark)

    if mismatch_count > 0:
        mismatch_percentage = (mismatch_count / total) * 100
    else:
        mismatch_percentage = 0
    return Model_Marklist, Teacher_Marklist, mismatch_percentage


def build_diction_from_model(input_str, length, teacher_mark):
    # 正则表达式模式来匹配 Point 和 类型
    points_dict = {}
    mismatch_count = 0
    pattern = re.compile(
        r"<(Point\d+)\s*:\w+\s*>\s*\*?(True|False)\*?\s*\n?\(?([^)]*)\)?"
    )
    original_input_str_list = re.findall(pattern, input_str)
    original_input_str_list_length = len(original_input_str_list)
    if original_input_str_list_length != length:
        if original_input_str_list_length < length:
            mismatch_count = length - original_input_str_list_length
            for point in teacher_mark:
                if point not in [point[0] for point in original_input_str_list]:
                    if teacher_mark[point] == "True":
                        points_dict[point] = "False"
                    else:
                        points_dict[point] = "True"
        else:
            mismatch_count = length
            for point in teacher_mark:
                if point[1] == "True":
                    points_dict[point] = "False"
                else:
                    points_dict[point] = "True"
            return points_dict, mismatch_count
    for match in re.finditer(pattern, input_str):
        point, type_, comment = match.groups()
        points_dict[point] = type_
    return points_dict, mismatch_count


def build_diction_from_teacher(input_str):
    # 正则表达式模式来匹配 Point 和 类型
    points_dict = {}
    pattern = re.compile(r"<(Point\d+):(\w+)>")
    for match in re.finditer(pattern, input_str):
        point, type_ = match.groups()
        points_dict[point] = type_
    return points_dict


def extract_info_from_json(file_path, dynamic=False):
    # Read the JSON file
    if os.path.exists(file_path) == False:
        print("The file does not exist!\n\n")
        return None, None, None, None
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        if dynamic:
            ModelMark, TeacherMark, mismatch_percentage = extract_dynamic_info(data)
        else:
            ModelMark, TeacherMark, mismatch_percentage = extract_info(data)
        # print("ModelMark\t", ModelMark)
        # print("TeacherMark\t", TeacherMark)
        model_points = extract_points(ModelMark)
        teacher_points = extract_points(TeacherMark)
        model_labels = [1 if point == "True" else 0 for point in model_points]
        teacher_labels = [1 if point == "True" else 0 for point in teacher_points]
        f1, precision, recall = get_score(teacher_labels, model_labels)
        print("F1 score:\t", f1)
        print("Precision score:", precision)
        print("Recall score:\t", recall)
        print(f"Mismatch percentage: {mismatch_percentage:2f}%\n\n")
        return f1, precision, recall, mismatch_percentage


# 提取点并将其转换为列表
def extract_points(marks):
    return [point for mark in marks for point in mark.values()]


def get_score(teacher_labels, model_labels):
    # print("Model Labels\t", model_labels)
    # print("Teacher Labels\t", teacher_labels)
    f1 = f1_score(teacher_labels, model_labels)
    precision = precision_score(teacher_labels, model_labels)
    recall = recall_score(teacher_labels, model_labels)
    return f1, precision, recall


if __name__ == "__main__":
    extract_info_from_json(r"../results/short/example/v1/zeroshot/Qwen1.5-14B.json")
