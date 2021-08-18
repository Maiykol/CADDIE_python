import pandas as pd
from caddiepy import settings


def load_csv(file):
    return pd.read_csv(f'{settings.PATH_SOTRAGE}/{file}')

def load_xlsx(file, sheet=0):
    return pd.read_excel(f'{settings.PATH_SOTRAGE}/{file}', sheet_name=sheet)