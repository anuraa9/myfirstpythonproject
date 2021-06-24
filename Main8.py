from pathlib import Path
import pandas as pd
from pandas import DataFrame as df
import os


# xl = pd.ExcelFile(xl_path)
# df = xl.parse("Sheet1")
# df = df.astype({'Unique Id': 'str'}).dtypes


def get_column_values_from_xl(unique_id, po_num):
    xl_path = os.path.join(Path.home(), "Downloads", "back2back_tds.xlsx")
    df = pd.read_excel(xl_path, sheet_name="Sheet1", na_filter=False)
    output_header_list = ['Section Code', 'Tax Category', 'Basic Amt', 'Invoice Amount', 'TDS Amt', 'Category']
    dict_to_return = {}
    rowitem_list = []
    if unique_id and po_num:
        rowitem_list = df.loc[(df['Unique Id'] == unique_id) & (df['PO Num'] == po_num)].values.tolist()
    elif unique_id:
        rowitem_list = df.loc[df['Unique Id'] == unique_id].values.tolist()
    elif po_num:
        rowitem_list = df.loc[df['PO Num'] == po_num].values.tolist()
    else:
        return None

    if len(rowitem_list) > 0:
        rowitem_list = rowitem_list[0]
        column_indexes = [df.columns.get_loc(col) for col in output_header_list]
        for ind in range(len(column_indexes)):
            dict_to_return[output_header_list[ind]] = rowitem_list[column_indexes[ind]]
        return dict_to_return
    else:
        return None


unique_id = 23305431
po_num = 19030174641
column_values_dict = get_column_values_from_xl(unique_id, po_num)
print(column_values_dict)