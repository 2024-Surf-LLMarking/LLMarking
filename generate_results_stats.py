from utils.compute_mark import extract_info_from_json
import pathlib as pl
import csv

model_name_list = pl.Path('results/short/fewshot').rglob('*.json')
model_name_list = [i.name.split('.jso')[0] for i in list(model_name_list)]

directory = ["zeroshot", "oneshot", "fewshot"]
course = "INT"

eval_results = []
for model_name in model_name_list:
    row = [model_name]
    for d in directory:
        print(f"Processing {d} for {model_name}")
        f1, precision, recall = extract_info_from_json(f'results/short/{d}/{model_name}.json')
        cell = f"""F1 score:\t{f1}\nPrecision score: {precision}\nRecall score:\t{recall}"""
        row.append(cell)
    eval_results.append(row)
    with open(f'results/short/{course}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Model Name", "Zero-shot", "One-shot", "Few-shot"])
        writer.writerows(eval_results)