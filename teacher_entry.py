from db_utils import create_table, insert_data, select_data, list_to_string
import gradio as gr
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

with gr.Blocks(css=css) as app:
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
        # file_output: List
        # for file in file_output:
        #     csv = pd.read_csv(file)
        #     for row in csv:
        #         question = row['Question']
        #         stu_answer = row['stuAnswer']
        #         ref_answer = row['refAnswer']
        file_name_list = [file.split('/')[-1] for file in file_output]
        file_name = ', '.join(file_name_list)
        gr.Info(f"Sending file: {file_name} to server and grade answers according to {db} database...")
        return gr.Button('Submit', interactive=False)
    
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
    submit_btn.click(submit_for_grading, [db, file_output], submit_btn)
    upload_to_db_submit_btn.click(submit_to_db, db_data, [upload_to_db_submit_btn, db])

if __name__ == "__main__":
    app.queue(200)  # 请求队列
    app.launch(server_name='0.0.0.0',max_threads=500) # 线程池