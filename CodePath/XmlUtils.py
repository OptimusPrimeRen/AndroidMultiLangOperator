# coding=utf-8
import os
import xml.dom.minidom
import sys

import time

reload(sys)
sys.setdefaultencoding('utf8')

ISO_TIME_FORMAT = '%Y-%m-%d %X'


# 将from_res_path有的多语言补充到to_res_path，两个path都是android工程的res目录，此方法将遍历目录下的values文件夹
def import_lang_from_xml(from_res_path, to_res_path):
    for parent, dirNames, fileNames in os.walk(from_res_path):
        for dirName in dirNames:
            # print dirName
            if dirName.__contains__('values'):
                # print os.path.join(parent, dirName + '/string.xml')
                from_string_path = os.path.join(parent, dirName + '/strings.xml')
                to_string_path = os.path.join(to_res_path, dirName + '/strings.xml')
                import_lang_from_string_file(from_string_path, to_string_path)


# 将from_string_path有的多语言补充到to_string_path，两个path都是string.xml的路径
def import_lang_from_string_file(from_string_path, to_string_path):
    from_lang_dict = parse_string_path(from_string_path)
    to_string_dict = parse_string_path(to_string_path)
    need_supply_string_dict = produce_need_supply_string(from_lang_dict, to_string_dict)
    append_string_to_xml(to_string_path, need_supply_string_dict)


# 解析string.xml，转换为dict
def parse_string_path(string_path):
    string_dict = {}
    if os.path.exists(string_path):
        dom = xml.dom.minidom.parse(string_path)
        root = dom.documentElement
        for item in root.getElementsByTagName("string"):
            string_dict[item.getAttribute("name")] = item.firstChild.nodeValue
            # print string_dict
    return string_dict


# 对比两个dict，产生需要补充的的string dict
def produce_need_supply_string(from_string_dict, to_string_dict):
    need_supply_string_dict = {}
    for (mainKey, mainValue) in from_string_dict.items():
        if mainKey not in to_string_dict:
            need_supply_string_dict[mainKey] = from_string_dict.get(mainKey, -1)
            # print need_supply_string_dict
    return need_supply_string_dict


# 在string.xml文件后追加需要补充的string
def append_string_to_xml(string_xml_path, string_dict):
    if not os.path.exists(string_xml_path):
        return

    covert_html_tag(string_dict)

    string_xml_file = open(string_xml_path, 'r')
    file_line_list = string_xml_file.readlines()

    resource_tag_index = 0
    for index, line in enumerate(file_line_list):
        if line.__contains__('</resources>'):
            resource_tag_index = index

    current_time = time.strftime(ISO_TIME_FORMAT, time.localtime())
    file_line_list.insert(resource_tag_index, '\t<!--多语言补充 END ******' + current_time + '******-->\n\n')
    for (supplyKey, supplyValue) in string_dict.items():
        file_line_list.insert(resource_tag_index, '\t<string name="' + supplyKey + '">' + supplyValue + '</string>\n')
    file_line_list.insert(resource_tag_index, '\n\t<!--多语言补充 BEGIN ******' + current_time + '******-->\n')

    string_xml_file = open(string_xml_path, 'w')
    for line in file_line_list:
        string_xml_file.writelines(unicode(line))


# 将多语言中的 HTML标签转义
def covert_html_tag(string_dict):
    for (supplyKey, supplyValue) in string_dict.items():
        covert_value = supplyValue.replace('<', "&lt;")
        string_dict[supplyKey] = covert_value
