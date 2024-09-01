import sqlite3 as sql


def create_connection(db_file):
    conn = None
    try:
        conn = sql.connect(db_file)
        print(sql.version)
    except sql.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(db_file, table_name, columns):
    conn = sql.connect(db_file)
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    conn.commit()
    conn.close()


def insert_data(db_file, table_name, data):
    conn = sql.connect(db_file)
    c = conn.cursor()
    c.execute(f"INSERT INTO {table_name} VALUES ({data})")
    conn.commit()
    conn.close()


def select_data(db_file, table_name):
    conn = sql.connect(db_file)
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    conn.close()
    return rows


def select_question(db_file, table_name, question_code):
    conn = sql.connect(db_file)
    c = conn.cursor()
    c.execute(
        f"SELECT question FROM {table_name} WHERE question_code = '{question_code}'"
    )
    rows = c.fetchall()
    conn.close()
    return rows


def update_data(db_file, table_name, data):
    conn = sql.connect(db_file)
    c = conn.cursor()
    c.execute(f"UPDATE {table_name} SET {data}")
    conn.commit()
    conn.close()


def delete_data(db_file, table_name, data):
    conn = sql.connect(db_file)
    c = conn.cursor()
    c.execute(f"DELETE FROM {table_name} WHERE {data}")
    conn.commit()
    conn.close()


def drop_table(db_file, table_name):
    conn = sql.connect(db_file)
    c = conn.cursor()
    c.execute(f"DROP TABLE {table_name}")
    conn.commit()
    conn.close()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def list_to_string(data_list):
    result = []
    for item in data_list:
        if is_number(item):
            result.append(item)
        else:
            result.append(f"'{item}'")
    return ", ".join(result)


def main():
    db_file = "data/INT204.db"
    table_name = "INT204"
    columns = "question_code TEXT, question TEXT, full_mark REAL, scoring TEXT"
    data = "'INT001', 'Explain the primary differences between machine learning and traditional programming.', 5.0, 'In traditional programming, programmers explicitly code the behavior based on logic and data inputs, which the program then executes to produce outputs. Conversely, machine learning involves training a model on a dataset, allowing it to learn the patterns and behaviors from the data, which it then applies to make predictions or decisions, rather than following explicitly programmed instructions.'"
    create_connection(db_file)
    create_table(db_file, table_name, columns)
    insert_data(db_file, table_name, data)
    select_data(db_file, table_name)
    data = "question_code = 'INT002'"
    update_data(db_file, table_name, data)
    select_data(db_file, table_name)
    delete_data(db_file, table_name, data)
    select_data(db_file, table_name)
    drop_table(db_file, table_name)
    # db_file = "data/CCT.db"
    # table_name = "CCT"
    # select_data(db_file, table_name)


if __name__ == "__main__":
    main()
