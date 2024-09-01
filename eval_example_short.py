from prompt.prompt_template import prompt_list_v1, prompt_list_v2
import requests
import json


def clear_lines():
    print("\033[2J")


directory = ["zeroshot", "oneshot", "fewshot"]

with open("data/example.json", "r") as file:
    data = json.load(file)

example_list = data["examples"]
prompt_v_list = [prompt_list_v1, prompt_list_v2]


def get_response(i, j, stream=False):
    global prompt
    index = 0
    results = {}
    while index < len(example_list):
        question = example_list[index]["question"]
        full_mark = example_list[index]["fullMark"]
        ref_answer = example_list[index]["referenceAnswer"]
        stu_answer = example_list[index]["studentAnswer"]
        query = prompt.format(
            question=question,
            ref_answer=ref_answer,
            stu_answer=stu_answer,
            full_mark=full_mark,
        )

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
                    print("Question:", question, "\n")
                    print("Reference Answer:", ref_answer, "\n")
                    print("Student Answer:", stu_answer, "\n")
                    print("Feedback:", text, "\n\n")
            example_list[index]["feedback"] = text
            results[index] = example_list[index]
        else:
            text = json.loads(response.text)["text"]
            print("Question:", question, "\n")
            print("Reference Answer:", ref_answer, "\n")
            print("Student Answer:", stu_answer, "\n")
            print("Feedback:", text, "\n\n")
            example_list[index]["feedback"] = text
            results[index] = example_list[index]
            model_name = json.loads(response.text)["model"]
        index += 1

    if stream:
        with open("results/results.json", "w") as file:
            json.dump(results, file, indent=4)
    else:
        with open(
            f"results/short/example/v{j+1}/{directory[i]}/{model_name}.json", "w"
        ) as file:
            json.dump(results, file, indent=4)


for i in range(len(directory)):
    for j in range(2):
        prompt = prompt_v_list[j][i]
        get_response(i, j, False)
