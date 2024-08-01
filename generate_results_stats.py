from utils.compute_mark import extract_info_from_json
import pathlib as pl
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--course", "-c", type=str, help="Course name", required=True)
parser.add_argument("--prompt", "-p", type=int, help="Prompt type to use.", required=True, choices=[1, 3])
args = parser.parse_args()

course = args.course

model_name_list_few = pl.Path(f'results/v{args.prompt}/short/{course}/fewshot').glob('*')
model_name_list_few = [i.name.split('.jso')[0] for i in list(model_name_list_few)]

model_name_list_one = pl.Path(f'results/v{args.prompt}/short/{course}/oneshot').glob('*')
model_name_list_one = [i.name.split('.jso')[0] for i in list(model_name_list_one)]

model_name_list_zero = pl.Path(f'results/v{args.prompt}/short/{course}/zeroshot').glob('*')
model_name_list_zero = [i.name.split('.jso')[0] for i in list(model_name_list_zero)]

model_name_list = list(set(model_name_list_few) | set(model_name_list_one) | set(model_name_list_zero))
model_name_list = sorted(model_name_list)

# model_name_list = [input("Please enter the model name: ")]

directory = ["zeroshot", "oneshot", "fewshot"]

eval_results = []
for model_name in model_name_list:
    row = [model_name]
    for d in directory:
        print(f"Processing {d} for {model_name}")
        f1, precision, recall, mismatch_percentage = extract_info_from_json(f'results/v{args.prompt}/short/{course}/{d}/{model_name}.json')
        if f1 is None:
            cell = f"F1 score:                None\nPrecision score: None\nRecall score:        None\nMismatch percentage: None"
        else:
            cell = f"F1 score:                {f1:.4f}\nPrecision score: {precision:.4f}\nRecall score:        {recall:.4f}\nMismatch percentage: {mismatch_percentage:.2f}%"
        row.append(cell)
    eval_results.append(row)
    with open(f'results/v{args.prompt}/short/{course}/{course}.csv', 'w') as file:
    # with open(f'results/v{args.prompt}/short/{course}/{course}.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["Model Name", "Zero-shot", "One-shot", "Few-shot"])
        writer.writerows(eval_results)