# coding=utf-8
import sys

from CodePath import ExcelUtils, XmlUtils

reload(sys)
sys.setdefaultencoding('utf8')

excelPath = "../super_lang_vi.xls"
# fromResPath = "../Easy"
toResPath = "../Super"

# XmlUtils.import_lang_from_xml(fromResPath, toResPath)
ExcelUtils.import_lang_from_excel(excelPath, toResPath)
# ExcelUtils.write_lang_to_excel(XmlUtils.parse_string_path(toResPath + "/values/strings.xml"), "lang_en", toResPath + "/super_en.xls")
