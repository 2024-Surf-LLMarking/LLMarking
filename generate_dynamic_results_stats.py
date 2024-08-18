from utils.compute_mark import extract_dynamic_info_from_json
import pathlib as pl
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--course", "-c", type=str, help="Course name", required=True)
args = parser.parse_args()

course = args.course

model_name_list_few = pl.Path(f'results/dynamic/short/{course}/fewshot').glob('*')
model_name_list_few = [i.name.split('.jso')[0] for i in list(model_name_list_few)]

model_name_list_one = pl.Path(f'results/dynamic/short/{course}/oneshot').glob('*')
model_name_list_one = [i.name.split('.jso')[0] for i in list(model_name_list_one)]

model_name_list_zero = pl.Path(f'results/dynamic/short/{course}/zeroshot').glob('*')
model_name_list_zero = [i.name.split('.jso')[0] for i in list(model_name_list_zero)]

model_name_list = list(set(model_name_list_few) | set(model_name_list_one) | set(model_name_list_zero))
model_name_list = sorted(model_name_list)

directory = ["zeroshot", "oneshot", "fewshot"]

eval_results = []
mismatched_eval_results = []
for model_name in model_name_list:
    row = [model_name]
    mismatched_row = [model_name]
    for d in directory:
        print(f"Processing {d} for {model_name}")
        f1, precision, recall, mismatch_percentage = extract_dynamic_info_from_json(f'results/dynamic/short/{course}/{d}/{model_name}.json')

        if f1 is None:
            cell = f"F1 score:                None\nPrecision score: None\nRecall score:        None\nMismatch percentage: None"
            row.append("None")
            mismatched_row.append("None")
        elif mismatch_percentage > 0:
            cell = f"F1 score:                {f1:.4f}\nPrecision score: {precision:.4f}\nRecall score:        {recall:.4f}\nMismatch percentage: {mismatch_percentage:.2f}%"
            row.append("Mismatched")
            mismatched_row.append(cell)
        else:
            cell = f"F1 score:                {f1:.4f}\nPrecision score: {precision:.4f}\nRecall score:        {recall:.4f}"
            row.append(cell)
            mismatched_row.append("Matched")

    for cell in row[1:]:
        if cell != "Mismatched" and cell != "None":
            eval_results.append(row)
            break
    for cell in mismatched_row[1:]:
        if cell != "Matched":
            mismatched_eval_results.append(mismatched_row)
            break

    with open(f'results/dynamic/short/{course}/{course}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Model Name", "Zero-shot", "One-shot", "Few-shot"])
        writer.writerows(eval_results)
    with open(f'results/dynamic/short/{course}/{course}_mismatched.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Model Name", "Zero-shot", "One-shot", "Few-shot"])
        writer.writerows(mismatched_eval_results)