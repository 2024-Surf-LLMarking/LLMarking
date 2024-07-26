from utils.compute_mark import extract_info_from_json
import pathlib as pl
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--course", "-c", type=str, help="Course name", required=True)
args = parser.parse_args()

course = args.course

model_name_list_few = pl.Path(f'results/short/{course}/fewshot').glob('*')
model_name_list_few = [i.name.split('.jso')[0] for i in list(model_name_list_few)]

model_name_list_one = pl.Path(f'results/short/{course}/oneshot').glob('*')
model_name_list_one = [i.name.split('.jso')[0] for i in list(model_name_list_one)]

model_name_list_zero = pl.Path(f'results/short/{course}/zeroshot').glob('*')
model_name_list_zero = [i.name.split('.jso')[0] for i in list(model_name_list_zero)]

model_name_list = list(set(model_name_list_few) | set(model_name_list_one) | set(model_name_list_zero))
model_name_list = sorted(model_name_list)

directory = ["zeroshot", "oneshot", "fewshot"]

eval_results = []
for model_name in model_name_list:
    row = [model_name]
    for d in directory:
        print(f"Processing {d} for {model_name}")
        f1, precision, recall = extract_info_from_json(f'results/short/{course}/{d}/{model_name}.json')
        cell = f"""F1 score:\t{f1}\nPrecision score: {precision}\nRecall score:\t{recall}"""
        row.append(cell)
    eval_results.append(row)
    with open(f'results/short/{course}/{course}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Model Name", "Zero-shot", "One-shot", "Few-shot"])
        writer.writerows(eval_results)