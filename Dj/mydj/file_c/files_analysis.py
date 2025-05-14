import pandas as pd

def file_read(path):
    path = f"file//"+str(path)
    df = None
    file_ext = path.split('.')[-1]
    if file_ext == 'csv':
        df = pd.read_csv(path)
    elif file_ext == ['xlsx', 'xls']:
        df = pd.read_excel(path)
    return df.head().to_html(col_space=100,justify="left")
