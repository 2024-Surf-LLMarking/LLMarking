from prompt.prompt_template_long import prompt_template_long
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import threading
import requests
import argparse
import json
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument("--course", "-c", type=str, help="Course name", required=True)
parser.add_argument(
    "--prompt", "-p", type=int, help="Prompt version", required=True, choices=[3]
)
parser.add_argument("--thread", "-t", type=int, help="Number of threads", default=10)
args = parser.parse_args()

directory = ["zeroshot", "oneshot", "fewshot"]
course = args.course
model_name = None
num_thread = args.thread

global data
data = None

if not os.path.exists("results"):
    print("Creating results directory...")
    os.makedirs("results")
if not os.path.exists(f"results/v{args.prompt}"):
    print(f"Creating results/v{args.prompt} directory...")
    os.makedirs(f"results/v{args.prompt}")

if not os.path.exists(f"results/v{args.prompt}/long"):
    print(f"Creating results/v{args.prompt}/long directory...")
    os.makedirs(f"results/v{args.prompt}/long")
if not os.path.exists(f"results/v{args.prompt}/long/{course}"):
    print(f"Creating results/v{args.prompt}/long/{course} directory...")
    os.makedirs(f"results/v{args.prompt}/long/{course}")
    for d in directory:
        print(f"Creating results/v{args.prompt}/long/{course}/{d} directory...")
        os.makedirs(f"results/v{args.prompt}/long/{course}/{d}")
else:
    for d in directory:
        if not os.path.exists(f"results/v{args.prompt}/long/{course}/{d}"):
            print(f"Creating results/v{args.prompt}/long/{course}/{d} directory...")
            os.makedirs(f"results/v{args.prompt}/long/{course}/{d}")

with open(f"data/long/{course}/{course}_CSV1.csv", "r") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    rows = list(csv_reader)
    db_data = {}
    for row in rows:
        db_data[row[0]] = {
            "question": row[1],
            "fullMark": row[2],
            "referenceAnswer": row[3],
            "note": row[4].strip("\n"),
        }

with open(f"data/long/{course}/{course}_CSV2.csv", "r") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    rows = list(csv_reader)
    data = []
    for row in rows:
        data.append(
            {
                "question_code": row[0],
                "question": db_data[row[0]]["question"],
                "fullMark": db_data[row[0]]["fullMark"],
                "referenceAnswer": db_data[row[0]]["referenceAnswer"],
                "note": db_data[row[0]]["note"],
                "studentAnswer": row[1],
                "teacherMark": row[2].split("\n")[1].strip('"'),
            }
        )


def get_response(i, stream=False):
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
        note = entry["note"]
        query = prompt.format(
            question=question,
            ref_answer=ref_answer,
            stu_answer=stu_answer,
            full_mark=full_mark,
            note=note,
        )

        response = requests.post(
            "http://192.168.0.72:8000/chat",
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

    model_name = model_name if not stream else "streamed_model"
    index_list, results = zip(*results.items())
    sorted_results = {
        index: result
        for index, result in sorted(zip(index_list, results), key=lambda x: x[0])
    }
    with open(
        f"results/v{args.prompt}/long/{course}/{directory[i]}/{model_name}.json", "w"
    ) as file:
        json.dump(sorted_results, file, indent=4)


prompt = prompt_template_long
for i in range(len(directory)):
    get_response(i, False)
