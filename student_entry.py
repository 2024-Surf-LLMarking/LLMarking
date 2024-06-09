import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stream", action="store_true", help="Whether or not to print the response in a streaming way.")

args = parser.parse_args()

def clear_lines():
    print("\033[2J")

prompt_template = """
**Instructions: Grade the student's response based on the given question and reference answer on a scale of 0 to 100. Then identify and list each specific point in the student's answer that leads to point deductions, noting any discrepancies, accuracies, or areas for improvement compared to the reference answer. Use the following format for the interaction:**

- **Question:** The question given to the student, which they need to answer succinctly.
- **Reference Answer:** A reference answer for comparison.
- **Student Answer:** The actual answer provided by the student.

**Please provide the feedback (each deduction point) as follows:**
1. **Final Score of the Student's Answer:** [0 to 100]
2. **Deduction Reason:** [Briefly describe the reason for the deduction, including the number of deduction points.]
3. **Deduction Reason:** [Continue listing each reason and the number of deduction points, ensuring clarity and specificity in each entry.]

**Now, let's begin:**

- **Question:** {question}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

with open('example.json', 'r') as file:
    data = json.load(file)

example_list = data["examples"]

index = 0
results = {}

def get_response(stream = False):
    while index < len(example_list):
        question = example_list[index]["question"]
        ref_answer = example_list[index]["referenceAnswer"]
        stu_answer = example_list[index]["studentAnswer"]
        query = prompt_template.format(question=question, ref_answer=ref_answer, stu_answer=stu_answer)

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
                    print("Question:", question)
                    print("Reference Answer:", ref_answer)
                    print("Student Answer:", stu_answer)
                    print("Feedback:", text)
            example_list[index]["feedback"] = text
            results[index] = example_list[index]
        else:
            text = json.loads(response.text)["text"]
            print("Question:", question)
            print("Reference Answer:", ref_answer)
            print("Student Answer:", stu_answer)
            print("Feedback:", text)
            example_list[index]["feedback"] = text
            results[index] = example_list[index]
            model_name = json.loads(response.text)["model_name"]
        index += 1

    if stream:
        with open('example/results.json', 'w') as file:
            json.dump(results, file, indent=4)
    else:
        with open(f'example/{model_name}.json', 'w') as file:
            json.dump(results, file, indent=4)
    
get_response(args.stream)
