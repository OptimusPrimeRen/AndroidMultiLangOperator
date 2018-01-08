# coding=utf-8
import sys

import xlrd
import xlwt

from CodePath import XmlUtils

reload(sys)
sys.setdefaultencoding('utf8')


# 传入excel路径及需要添加多语言的android工程的res目录，补充多语言到对应strings.xml下
def import_lang_from_excel(excel_path, res_path):
    workbook = xlrd.open_workbook(excel_path)
    sheet1 = workbook.sheet_by_index(0)
    for (langId, langMap) in produce_table_map(sheet1).items():
        if langId == 'en':
            string_path = res_path + '/values/strings.xml'
        else:
            string_path = res_path + '/values-' + langId + '/strings.xml'
        print string_path
        # print langMap
        XmlUtils.append_string_to_xml(string_path, langMap)


# 传入table，产生excel table的map，key为多语言语种名称，value为一个多语言key与多语言真实语言对应的map
def produce_table_map(table):
    table_map = {}
    # table_rows = table.nrows  # 行数
    table_cols = table.ncols  # 列数
    for i in range(1, table_cols):
        # print table.row_values(i)
        lang_key = table.col_values(i)[0]
        lang_map = produce_lang_map(table.col_values(0), table.col_values(i))
        table_map[lang_key] = lang_map
    # print table_map
    return table_map


# 传入key数组及string数组，产生多语言map，key对应多语言的key，value对应多语言语言真实的语言
def produce_lang_map(key_array, value_array):
    lang_map = {}
    for i in range(1, len(key_array)):
        lang_map[key_array[i]] = value_array[i]
    # print lang_map
    return lang_map


# 将dict写入excel， dict key是strings.xml中的name，value是string
def write_lang_to_excel(string_dict, sheet_name, export_xls_path):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    for index, (mainKey, mainValue) in enumerate(string_dict.items()):
        # print index, mainKey, mainValue
        sheet.write(index, 0, mainKey)
        sheet.write(index, 1, mainValue)
    workbook.save(export_xls_path)
