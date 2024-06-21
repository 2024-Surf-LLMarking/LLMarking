import json
from sklearn.metrics import f1_score, precision_score, recall_score
import re

def extract_info(data):
    Model_Marklist =[]
    Teacher_Marklist =[]

    for key, value in data.items():
        Model_Marklist.append(build_diction(value.get("feedback")))
        Teacher_Marklist.append(build_diction(value.get("teacherMark")))
    return Model_Marklist,Teacher_Marklist

def build_diction(input_str):
    # 正则表达式模式来匹配 Point 和 类型
    points_dict = {}
    pattern = re.compile(r'<(Point\d+):\d+> <(Induction|Deduction)>')
    for match in re.finditer(pattern, input_str):
        point, type_ = match.groups()
        points_dict[point] = type_
    return points_dict

def extract_info_from_json(file_path):
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file )
        ModelMark, TeacherMark = extract_info(data)
        print("ModelMark", ModelMark)
        print("TeacherMark", TeacherMark)
        model_points = extract_points(ModelMark)
        teacher_points = extract_points(TeacherMark)
        model_labels = [1 if point == 'Induction' else 0 for point in model_points]
        teacher_labels = [1 if point == 'Induction' else 0 for point in teacher_points]
        f1 = F1_Score(teacher_labels,model_labels)
        print(f1)
        print("hello")


# 提取点并将其转换为列表
def extract_points(marks):
    return [point for mark in marks for point in mark.values()]

def F1_Score(teacher_labels,model_labels):
    f1 = f1_score(teacher_labels, model_labels)
    return f1


if __name__ == '__main__':
    extract_info_from_json(r"./results/zeroshot/Qwen1.5-32B.json")