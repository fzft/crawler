import xlrd
import uuid
import utils.helper.file_operate as file_operate


def open_excel(file,encode=None):
    try:
        if encode:
            data = xlrd.open_workbook(file, encoding_override=encode)
        else:
            data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print("文件打开失败,str(e)是",str(e))

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0,by_index=0,encode=None):
    data = open_excel(file,encode)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file,colnameindex=0,by_name=u'***'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list


def excel_table_byindex_tocredit(file,colum,start_row=0,last_row=0,by_index=0,encode=None):
    data = open_excel(file,encode)
    if not data:
        return []
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    # ncols = table.ncols #列数
    # colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(start_row,nrows-last_row):
         row = table.row_values(rownum)
         if row:
             app = []
             for i in colum:
                app.append(row[i])
             list.append(app)
    return list


def excel_analyze(data,colum,start_row=0,last_row=0,by_index=0,encode=None):
    try:
        filename = str(uuid.uuid1()).replace("-","")+".xls"
        file_operate.save_file(filename,data)

        list = excel_table_byindex_tocredit(filename,colum,start_row,last_row,by_index,encode=encode)
        
        return list
    except Exception as e:
        print (e)
        return []
    finally:
        file_operate.del_file(filename)

    pass
