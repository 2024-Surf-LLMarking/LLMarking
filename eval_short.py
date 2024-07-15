from prompt.prompt_template import prompt_list_v1
from tqdm import tqdm
import requests
import json
import csv
import os

def clear_lines():
    print("\033[2J")

directory = ["zeroshot", "oneshot", "fewshot"]
course = "CPT"

global data
data = None

if not os.path.exists('results/short'):
    print("Creating results/short directory...")
    os.makedirs('results/short')
if not os.path.exists(f'results/short/{course}'):
    print(f"Creating results/short/{course} directory...")
    os.makedirs(f'results/short/{course}')
    for d in directory:
        print(f"Creating results/short/{course}/{d} directory...")
        os.makedirs(f'results/short/{course}/{d}')
else:
    for d in directory:
        if not os.path.exists(f'results/short/{course}/{d}'):
            print(f"Creating results/short/{course}/{d} directory...")
            os.makedirs(f'results/short/{course}/{d}')

with open(f'data/short/{course}/{course}_CSV1.csv', 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    rows = list(csv_reader)
    db_data = {}
    for row in rows:
        db_data[row[0]] = {
            "question": row[1],
            "fullMark": row[2],
            "referenceAnswer": row[3]
        }

with open(f'data/short/{course}/{course}_CSV2.csv', 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    rows = list(csv_reader)
    data = []
    for row in rows:
        data.append({
            "question_code": row[0],
            "question": db_data[row[0]]["question"],
            "fullMark": db_data[row[0]]["fullMark"],
            "referenceAnswer": db_data[row[0]]["referenceAnswer"],
            "studentAnswer": row[1],
            "teacherMark": row[2].split('\n')[1].strip('"'),
        })

def get_response(i, stream = False):
    global prompt, data
    index = 0
    results = {}
    pbar = tqdm(total=len(data), desc=f"Processing {directory[i]}")
    while index < len(data):
        question = data[index]["question"]
        full_mark = data[index]["fullMark"]
        ref_answer = data[index]["referenceAnswer"]
        stu_answer = data[index]["studentAnswer"]
        query = prompt.format(question=question, ref_answer=ref_answer, stu_answer=stu_answer, full_mark=full_mark)

        response = requests.post(
            "http://100.65.8.31:8000/chat",
            json={
                "query": query,
                "stream": stream,
                "history": None,
            },
            stream=stream,
        )

        if stream:
            # 流式读取http response body, 按\0分割
            for chunk in response.iter_lines(
                chunk_size=8192, decode_unicode=False, delimiter=b"\0"
            ):
                if chunk:
                    data = json.loads(chunk.decode("utf-8"))
                    text = data["text"].rstrip("\r\n")  # 确保末尾无换行

                    # 打印最新内容
                    clear_lines()
                    print("Question:", question, '\n')
                    print("Reference Answer:", ref_answer, '\n')
                    print("Student Answer:", stu_answer, '\n')
                    print("Feedback:", text, '\n\n')
            data[index]["feedback"] = text
            results[index] = data[index]
        else:
            text = json.loads(response.text)["text"]
            print("Question:", question, '\n')
            print("Reference Answer:", ref_answer, '\n')
            print("Student Answer:", stu_answer, '\n')
            print("Feedback:", text, '\n\n')
            data[index]["feedback"] = text
            results[index] = data[index]
            model_name = json.loads(response.text)["model"]
        index += 1
        pbar.update(1)

    if stream:
        with open('results/results.json', 'w') as file:
            json.dump(results, file, indent=4)
    else:
        with open(f'results/short/{course}/{directory[i]}/{model_name}.json', 'w') as file:
            json.dump(results, file, indent=4)
    
for i in range(len(directory)):
    prompt = prompt_list_v1[i]
    get_response(i, False)
