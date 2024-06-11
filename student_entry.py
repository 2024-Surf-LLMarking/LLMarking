from prompt_template import prompt_list
import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stream", action="store_true", help="Whether or not to print the response in a streaming way.")
parser.add_argument("-n", "--shots", type=int, default=0, help="Number of shots to run.", required=True, choices=[0, 1, 2])

args = parser.parse_args()

def clear_lines():
    print("\033[2J")

directory = ["zeroshot", "oneshot", "fewshot"]

with open('data/example.json', 'r') as file:
    data = json.load(file)

example_list = data["examples"]

index = 0
results = {}
prompt = prompt_list[args.shots]

def get_response(stream = False):
    global index, results, prompt
    while index < len(example_list):
        question = example_list[index]["question"]
        ref_answer = example_list[index]["referenceAnswer"]
        stu_answer = example_list[index]["studentAnswer"]
        query = prompt.format(question=question, ref_answer=ref_answer, stu_answer=stu_answer)

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
            example_list[index]["feedback"] = text
            results[index] = example_list[index]
        else:
            text = json.loads(response.text)["text"]
            print("Question:", question, '\n')
            print("Reference Answer:", ref_answer, '\n')
            print("Student Answer:", stu_answer, '\n')
            print("Feedback:", text, '\n\n')
            example_list[index]["feedback"] = text
            results[index] = example_list[index]
            model_name = json.loads(response.text)["model"]
        index += 1

    if stream:
        with open('results/results.json', 'w') as file:
            json.dump(results, file, indent=4)
    else:
        with open(f'results/{directory[args.shots]}/{model_name}.json', 'w') as file:
            json.dump(results, file, indent=4)
    
get_response(args.stream)
