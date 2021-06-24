from pathlib import Path
import pandas as pd
import os
import json
import re
COLUMN_TO_CHECK = ['basic_amount', 'tax_amount', 'unit_price', 'item_quantity']


def combine_df1_items(df1):
    for i in range(0, len(df1)):
        if df1[i]['item_code'] == '':
            continue
        for j in range(i+1, len(df1)):
            if df1[i]['item_code'] == df1[j]['item_code']:
                df1[i]['item_quantity'] = str(float(df1[i]['item_quantity']) + float(df1[j]['item_quantity']))
                df1[i]['tax_amount'] = str(float(df1[i]['tax_amount']) + float(df1[j]['tax_amount']))
                df1[i]['basic_amount'] = str(float(df1[i]['basic_amount']) + float(df1[j]['basic_amount']))
                df1[j]['item_code'] = ''
    df1_to_return = df1.copy()
    for df_item in df1:
        if df_item['item_code'] == '':
            df1_to_return.remove(df_item)

    return df1_to_return


def get_df2_index_for_df1_item(df1_item, df2):
    print(df1_item['item_description'])
    match_count = 0
    df2_index = -1
    for df2_item in df2:
        if abs(float(df1_item['item_quantity']) - float(df2_item['item_quantity'])) < ((0.5 / 100) * float(df1_item['item_quantity'])):
            match_count += 1
            if match_count > 1:
                df2_index = -1
                break
            else:
                df2_index = df2.index(df2_item)

    if df2_index != -1:
        return df2_index

    match_count = 0

    if df2_index == -1:
        for df2_item in df2:
            if abs(float(df1_item['unit_price']) - float(df2_item['unit_price'])) < 0.5:
                match_count += 1
                if match_count > 1:
                    df2_index = -1
                    break
                else:
                    df2_index = df2.index(df2_item)

    if df2_index != -1:
        return df2_index

    if df2_index == -1:
        item_description_str = re.split(',| ', df1_item['item_description'])
        print(item_description_str)
        match_percent_list = []
        for df2_item in df2:
            match_percent = len([i for i in item_description_str if i in df2_item['item_description']])/len(item_description_str) * 100
            match_percent_list.append(match_percent)
        print(match_percent_list)
        df2_index = match_percent_list.index(max(match_percent_list))
        if max(match_percent_list) > 50:    #and abs(float(po_item['invoiced_quantity']) - float(invoice_dict_list[df2_index]['item_quantity'])) < 0.5
            return df2_index
        else:
            print("No match found for the serial number : {0}".format(df1_item['serial_number']))
            return -1


def change_df1_headers_according_to_df2_headers(df1):
    for df_item in df1:
        df_item['serial_number'] = df_item.pop('po_line_number')
        df_item['unit_of_measurement'] = df_item.pop('uom')
        df_item['item_quantity'] = df_item.pop('invoiced_quantity')
        df_item['basic_amount'] = df_item.pop('line_amount')


def filter_df2_dict(df2):
    df2_to_return = df2.copy()
    keys_to_filter = ['total', 'amount', 'value', 'total amount', 'total value', 'cgst', 'sgst', 'in words']
    for df2_item in df2:
        if any(x in df2_item['item_description'].lower() for x in keys_to_filter):
            df2_to_return.remove(df2_item)
    return df2_to_return


def compare_df1_item_count_with_df2_item_count(df1, df2):
    if len(df2) == len(df1):
        print('Invoice item count matches with PO item count')
    else:
        print('Invoice item count does not matches with PO item count')


def compare_df1_value_with_df2_values(df1_item, df2_item, df1_match_dict_list):
    match_matrix_dict = {}
    if df2_item == {}:
        df1_match_dict_list[df1_item['serial_number']] = {'unit_of_measurement': 'notfound', 'item_quantity': 'notfound', 'unit_price': 'notfound', 'hsn_code': 'notfound', 'tax_amount': 'notfound', 'basic_amount': 'notfound'}
    print(df1_item['unit_of_measurement'])
    print(df2_item['unit_of_measurement'])

    if df1_item['unit_of_measurement'].lower() == df2_item['unit_of_measurement'].lower():
        match_matrix_dict['unit_of_measurement'] = 'correct'
    else:
        match_matrix_dict['unit_of_measurement'] = 'incorrect'

    print(df1_item['item_quantity'])
    print(df2_item['item_quantity'])
    if abs(float(df1_item['item_quantity']) - float(df2_item['item_quantity'])) < ((0.5 / 100) * float(df1_item['item_quantity'])):
        match_matrix_dict['item_quantity'] = 'correct'
    else:
        match_matrix_dict['item_quantity'] = 'incorrect'

    print(df1_item['unit_price'])
    print(df2_item['unit_price'])
    if abs(float(df1_item['unit_price']) - float(df2_item['unit_price'])) < 0.5:
        match_matrix_dict['unit_price'] = 'correct'
    else:
        match_matrix_dict['unit_price'] = 'incorrect'

    print(df1_item['hsn_code'])
    print(df2_item['hsn_code'])
    if abs(float(df1_item['hsn_code']) - float(df2_item['hsn_code'])) < 0.5:
        match_matrix_dict['hsn_code'] = 'correct'
    else:
        match_matrix_dict['hsn_code'] = 'incorrect'

    # print(po_item['gst_rate'])
    # print(invoice_item['sgst_amount'])
    # print(invoice_item['cgst_amount'])
    # print(invoice_item['igst_amount'])
    # pass

    print(df1_item['tax_amount'])
    print(df2_item['tax_amount'])
    if abs(float(df1_item['tax_amount']) - float(df2_item['tax_amount'])) < 0.5:
        match_matrix_dict['tax_amount'] = 'correct'
    else:
        match_matrix_dict['tax_amount'] = 'incorrect'

    print(df1_item['basic_amount'])
    print(df2_item['basic_amount'])
    if abs(float(df1_item['basic_amount']) - float(df2_item['basic_amount'])) < 0.5:
        match_matrix_dict['basic_amount'] = 'correct'
    else:
        match_matrix_dict['basic_amount'] = 'incorrect'

    df1_match_dict_list[df1_item['serial_number']] = match_matrix_dict


def compare_df1_total_with_df2_total(df1, df2):
    df1_item_quantity_total, df1_unit_price_total, df1_tax_amount_total, df1_basic_amount_total = 0, 0, 0, 0
    df2_item_quantity_total, df2_unit_price_total, df2_tax_amount_total, df2_basic_amount_total = 0, 0, 0, 0
    for df1_item in df1:
        df1_item_quantity_total += float(df1_item['item_quantity'])
        df1_unit_price_total += float(df1_item['unit_price'])
        df1_tax_amount_total += float(df1_item['tax_amount'])
        df1_basic_amount_total += float(df1_item['basic_amount'])

    for df2_item in df2:
        df2_item_quantity_total += float(df2_item['item_quantity'])
        df2_unit_price_total += float(df2_item['unit_price'])
        df2_tax_amount_total += float(df2_item['tax_amount'])
        df2_basic_amount_total += float(df2_item['basic_amount'])

    if abs(df1_item_quantity_total - df2_item_quantity_total) < ((0.5/100) * df1_item_quantity_total):
        print('Invoice quantity total matches with PO quantity total')
    else:
        print('Invoice quantity total does not matches with PO quantity total')

    if abs(df1_unit_price_total - df2_unit_price_total) < 0.5:
        print('Invoice Unit price total matches with PO Unit price total')
    else:
        print('Invoice Unit price total does not matches with PO Unit price total')

    if abs(df1_tax_amount_total - df2_tax_amount_total) < 0.5:
        print('Invoice Tax amount total matches with PO Tax amount total')
    else:
        print('Invoice Tax amount total does not matches with PO Tax amount total')

    if abs(df1_basic_amount_total - df2_basic_amount_total) < 0.5:
        print('Invoice Basic amount total matches with PO Basic amount total')
    else:
        print('Invoice Basic amount total does not matches with PO Basic amount total')


def compare_df1_values_with_df2_values(df1, df2):
    df1_match_dict = {}
    for df1_item in df1:
        df2_index = get_df2_index_for_df1_item(df1_item, df2)
        if df2_index != -1:
            compare_df1_value_with_df2_values(df1_item, df2[df2_index], df1_match_dict)
        else:
            print("No invoice item found for the serial number: {0}".format(df1_item['serial_number']))
            compare_df1_value_with_df2_values(df1_item, {}, df1_match_dict)

    accuracy_list = []
    for df1_item in df1:
        if df1_item['serial_number'] in df1_match_dict:
            match_matrix = df1_match_dict[df1_item['serial_number']]
            print('Comparison of item with serial_number = \'{0}\''.format(df1_item['serial_number']))

            correct_count = 0

            if all(x == 'notfound' for x in match_matrix.values()):
                print('\tThe specified item not found.')
            else:
                if match_matrix['unit_of_measurement'] == 'correct':
                    correct_count += 1
                    print("\tThe value of 'unit_of_measurement' is correct.")
                else:
                    print("\tThe value of 'unit_of_measurement' is incorrect.")

                if match_matrix['item_quantity'] == 'correct':
                    correct_count += 1
                    print("\tThe value of 'item_quantity' is correct.")
                else:
                    print("\tThe value of 'item_quantity' is incorrect.")

                if match_matrix['unit_price'] == 'correct':
                    correct_count += 1
                    print("\tThe value of 'unit_price' is correct.")
                else:
                    print("\tThe value of 'unit_price' is incorrect.")

                if match_matrix['hsn_code'] == 'correct':
                    correct_count += 1
                    print("\tThe value of 'hsn_code' is correct.")
                else:
                    print("\tThe value of 'hsn_code' is incorrect.")

                if match_matrix['tax_amount'] == 'correct':
                    correct_count += 1
                    print("\tThe value of 'tax_amount' is correct.")
                else:
                    print("\tThe value of 'tax_amount' is incorrect.")

                if match_matrix['basic_amount'] == 'correct':
                    correct_count += 1
                    print("\tThe value of 'basic_amount' is correct.")
                else:
                    print("\tThe value of 'basic_amount' is incorrect.")

            column_accuracy = (correct_count/6.0) * 100
            accuracy_list.append(column_accuracy)
            print(accuracy_list)


def automate_test_of_extracted_line_item():
    json_out = json.load(open(os.path.join(Path.home(), "Downloads", "15060186086.json")))
    print(json_out['erp_line_items'])
    df1 = json_out['erp_line_items']
    change_df1_headers_according_to_df2_headers(df1)
    df1 = combine_df1_items(df1)
    xl_path = os.path.join(Path.home(), "Downloads", "15060186086 TSP.pdf.xlsx")
    xl_df = pd.read_excel(xl_path, sheet_name="Sheet1", na_filter=False)
    df2 = xl_df.to_dict(orient='records')
    print(xl_df.to_dict(orient='records'))
    df2 = filter_df2_dict(df2)
    compare_df1_item_count_with_df2_item_count(df1, df2)
    compare_df1_total_with_df2_total(df1, df2)
    compare_df1_values_with_df2_values(df1, df2)


automate_test_of_extracted_line_item()
