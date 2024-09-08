from prompt.prompt_template import dynamic_prompt
from utils.dynamic_utils import build_diction_from_model
from utils.count_utils import count_points
import concurrent.futures
from openai import OpenAI
from tqdm import tqdm
import argparse
import json
import time
import csv
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

parser = argparse.ArgumentParser()
parser.add_argument("--course", "-c", type=str, help="Course name", required=True)
parser.add_argument("--thread", "-t", type=int, help="Number of threads", default=3)
args = parser.parse_args()

course = args.course

global data, prompt, example_dict
data = None
prompt = None
example_dict = {}

if not os.path.exists("results/dynamic/short"):
    print("Creating results/dynamic/short directory...")
    os.makedirs("results/dynamic/short")
if not os.path.exists(f"results/dynamic/short/{course}"):
    print(f"Creating results/dynamic/short/{course} directory...")
    os.makedirs(f"results/dynamic/short/{course}")

with open(f"data/short/{course}/{course}_CSV1.csv", "r") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    rows = list(csv_reader)
    db_data = {}
    for row in rows:
        example_text = row[4]
        parts = re.split(r"\n(?=<Point)", example_text, maxsplit=1)
        example_stu_answer = parts[0].strip()
        example_feedback = parts[1].strip() if len(parts) > 1 else ""
        example_dict[row[0]] = {
            "example_stu_answer": example_stu_answer,
            "example_feedback": example_feedback,
        }
        db_data[row[0]] = {
            "question": row[1],
            "fullMark": row[2],
            "referenceAnswer": row[3],
            "num_points": count_points(row[3]),
        }

with open(f"data/short/{course}/{course}_CSV2.csv", "r") as file:
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
                "studentAnswer": row[1],
                "teacherMark": row[2].split("\n")[1].strip('"'),
            }
        )


def get_single_response(entry, prompt):
    global example_dict
    question = entry["question"]
    full_mark = entry["fullMark"]
    ref_answer = entry["referenceAnswer"]
    stu_answer = entry["studentAnswer"]
    num_points = entry["num_points"]
    example_stu_answer = example_dict[entry["question_code"]]["example_stu_answer"]
    example_feedback = example_dict[entry["question_code"]]["example_feedback"]
    query = prompt.format(
        question=question,
        ref_answer=ref_answer,
        stu_answer=stu_answer,
        full_mark=full_mark,
        num_points=num_points,
        example_stu_answer=example_stu_answer,
        example_feedback=example_feedback,
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
        temperature=1,
    )
    text = completion.choices[0].message.content
    return text, model


def get_responses(entry, prompt):
    global example_dict
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.thread) as executor:
        futures = [
            executor.submit(get_single_response, entry, prompt)
            for _ in range(args.thread)
        ]
        results = [
            future.result() for future in concurrent.futures.as_completed(futures)
        ]

    for i, (text, model_name) in enumerate(results, 1):
        entry[f"feedback_{i}"] = text

    has_diff, final_feedback, final_points_dict, mismatch_count, num_of_total_points = (
        build_diction_from_model(
            results,
            entry["num_points"],
            entry["teacherMark"],
            args.thread,
            entry["question"],
            entry["referenceAnswer"],
            entry["studentAnswer"],
        )
    )
    if has_diff:
        example_dict[entry["question_code"]]["example_stu_answer"] = entry[
            "studentAnswer"
        ]
        example_dict[entry["question_code"]]["example_feedback"] = final_feedback
    entry["model_name"] = model_name
    entry["feedback"] = final_feedback
    entry["feedback_dict"] = final_points_dict
    entry["mismatch_count"] = mismatch_count
    entry["num_of_total_points"] = num_of_total_points
    return entry


def process_data():
    global prompt, data
    results = {}

    def process_entry(index_entry):
        index, entry = index_entry
        updated_entry = get_responses(entry.copy(), prompt)

        return index, updated_entry

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.thread) as executor:
        futures = [
            executor.submit(process_entry, (index, entry))
            for index, entry in enumerate(data)
        ]

        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(data),
            desc=f"Processing {course}",
        ):
            index, updated_entry = future.result()
            results[index] = updated_entry
            time.sleep(30)

    with open(f"results/dynamic/short/{course}/{model}.json", "w") as file:
        json.dump(results, file, indent=4)


prompt = dynamic_prompt
process_data()
