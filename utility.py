import openpyxl 


excel_obj = openpyxl.load_workbook("datalog4.xlsx")
datasheet = excel_obj.active
sheet_index = 4

# class writeData:

#     def __init__(self):
#         self 

def writeData(pitch,yaw,roll,index):
    # writes data to datalog Excel file
    global sheet_index
    global datasheet

    try:
        datasheet[f"A{sheet_index}"] = pitch;
        datasheet[f"B{sheet_index}"] = yaw;
        datasheet[f"C{sheet_index}"] = roll;
       
    
    except(Exception):
        print(Exception)

    excel_obj.save("datalog4.xlsx")