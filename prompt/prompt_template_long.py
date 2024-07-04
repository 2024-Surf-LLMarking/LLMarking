zero_prompt_v1 = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **Relevance (0-25 points)**: The answer must directly address all parts of the question.
  - 21-25 points (Highly Relevant): The answer directly addresses every part of the question with well-integrated examples or evidence. There is a strong alignment with the question throughout.
  - 11-20 points (Moderately Relevant): The answer addresses most parts of the question, but may miss some elements or the alignment may not be consistently clear.
  - 0-10 points (Low Relevance): The answer addresses the question partially, with significant elements either misinterpreted or not covered.
- **Accuracy (0-25 points)**: The answer must be factually correct.
  - 21-25 points (Highly Relevant): The answer directly addresses every part of the question with well-integrated examples or evidence. There is a strong alignment with the question throughout.
  - 11-20 points (Moderately Relevant): The answer addresses most parts of the question, but may miss some elements or the alignment may not be consistently clear.
  - 0-10 points (Low Relevance): The answer addresses the question partially, with significant elements either misinterpreted or not covered.
- **Completeness (0-25 points)**: The answer must cover all necessary aspects of the question without omitting crucial details.
  - 21-25 points (Highly Complete): The answer provides a comprehensive discussion of the topic, covering all necessary aspects as outlined in the question. It includes detailed explanations and specific examples where appropriate.
  - 11-20 points (Moderately Complete): The answer covers many of the necessary aspects but lacks depth in one or two. Some parts of the response may be too general or incomplete.
  - 0-10 points (Lacking Completeness): The answer omits significant aspects of the question, providing a response that feels incomplete or superficial. Key details or examples are missing.
- **Clarity (0-25 points)**: The answer must be clearly and logically presented.
  - 21-25 points (Highly Clear): The answer is presented logically and clearly. Ideas flow naturally from one to another, with effective transitions and phrasing that enhance the reader’s ability to follow the argument or narrative.
  - 11-20 points (Moderately Clear): The answer has some organization and the reader can follow the logic, but there are lapses in clarity due to poor phrasing or loose transitions.
  - 0-10 points (Low Clarity): The answer is difficult to follow due to poor organization, unclear or confusing phrasing, and lacks logical flow. Ideas appear disjointed or are presented in a confusing order.

**Please provide the feedback as follows:**

1. **Positive Feedback:** [Highlight strengths and correct aspects of the student's answer.]
2. **Deduction Reason:** [Describe the reason for the deduction, including the number of deduction points. Repeat for issues identified in each criteria.]
...
**Final Score of the Student's Answer:** [Full Mark - sum of all the deduction points] / [Full Mark]

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

one_prompt_v1 = """"""

few_prompt_v1 = """"""

prompt_list_v1 = [zero_prompt_v1, one_prompt_v1, few_prompt_v1]

zero_prompt_v2 = """"""

one_prompt_v2 = """"""

few_prompt_v2 = """"""

prompt_list_v2 = [zero_prompt_v2, one_prompt_v2, few_prompt_v2]