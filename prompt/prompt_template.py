zero_prompt_v1 = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer.**
- **If the student's answer satisfies the Point, the Point is judged as 'True'. The student's answer doesn't need to be perfectly the same as the reference answer.**
- **If the student's answer does not satisfy the Point, the Point is judged as 'False'.**
- **The judgement should only be 'True' or 'False', other formats are all invalid.**

**Please provide the feedback in the following form, mention: the <Point:mark> should be only at the front of the reason, each point should be given at a new row; every point that exists in reference answer should have a feedback; don't give feedback on extra points, the number of points in the following should be the same as the number of points inside Reference Answer:"**
<Point1:mark> *True* (reason, Highlight strengths and correct aspects of the student's answer, show which point the student is correct about)\n
<Point2:mark> *False* (reason, Describe why this point is false)\n
...

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

one_prompt_v1 = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer.**
- **If the student's answer satisfies the Point, the Point is judged as 'True'. The student's answer doesn't need to be perfectly the same as the reference answer.**
- **If the student's answer does not satisfy the Point, the Point is judged as 'False'.**
- **The judgement should only be 'True' or 'False', other formats are all invalid.**

**Please provide the feedback in the following form, mention: the <Point:mark> should be only at the front of the reason, each point should be given at a new row; every point that exists in reference answer should have a feedback; don't feedback on extra points:"**
<Point1:mark> *True* (reason, Highlight strengths and correct aspects of the student's answer, show which point the student is correct about)\n
<Point2:mark> *False* (reason, Describe why this point is false)\n
...

**Example:**
- **Question:** Describe the basic components of a distributed system.
- **Full Mark:** 5
- **Reference Answer:** A distributed system consists of multiple software components located on different networked computers, <Point1:2>which communicate and coordinate their actions by passing messages<Point1:2>. <Point2:2>The components interact with each other in order to achieve a common goal<Point2:2>. <Point3:1>Key components include servers, clients, and the communication infrastructure<Point3:1>.
- **Student Answer:** Distributed systems are multiple computers connected to a server that manages them. Within the system, the computers communicate with each other to achieve a common goal.

**Feedback:**
<Point1:2> *True* (The student's answer correctly mentions the communication between components.)\n
<Point2:2> *True* (The student's answer correctly mentions the common goal shared among the components.)\n
<Point3:1> *False* (The student's answer does not mention the key components of a distributed system.)\n

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

few_prompt_v1 = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer.**
- **If the student's answer satisfies the Point, the Point is judged as 'True'. The student's answer doesn't need to be perfectly the same as the reference answer.**
- **If the student's answer does not satisfy the Point, the Point is judged as 'False'.**
- **The judgement should only be 'True' or 'False', other formats are all invalid.**

**Please provide the feedback in the following form, mention: the <Point:mark> should be only at the front of the reason, each point should be given at a new row; every point that exists in reference answer should have a feedback; don't feedback on extra points:"**
<Point1:mark> *True* (reason, Highlight strengths and correct aspects of the student's answer, show which point the student is correct about)\n
<Point2:mark> *False* (reason, Describe why this point is false)\n
...

**Example 1:**
- **Question:** Describe the basic components of a distributed system.
- **Full Mark:** 5
- **Reference Answer:** A distributed system consists of multiple software components located on different networked computers, <Point1:2>which communicate and coordinate their actions by passing messages<Point1:2>. <Point2:2>The components interact with each other in order to achieve a common goal<Point2:2>. <Point3:1>Key components include servers, clients, and the communication infrastructure<Point3:1>.
- **Student Answer:** Distributed systems are multiple computers connected to a server that manages them. Within the system, the computers communicate with each other to achieve a common goal.

**Feedback:**
<Point1:2> *True* (The student's answer correctly mentions the communication between components.)\n
<Point2:2> *True* (The student's answer correctly mentions the common goal shared among the components.)\n
<Point3:1> *False* (The student's answer does not mention the key components of a distributed system.)\n

**Example 2:**
- **Question:** What is refactoring in software development?
- **Full Mark:** 5
- **Reference Answer:** <Point1:3>Refactoring is the process of restructuring existing computer code—changing the factoring—without changing its external behavior<Point1:3>. <Point2:2>It is done to improve nonfunctional attributes of the software, such as readability, reduced complexity, or improving maintainability and scalability<Point2:2>.
- **Student Answer:** Refactoring is when you try to improve the code quality of a software system without changing the way that people use it.

**Feedback:**
<Point1:3> *True* (The student's answer correctly mentions the restructuring of existing code without changing its behavior.)\n
<Point2:2> *False* (The student's answer does not mention the improvement of nonfunctional attributes of the software.)\n

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

prompt_list_v1 = [zero_prompt_v1, one_prompt_v1, few_prompt_v1]

zero_prompt_v2 = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer.**
- **If the student's answer satisfies the Point, the Point is judged as 'True'. The student's answer doesn't need to be perfectly the same as the reference answer.**
- **If the student's answer does not satisfy the Point, the Point is judged as 'False'.**
- **The judgement should only be 'True' or 'False', other formats are all invalid.**

**Please provide the feedback in the following form, mention: the <Point:mark> should be only at the front of the reason, each point should be given at a new row; every point that exists in reference answer should have a feedback; don't feedback on extra points:"**
<Point1:mark> *True* (reason, Highlight strengths and correct aspects of the student's answer, show which point the student is correct about)\n
<Point2:mark> *False* (reason, Describe why this point is false)\n
...
Total score: [Sum of all the points marked as 'True'] / [Full mark]

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

one_prompt_v2 = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer.**
- **If the student's answer satisfies the Point, the Point is judged as 'True'. The student's answer doesn't need to be perfectly the same as the reference answer.**
- **If the student's answer does not satisfy the Point, the Point is judged as 'False'.**
- **The judgement should only be 'True' or 'False', other formats are all invalid.**

**Please provide the feedback in the following form, mention: the <Point:mark> should be only at the front of the reason, each point should be given at a new row; every point that exists in reference answer should have a feedback; don't feedback on extra points:"**
<Point1:mark> *True* (reason, Highlight strengths and correct aspects of the student's answer, show which point the student is correct about)\n
<Point2:mark> *False* (reason, Describe why this point is false)\n
...
Total score: [Sum of all the points marked as 'True'] / [Full mark]

**Example:**
- **Question:** Describe the basic components of a distributed system.
- **Full Mark:** 5
- **Reference Answer:** A distributed system consists of multiple software components located on different networked computers, <Point1:2>which communicate and coordinate their actions by passing messages<Point1:2>. <Point2:2>The components interact with each other in order to achieve a common goal<Point2:2>. <Point3:1>Key components include servers, clients, and the communication infrastructure<Point3:1>.
- **Student Answer:** Distributed systems are multiple computers connected to a server that manages them. Within the system, the computers communicate with each other to achieve a common goal.

**Feedback:**
<Point1:2> *True* (The student's answer correctly mentions the communication between components.)\n
<Point2:2> *True* (The student's answer correctly mentions the common goal shared among the components.)\n
<Point3:1> *False* (The student's answer does not mention the key components of a distributed system.)\n
Total score: 4 / 5

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

few_prompt_v2 = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer.**
- **If the student's answer satisfies the Point, the Point is judged as 'True'. The student's answer doesn't need to be perfectly the same as the reference answer.**
- **If the student's answer does not satisfy the Point, the Point is judged as 'False'.**
- **The judgement should only be 'True' or 'False', other formats are all invalid.**

**Please provide the feedback in the following form, mention: the <Point:mark> should be only at the front of the reason, each point should be given at a new row; every point that exists in reference answer should have a feedback; don't feedback on extra points:"**
<Point1:mark> *True* (reason, Highlight strengths and correct aspects of the student's answer, show which point the student is correct about)\n
<Point2:mark> *False* (reason, Describe why this point is false)\n
...

**Example 1:**
- **Question:** Describe the basic components of a distributed system.
- **Full Mark:** 5
- **Reference Answer:** A distributed system consists of multiple software components located on different networked computers, <Point1:2>which communicate and coordinate their actions by passing messages<Point1:2>. <Point2:2>The components interact with each other in order to achieve a common goal<Point2:2>. <Point3:1>Key components include servers, clients, and the communication infrastructure<Point3:1>.
- **Student Answer:** Distributed systems are multiple computers connected to a server that manages them. Within the system, the computers communicate with each other to achieve a common goal.

**Feedback:**
<Point1:2> *True* (The student's answer correctly mentions the communication between components.)\n
<Point2:2> *True* (The student's answer correctly mentions the common goal shared among the components.)\n
<Point3:1> *False* (The student's answer does not mention the key components of a distributed system.)\n
Total score: 4 / 5

**Example 2:**
- **Question:** What is refactoring in software development?
- **Full Mark:** 5
- **Reference Answer:** <Point1:3>Refactoring is the process of restructuring existing computer code—changing the factoring—without changing its external behavior<Point1:3>. <Point2:2>It is done to improve nonfunctional attributes of the software, such as readability, reduced complexity, or improving maintainability and scalability<Point2:2>.
- **Student Answer:** Refactoring is when you try to improve the code quality of a software system without changing the way that people use it.

**Feedback:**
<Point1:3> *True* (The student's answer correctly mentions the restructuring of existing code without changing its behavior.)\n
<Point2:2> *False* (The student's answer does not mention the improvement of nonfunctional attributes of the software.)\n
Total score: 3 / 5

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

prompt_list_v2 = [zero_prompt_v2, one_prompt_v2, few_prompt_v2]