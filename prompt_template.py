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