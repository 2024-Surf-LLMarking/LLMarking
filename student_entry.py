import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stream", action="store_true", help="Whether or not to print the response in a streaming way.")
parser.add_argument("-n", "--shots", type=int, default=0, help="Number of shots to run.", required=True, choices=[0, 1, 2])

args = parser.parse_args()

def clear_lines():
    print("\033[2J")

zero_prompt = """
**Instructions: Grade the student's answer based on the given question and reference answer on a scale of 0 to 100. Then identify and list each specific point in the student's answer that leads to point deductions, noting any relevances, accuracies, completenesses, clarities, or areas for improvement compared to the reference answer. Use the following format for the interaction:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**

- **Relevance (0-25 points)**: The answer must directly address all parts of the question.
- **Accuracy (0-25 points)**: The answer must be factually correct.
- **Completeness (0-25 points)**: The answer must cover all necessary aspects of the question without omitting crucial details.
- **Clarity (0-25 points)**: The answer must be clearly and logically presented.

**Please provide the feedback as follows:**

1. **Final Score of the Student's Answer:** [0 to 100]
2. **Positive Feedback:** [Highlight strengths and correct aspects of the student's answer.]
3. **Deduction Reason:** [Describe the reason for the deduction, including the number of deduction points. Repeat for each issue identified.]

**Now, let's begin:**

- **Question:** {question}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

one_prompt = """
**Instructions: Grade the student's response based on the given question and reference answer on a scale of 0 to 100. Then identify and list each specific point in the student's answer that leads to point deductions, noting any relevances, accuracies, completenesses, clarities, or areas for improvement compared to the reference answer. Use the following format for the interaction:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**

- **Relevance (0-25 points)**: The answer must directly address all parts of the question.
- **Accuracy (0-25 points)**: The answer must be factually correct.
- **Completeness (0-25 points)**: The answer must cover all necessary aspects of the question without omitting crucial details.
- **Clarity (0-25 points)**: The answer must be clearly and logically presented.

**Please provide the feedback as follows:**

1. **Final Score of the Student's Answer:** [0 to 100]
2. **Positive Feedback:** [Highlight strengths and correct aspects of the student's answer.]
3. **Deduction Reason:** [Describe the reason for the deduction, including the number of deduction points. Repeat for each issue identified.]

**Now, let's begin:**

- **Question:** {question}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

few_prompt = """
**Instructions: Grade the student's response based on the given question and reference answer on a scale of 0 to 100. Then identify and list each specific point in the student's answer that leads to point deductions, noting any relevances, accuracies, completenesses, clarities, or areas for improvement compared to the reference answer. Use the following format for the interaction:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**

- **Relevance (0-25 points)**: The answer must directly address all parts of the question.
- **Accuracy (0-25 points)**: The answer must be factually correct.
- **Completeness (0-25 points)**: The answer must cover all necessary aspects of the question without omitting crucial details.
- **Clarity (0-25 points)**: The answer must be clearly and logically presented.

**Please provide the feedback as follows:**

1. **Final Score of the Student's Answer:** [0 to 100]
2. **Positive Feedback:** [Highlight strengths and correct aspects of the student's answer.]
3. **Deduction Reason:** [Describe the reason for the deduction, including the number of deduction points. Repeat for each issue identified.]

**Now, let's begin:**

- **Question:** {question}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

prompt_list = [zero_prompt, one_prompt, few_prompt]
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
            model_name = json.loads(response.text)["model"]
        index += 1

    if stream:
        with open('results/results.json', 'w') as file:
            json.dump(results, file, indent=4)
    else:
        with open(f'results/{directory[args.shots]}/{model_name}.json', 'w') as file:
            json.dump(results, file, indent=4)
    
get_response(args.stream)
