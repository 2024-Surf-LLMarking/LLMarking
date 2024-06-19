from db_utils import create_table, insert_data, select_data, list_to_string
from prompt_template import one_prompt as prompt
import gradio as gr
import json
import csv
import pathlib as pl
import requests

def upload_file(db):
    if db is None:
        gr.Warning("Please also select a database!")
        return gr.Button('Submit', interactive=False)
    return gr.Button('Submit', interactive=True)

def upload_db():
    return gr.Button('Submit', interactive=True)

def select_db(file_output):
    if file_output is None:
        return gr.Button('Submit', interactive=False)
    return gr.Button('Submit', interactive=True)

def disable_submit():
    return gr.Button('Submit', interactive=False)

def disable_upload():
    return gr.Button('Upload', interactive=False)

def dis_enable_upload_to_db_field(enable):
    if enable:
        return (
            gr.Markdown('#### Upload your csv file that contains your course-question codes, corresponding questions, full mark and scoring details:', visible=True),
            gr.File(file_count='multiple', file_types=['.csv'], label='CSV files that contain database data', visible=True),
            gr.ClearButton([db_data], value='Clear', visible=True),
            gr.Button("Upload", interactive=False, visible=True)
        )
    else:
        return (
            gr.Markdown(visible=False),
            gr.File(visible=False),
            gr.ClearButton(visible=False),
            gr.Button(visible=False)
        )

css = """footer {visibility: hidden}
.logo img {height:100px; width:auto; margin:0 auto;}
"""
columns = "question_code TEXT, question TEXT, full_mark REAL, scoring TEXT"
p = pl.Path('data')
if not p.exists():
    p.mkdir()
r = pl.Path('results')
if not r.exists():
    r.mkdir()

with gr.Blocks(css=css, title='LLMarking') as app:
    db_files = list(p.glob('*.db'))
    db_files = [file.name.split('.')[-2] for file in db_files]
    with gr.Row():
        logo_img=gr.Image('https://s2.loli.net/2024/06/18/kbRqVAKdnFEhLj8.png',elem_classes='logo', show_download_button=False, show_label=False, container=False)
    with gr.Row():
        gr.Markdown('# LLMarking')
    with gr.Row():
        db = gr.Dropdown(
            db_files, label="Question Database", info="Select the question database that you would like the automatically grade upon."
        )
    with gr.Row():
        gr.Markdown('#### Upload your csv file that needs to be marked:')
    with gr.Row():
        file_output = gr.File(file_count='multiple', file_types=['.csv'], label='CSV files that needs to be graded')
    with gr.Row():
        clear_btn=gr.ClearButton([db, file_output],value='Clear')
        submit_btn=gr.Button("Submit", interactive=False)
    with gr.Row():
        file_download = gr.File(label="Download Grading Results", visible=False)
    with gr.Row():
        upload_to_db_ck_box = gr.Checkbox(label="Upload to database", info="Do you want to upload your data to database?")
    with gr.Row():
        upload_to_db_title = gr.Markdown(
            '#### Upload your csv file that contains your course-question codes, corresponding questions, full mark and scoring details:', 
            visible=False
            )
    with gr.Row():
        db_data = gr.File(
            file_count='multiple', 
            file_types=['.csv'], 
            label='CSV files that contain database data', 
            visible=False
            )
    with gr.Row():
        upload_to_db_clear_btn = gr.ClearButton(
            [db_data],value='Clear', 
            visible=False
            )
        upload_to_db_submit_btn = gr.Button("Upload", 
                                            interactive=False, 
                                            visible=False
                                            )
        
    def submit_for_grading(db, file_output):
        file_name_list = [file.split('/')[-1] for file in file_output]
        file_name = ', '.join(file_name_list)
        gr.Info(f"Sending file: {file_name} to server and grade answers according to {db} database...")
        db_rows = select_data(f"data/{db}.db", db)
        question_answer_mapping = {row[0]: (row[1], row[3]) for row in db_rows}
        responses = []
        gr.Info(f"Grading answers...")
        for idx, file in enumerate(file_output):
            with open(file, 'r') as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader)
                for row in csv_reader:
                    question_code, stu_answer, manual_score = row
                    question = question_answer_mapping[question_code][0]
                    ref_answer = question_answer_mapping[question_code][1]
                    query = prompt.format(question=question, ref_answer=ref_answer, stu_answer=stu_answer)
                    response = requests.post(
                        "http://100.65.8.31:8000/chat",
                        json={
                            "query": query,
                            "stream": False,
                            "history": None,
                        },
                        stream=False,
                    )
                    text = json.loads(response.text)["text"]
                    responses.append({
                        "question_code": question_code,
                        "question": question,
                        "student_answer": stu_answer,
                        "reference_answer": ref_answer,
                        "feedback": text
                    })
        results_path = r / 'results.json'
        with results_path.open('w') as file:
            json.dump(responses, file, indent=4)
        gr.Info(f"Data uploaded to server and graded successfully! You can download the results below by clicking the button.")
        gr.Info(f"Results are saved in {results_path.name}!")
        download_path = r.name + '/' + results_path.name
        return gr.Button('Submit', interactive=True), gr.File(download_path, label="Download Grading Results", visible=True)
    
    def submit_to_db(db_data):
        file_name_list = [file.split('/')[-1].split('.')[-2] for file in db_data]
        file_name = ', '.join(file_name_list)
        gr.Info(f"Sending file: {file_name} to database...")
        for idx, name in enumerate(file_name_list):
            create_table(f"data/{name}.db", name, columns)
            with open(db_data[idx], 'r') as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader)
                for row in csv_reader:
                    row_str = list_to_string(row)
                    print(row_str)
                    insert_data(f"data/{name}.db", name, row_str)
        db_files = list(p.glob('*.db'))
        db_files = [file.name.split('.')[-2] for file in db_files]
        gr.Info(f"Data uploaded to database successfully!")
        return gr.Button('Upload', interactive=True), gr.Dropdown(db_files, label="Question Database", info="Select the question database that you would like the automatically grade upon.")
    
    db.change(select_db, file_output, submit_btn)
    upload_to_db_ck_box.change(dis_enable_upload_to_db_field, upload_to_db_ck_box, [upload_to_db_title, db_data, upload_to_db_clear_btn, upload_to_db_submit_btn])
    file_output.upload(upload_file, db, submit_btn)
    db_data.upload(upload_db, None, upload_to_db_submit_btn)
    clear_btn.click(disable_submit, None, submit_btn)
    upload_to_db_clear_btn.click(disable_upload, None, upload_to_db_submit_btn)
    submit_btn.click(submit_for_grading, [db, file_output], [submit_btn, file_download])
    upload_to_db_submit_btn.click(submit_to_db, db_data, [upload_to_db_submit_btn, db])

if __name__ == "__main__":
    app.queue(200)  # 请求队列
    app.launch(
        server_name='0.0.0.0',
        max_threads=500, # 线程池
        favicon_path='./favicon.png',
        server_port=80
        )