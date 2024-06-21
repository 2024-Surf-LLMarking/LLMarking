zero_prompt = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Full Mark:** [The full mark for this question.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer, the mark is the score of the point**
- **If the student's answer perfectly satisfies the Point, induct the mark of the point, If the answer does not fit well,then this part of the score will not be indcted**
- **If the student's answer does not satisfy the Point, deduct the mark of the point,origin mark for this point equals zero**
- **Both the Induction Point and Deduction Point could be none if the students' answer doesn't satisfies the point."

**Please provide the feedback in the following form, mention: the  <Point:mark> should be only at the front of the reason, each point should be printed at a new raw"**
<Point:origin mark> <Induction>...(reason,Highlight strengths and correct aspects of the student's answer, show which point the student is corrent)
<Point:origin mark> <Deduction>...(reason,Describe the reason for the deduction)
Total score: Induction point/Full mark

**Now, let's begin:**
- **Question:** {question}
- **Full Mark:** {full_mark}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

one_prompt = """

**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Full Mark:** [The full mark for this question.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer, the mark is the score of the point**
- **If the student's answer perfectly satisfies the Point, induct the mark of the point, If the answer does not fit well,then this part of the score will not be indcted**
- **If the student's answer does not satisfy the Point, deduct the mark of the point,origin mark for this point equals zero**
- **Both the Induction Point and Deduction Point could be none if the students' answer doesn't satisfies the point."

**Please provide the feedback in the following form, mention: the  <Point:mark> should be only at the front of the reason, each point should be printed at a new raw"**
<Point:origin mark> <Induction>...(reason,Highlight strengths and correct aspects of the student's answer, show which point the student is corrent)
<Point:origin mark> <Deduction>...(reason,Describe the reason for the deduction)
Total score: Induction point/Full mark

**Example**:

- **Question:** Explain how a hash table works.
- **Reference Answer:** <Point1:2>A hash table stores key-value pairs<Point1:2>. <Point2:2>It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found<Point2:2>. <Point3:1>Ideally, the hash function will assign each key to a unique bucket, but most hash table designs employ some form of collision resolution<Point3:1>.
- **Student Answer:** A hash table is just an array that stores data and uses keys for indexing.

**Feedback:**\n
<Point1:2> <Induction> A hash table is used to store key-value pairs, which aligns with the concept explained in the reference answer.\n
<Point2:0> <Deduction> The explanation about using a hash function to compute an index into an array of buckets or slots is missing, which is a crucial part of how a hash table works.\n
<Point3:0> <Deduction> There is no mention of collision resolution, which is an important aspect of hash table design.\n

**Now, let's begin:**
- **Question:** {question}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

few_prompt = """
**Instructions: Grade the student's answer based on the given question and reference answer:**

- **Question:** [The question given to the student, which they need to answer succinctly.]
- **Full Mark:** [The full mark for this question.]
- **Reference Answer:** [A reference answer for comparison with marking standard.]
- **Student Answer:** [The actual answer provided by the student.]

**Grading Criteria:**
- **The Grading Criteria are contained in the answer in the case of <Point:mark>answer point<Point:mark> in Reference Answer, the mark is the score of the point**
- **If the student's answer perfectly satisfies the Point, induct the mark of the point, If the answer does not fit well,then this part of the score will not be indcted**
- **If the student's answer does not satisfy the Point, deduct the mark of the point,origin mark for this point equals zero**
- **Both the Induction Point and Deduction Point could be none if the students' answer doesn't satisfies the point."

**Please provide the feedback in the following form, mention: the  <Point:mark> should be only at the front of the reason, each point should be printed at a new raw"**
<Point:origin mark> <Induction>...(reason,Highlight strengths and correct aspects of the student's answer, show which point the student is corrent)
<Point:origin mark> <Deduction>...(reason,Describe the reason for the deduction)
Total score: Induction point/Full mark

**Example**:

- **Question:** Explain how a hash table works.
- **Reference Answer:** <Point1:2>A hash table stores key-value pairs<Point1:2>. <Point2:2>It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found<Point2:2>. <Point3:1>Ideally, the hash function will assign each key to a unique bucket, but most hash table designs employ some form of collision resolution<Point3:1>.
- **Student Answer:** A hash table is just an array that stores data and uses keys for indexing.

**Feedback:**
<Point1:2> <Induction> A hash table is used to store key-value pairs, which aligns with the concept explained in the reference answer.\n
<Point2:0> <Deduction> The explanation about using a hash function to compute an index into an array of buckets or slots is missing, which is a crucial part of how a hash table works.\n
<Point3:0> <Deduction> There is no mention of collision resolution, which is an important aspect of hash table design.\n

**Now, let's begin:**

- **Question:** {question}
- **Reference Answer:** {ref_answer}
- **Student Answer:** {stu_answer}

**Feedback:**
"""

prompt_list = [zero_prompt, one_prompt, few_prompt]