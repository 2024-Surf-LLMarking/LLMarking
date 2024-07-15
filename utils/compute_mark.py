import json
from sklearn.metrics import f1_score, precision_score, recall_score
import re
import os

def extract_info(data):
    Teacher_Marklist =[]
    Model_Marklist =[]

    for key, value in data.items():
        teacher_mark = build_diction_from_teacher(value.get("teacherMark"))
        Teacher_Marklist.append(teacher_mark)
        Model_Marklist.append(build_diction_from_model(value.get("feedback"), len(teacher_mark), teacher_mark))
    return Model_Marklist,Teacher_Marklist

def build_diction_from_model(input_str, length, teacher_mark):
    # 正则表达式模式来匹配 Point 和 类型
    points_dict = {}
    pattern = re.compile(r'<(Point\d+)\s*:\w+\s*>\s*\*?(True|False)\*?\s*\n?\(?([^)]*?)\)?')
    original_input_str_list = re.findall(pattern, input_str)
    if len(original_input_str_list) != length:
        if len(original_input_str_list) > length:
            cut_str = '\n\n'.join(input_str.split('\n\n')[:length])
            if len(re.findall(pattern, cut_str)) != length:
                print("No match found! The input string is:", input_str)
                mark_list = input(f"The number of teacher marks are {length}.\nThe teacher mark is as follow:\n {teacher_mark}\n\nPlease input the correct list of point(e.g. 01 or 110):")
                for i in range(length):
                    points_dict[f"Point{i+1}"] = True if mark_list[i] == '1' else False
                return points_dict
            input_str = cut_str
        else:
            print("No match found! The input string is:", input_str)
            mark_list = input(f"The number of teacher marks are {length}.\nThe teacher mark is as follow:\n {teacher_mark}\n\nPlease input the correct list of point(e.g. 01 or 110):")
            for i in range(length):
                points_dict[f"Point{i+1}"] = True if mark_list[i] == '1' else False
            return points_dict
    for match in re.finditer(pattern, input_str):
        point, type_, comment = match.groups()
        points_dict[point] = type_
    return points_dict

def build_diction_from_teacher(input_str):
    # 正则表达式模式来匹配 Point 和 类型
    points_dict = {}
    pattern = re.compile(r'<(Point\d+):(\w+)>')
    for match in re.finditer(pattern, input_str):
        point, type_ = match.groups()
        points_dict[point] = type_
    return points_dict

def extract_info_from_json(file_path):
    # Read the JSON file
    if os.path.exists(file_path) == False:
        print("The file does not exist!")
        return None, None, None
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        ModelMark, TeacherMark = extract_info(data)
        print("ModelMark\t", ModelMark)
        print("TeacherMark\t", TeacherMark)
        model_points = extract_points(ModelMark)
        teacher_points = extract_points(TeacherMark)
        model_labels = [1 if point == 'True' else 0 for point in model_points]
        teacher_labels = [1 if point == 'True' else 0 for point in teacher_points]
        f1, precision, recall = get_score(teacher_labels, model_labels)
        print("F1 score:\t", f1)
        print("Precision score:", precision)
        print("Recall score:\t", recall)
        return f1, precision, recall


# 提取点并将其转换为列表
def extract_points(marks):
    return [point for mark in marks for point in mark.values()]

def get_score(teacher_labels,model_labels):
    print("Model Labels\t", model_labels)
    print("Teacher Labels\t", teacher_labels)
    f1 = f1_score(teacher_labels, model_labels)
    precision = precision_score(teacher_labels, model_labels)
    recall = recall_score(teacher_labels, model_labels)
    return f1, precision, recall


if __name__ == '__main__':
    extract_info_from_json(r"../results/short/example/v1/zeroshot/Qwen1.5-14B.json")