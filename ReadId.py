# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET

# 递归遍历所有的节点
def foreachData(root_node, result_list):
    try:
        element_id = root_node.attrib[androidId]
        if element_id.find(addId) != -1:
            result_list.append([root_node.tag, element_id[len(addId):]])
    except KeyError:
        pass
        # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        foreachData(child, result_list)
    return

# 解析xml文件
def getXml(file_name):
    result_list = []
    root = ET.parse(file_name).getroot()
    foreachData(root, result_list)
    return result_list

# 打印txt文件
def printResultFile(result_list, output_filename, findViewById):
    if len(result_list) != 0:
        output = open(output_filename, "w")
        for result in result_list:
            type, id = result
            output.write(findViewById % (convertTypeName(type),
                        convertIdName(id), convertTypeName(type), id))
        output.close()

# 类名称去除包名防止出现（com.facebook.drawee.view.SimpleDraweeView）
def convertTypeName(typeName):
    resultName = typeName
    names = resultName.split('.')
    if len(names) > 1:
        resultName = names[len(names)-1]
    return resultName

# 将变量名变为驼峰式
def convertIdName(resourseId):
    resultName = ""
    names = resourseId.split('_')
    if len(names) != -1:
        for index in range(len(names)):
            if index == 0:
                resultName += names[index]
            else:
                resultName += names[index].capitalize()
    return resultName

if __name__ == '__main__':
    fileName = 'view.xml'
    outputFilename = fileName.replace(".xml", ".txt")
    androidId = "{http://schemas.android.com/apk/res/android}id"
    addId = "@+id/"
    findViewById = "%s %s = (%s) findViewById(R.id.%s);\n"
    R = getXml(fileName)
    printResultFile(R, outputFilename, findViewById)
