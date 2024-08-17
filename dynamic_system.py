from prompt.prompt_template import prompt_list_v3
from utils.dynamic_utils import extract_info
from utils.count_utils import count_points
import concurrent.futures
from tqdm import tqdm
import requests
import argparse
import json
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument("--course", "-c", type=str, help="Course name", required=True)
parser.add_argument("--thread", "-t", type=int, help="Number of threads", default=3)
args = parser.parse_args()

directory = ["zeroshot", "oneshot", "fewshot"]
course = args.course

global data, prompt
data = None
prompt = None

if not os.path.exists('results/dynamic/short'):
    print("Creating results/dynamic/short directory...")
    os.makedirs('results/dynamic/short')
if not os.path.exists(f'results/dynamic/short/{course}'):
    print(f"Creating results/dynamic/short/{course} directory...")
    os.makedirs(f'results/dynamic/short/{course}')
    for d in directory:
        print(f"Creating results/dynamic/short/{course}/{d} directory...")
        os.makedirs(f'results/dynamic/short/{course}/{d}')
else:
    for d in directory:
        if not os.path.exists(f'results/dynamic/short/{course}/{d}'):
            print(f"Creating results/dynamic/short/{course}/{d} directory...")
            os.makedirs(f'results/dynamic/short/{course}/{d}')

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

def get_single_response(entry, prompt):
    question = entry["question"]
    full_mark = entry["fullMark"]
    ref_answer = entry["referenceAnswer"]
    stu_answer = entry["studentAnswer"]
    num_points = count_points(ref_answer)
    query = prompt.format(question=question, ref_answer=ref_answer, stu_answer=stu_answer, full_mark=full_mark, num_points=num_points)

    response = requests.post(
        "http://192.168.0.72:8000/chat/dynamic",
        json={
            "query": query,
            "stream": False,
            "history": None,
            "temperature": 1.0
        },
        stream=False,
    )
    text = json.loads(response.text)["text"]
    model_name = json.loads(response.text)["model"]
    return text, model_name

def get_responses(entry, prompt):
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.thread) as executor:
        futures = [executor.submit(get_single_response, entry, prompt) for _ in range(args.thread)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    for i, (text, model_name) in enumerate(results, 1):
        entry[f'feedback_{i}'] = text
    
    entry['model_name'] = model_name
    return entry

def process_data(i):
    global prompt, data
    results = {}
    
    def process_entry(index_entry):
        index, entry = index_entry
        updated_entry = get_responses(entry.copy(), prompt)
        
        Model_Marklist, _, _ = extract_info({index: updated_entry})
        updated_entry['feedback'] = Model_Marklist[0] if Model_Marklist else {}
        
        return index, updated_entry

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.thread) as executor:
        futures = [executor.submit(process_entry, (index, entry)) for index, entry in enumerate(data)]
        
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(data), desc=f"Processing {directory[i]}"):
            index, updated_entry = future.result()
            results[index] = updated_entry

    model_name = results[0]['model_name']
    with open(f'results/dynamic/short/{course}/{directory[i]}/{model_name}.json', 'w') as file:
        json.dump(results, file, indent=4)

for i in range(len(directory)):
    prompt = prompt_list_v3[i]
    process_data(i)