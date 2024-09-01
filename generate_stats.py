from utils.compute_mark import build_diction_from_teacher
import csv

course_name = ["CPT", "INT", "FIN"]
directory = ["zeroshot", "oneshot", "fewshot"]
columns = ["Subject", "Question", "Total number of points", "Student answer"]
rows = []

for course in course_name:
    with open(f"data/short/{course}/{course}_CSV1.csv", "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        question_num = len(list(csv_reader))

    with open(f"data/short/{course}/{course}_CSV2.csv", "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data_rows = list(csv_reader)
        student_answer_num = len(data_rows)
        course_db = {}
        total_points = 0
        for question_code, _, teacher_mark in data_rows:
            if question_code in course_db:
                total_points += course_db[question_code]
            else:
                teacher_mark_dict = build_diction_from_teacher(teacher_mark)
                total_points += len(teacher_mark_dict)
                course_db[question_code] = len(teacher_mark_dict)
        print(course_db)
    rows.append([course, question_num, total_points, student_answer_num])

with open("data/short/stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(rows)
