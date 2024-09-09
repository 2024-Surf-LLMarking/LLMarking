from prompt.prompt_template_long import prompt_list
from concurrent.futures import ThreadPoolExecutor
from utils.count_utils import count_cases
from openai import OpenAI
from tqdm import tqdm
import threading
import argparse
import json
import csv
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

parser = argparse.ArgumentParser()
parser.add_argument("--course", "-c", type=str, help="Course name", required=True)
parser.add_argument("--thread", "-t", type=int, help="Number of threads", default=10)
parser.add_argument(
    "--prompt",
    "-p",
    type=int,
    help="Prompt type to use.",
    required=True,
    choices=[3],
)
args = parser.parse_args()

directory = ["zeroshot", "oneshot", "fewshot"]
course = args.course
model_name = None
num_thread = args.thread

global data, question_code_to_example_dict
data = None
question_code_to_example_dict = {}

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
        example_text_1 = row[5]
        example_text_2 = row[6]
        example_text_3 = row[7]
        parts_1 = re.split(r"\n(?=<Point)", example_text_1, maxsplit=1)
        parts_2 = re.split(r"\n(?=<Point)", example_text_2, maxsplit=1)
        parts_3 = re.split(r"\n(?=<Point)", example_text_3, maxsplit=1)
        example_stu_answer_1 = parts_1[0].strip()
        example_feedback_1 = parts_1[1].strip() if len(parts_1) > 1 else ""
        example_stu_answer_2 = parts_2[0].strip()
        example_feedback_2 = parts_2[1].strip() if len(parts_2) > 1 else ""
        example_stu_answer_3 = parts_3[0].strip()
        example_feedback_3 = parts_3[1].strip() if len(parts_3) > 1 else ""
        db_data[row[0]] = {
            "question": row[1],
            "fullMark": row[2],
            "referenceAnswer": row[3],
            "note": row[4],
            "num_points": count_cases(row[3]),
        }
        question_code_to_example_dict[row[0]] = {
            "example_stu_answer_1": example_stu_answer_1,
            "example_feedback_1": example_feedback_1,
            "example_stu_answer_2": example_stu_answer_2,
            "example_feedback_2": example_feedback_2,
            "example_stu_answer_3": example_stu_answer_3,
            "example_feedback_3": example_feedback_3,
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
                "num_points": db_data[row[0]]["num_points"],
                "referenceAnswer": db_data[row[0]]["referenceAnswer"],
                "note": db_data[row[0]]["note"],
                "studentAnswer": row[1],
                "teacherMark": row[2].split("\n")[1].strip('"'),
            }
        )


def get_response(i, stream=False):
    global prompt, data, model_name, question_code_to_example_dict
    results = {}
    pbar = tqdm(total=len(data), desc=f"Processing {directory[i]}")

    def process_entry(index):
        global model_name
        entry = data[index]
        question = entry["question"]
        full_mark = entry["fullMark"]
        ref_answer = entry["referenceAnswer"]
        stu_answer = entry["studentAnswer"]
        num_points = entry["num_points"]
        note = entry["note"]
        if i == 0:
            query = prompt.format(
                question=question,
                ref_answer=ref_answer,
                stu_answer=stu_answer,
                full_mark=full_mark,
                num_points=num_points,
                note=note,
            )
        elif i == 1:
            query = prompt.format(
                question=question,
                ref_answer=ref_answer,
                stu_answer=stu_answer,
                full_mark=full_mark,
                num_points=num_points,
                note=note,
                example_stu_answer_1=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_stu_answer_1"],
                example_feedback_1=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_feedback_1"],
            )
        elif i == 2:
            query = prompt.format(
                question=question,
                ref_answer=ref_answer,
                stu_answer=stu_answer,
                full_mark=full_mark,
                num_points=num_points,
                note=note,
                example_stu_answer_1=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_stu_answer_1"],
                example_feedback_1=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_feedback_1"],
                example_stu_answer_2=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_stu_answer_2"],
                example_feedback_2=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_feedback_2"],
                example_stu_answer_3=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_stu_answer_3"],
                example_feedback_3=question_code_to_example_dict[
                    entry["question_code"]
                ]["example_feedback_3"],
            )

        completion = client.chat.completions.create(
        model=model,
        messages=[
                {
                    "role": "system",
                    "content": "You are an impartial, objective AI grading assistant.",
                },
                {"role": "user", "content": query},
            ],
            temperature=0.0,
        )
        text = completion.choices[0].message.content
        model_name = model
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


for i in range(len(directory)):
    prompt = prompt_list[i]
    get_response(i, False)
