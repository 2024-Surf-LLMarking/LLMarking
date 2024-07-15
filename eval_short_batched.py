from prompt.prompt_template import prompt_list_v1
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import threading
import requests
import json
import csv
import os

directory = ["zeroshot", "oneshot", "fewshot"]
course = "CPT"
model_name = None
num_thread = 3

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
    global prompt, data, model_name
    results = {}
    pbar = tqdm(total=len(data), desc=f"Processing {directory[i]}")
    def process_entry(index):
        global model_name
        entry = data[index]
        question = entry["question"]
        full_mark = entry["fullMark"]
        ref_answer = entry["referenceAnswer"]
        stu_answer = entry["studentAnswer"]
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

        text = json.loads(response.text)["text"]
        model_name = json.loads(response.text)["model"]
        entry["feedback"] = text
        results[index] = entry

        with lock:
            pbar.update(1)

    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=num_thread) as executor:
        executor.map(process_entry, range(len(data)))

    model_name = model_name if not stream else 'streamed_model'
    index_list, results = zip(*results.items())
    sorted_results = {index: result for index, result in sorted(zip(index_list, results), key=lambda x: x[0])}
    with open(f'results/short/{course}/{directory[i]}/{model_name}.json', 'w') as file:
        json.dump(sorted_results, file, indent=4)
    
for i in range(len(directory)):
    prompt = prompt_list_v1[i]
    get_response(i, False)
