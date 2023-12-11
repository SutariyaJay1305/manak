import os
from django.shortcuts import render,redirect
from django.db.models import F
from .froms import loginForm
from .models import UIManager,DataManager,User,MainTables
from django.contrib.auth import authenticate,login as auth_login,logout
from django.http import  JsonResponse
from decimal import Decimal
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from django.shortcuts import render,HttpResponse,redirect


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.conf import settings
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@csrf_exempt  # Use this decorator for simplicity. Consider proper CSRF protection in production.
def print(request):
    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    excel_file_path = os.path.join(BASE_DIR,'files/hello.xlsx')
    # Specify the path to your Excel file

    # Read the Excel file into a DataFrame using pandas
    df = pd.read_excel(excel_file_path)

    # Create a PDF file
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'output_file.pdf')
    pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Set the starting position for drawing in the PDF
    x_position = 50
    y_position = letter[1] - 50

    # Loop through the DataFrame and write to the PDF
    for _, row in df.iterrows():
        for col_name, cell_value in row.items():
            pdf_canvas.drawString(x_position, y_position, f"{col_name}: {cell_value}")
            x_position += 150  # Adjust as needed for your layout

        x_position = 50  # Reset X position for the next row
        y_position -= 20  # Move to the next row

    # Save the PDF
    pdf_canvas.save()

    # Prepare the response
    with open(pdf_file_path, 'rb') as file:
        pdf_content = file.read()

    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_file_path)}"'

    # Delete the generated PDF file after sending it in the response
    os.remove(pdf_file_path)

    return response


# Create your views here.

def custom_round_up(decimal_value):
    integer_part = int(decimal_value)
    fractional_part = Decimal(decimal_value) - integer_part
    if fractional_part >= 0.5:
        return integer_part + 1
    else:
        return integer_part
    
def index(request):

    text1 = UIManager.objects.get(UI_position=1).text_description
    text2 = UIManager.objects.get(UI_position=2).text_description
    context = {
        "text1":text1,
        "text2":text2,
        
        }
    
    return render(request,'index.html',context)

def register(request):
   if request.method == 'POST':
        email=request.POST.get("inputEmail4")
        password=request.POST.get("inputPassword5")
        confirmpassword=request.POST.get("inputPassword6")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        mobile=request.POST.get("mobile")
        if User.objects.filter(email=email).exists():
          return render(request,'register.html',{"message":"User Already Exist"})
        else:
            if password!=confirmpassword:
                return render(request,'register.html',{"message":"Password and Confirm Password is not matching"})
            else:
                created = User.objects.create_user(username=email,email=email,first_name=firstname,last_name=lastname,password=password,phone_number=mobile)
                auth_login(request,created)
                user=request.user
                return redirect('report')
   else:
      print(type(User))
      return render(request,'register.html')
   
def login(request):
        if request.method=="POST":
            form=loginForm(request.POST)
            if form.is_valid:
                username = request.POST["username"]
                password = request.POST["password"]
                user= authenticate(username=username,password=password)

                if user is not None:
                    print("Login done")
                    auth_login(request,user)
                   
                    if user.is_superuser == True:
                        return redirect('admin_report')
                    else:
                        return redirect('report')
                else:
                    return render(request,'login.html',{'message':"Username Or Password Is Incorrect"})
        
        else:
            print(request.user.is_authenticated)
            if request.user.is_authenticated:
                user=request.user
                print(user)

                if user.is_superuser == True:
                    return redirect('admin_report')
                else:
                    return redirect('report')
                
            else:
                return render(request,'login.html')
    
def logoutUser(request):
    logout(request)
    return redirect('index')

def report(request):
    convert_excel_to_pdf()
    if request.method == "GET":
        try:
            shape = request.GET['shape']
        except :
            shape = "round"
        main_tables = MainTables.objects.filter(shape__iexact=shape)
        data = DataManager.objects.filter(parent_table__in = main_tables)
    
    return render(request,'report.html',{"data":data,'type':shape})

def admin_report(request):
    try:
        shape = request.GET['shape']
    except :
        shape = "round"
    main_tables = MainTables.objects.filter(shape__iexact=shape)
    data = DataManager.objects.filter(parent_table__in = main_tables)
    print(data)
    return render(request,'admin_report.html',{"data":data,'type':shape})

def update_price(request):
    if request.method=="POST":
        per_change = request.POST["per_change"]
        change = request.POST["change"]
        shape = request.POST["shape"]
        main_tables = MainTables.objects.filter(shape__iexact=shape)
        if change=="increase":
            DataManager.objects.filter(parent_table__in = main_tables).update(
                current_percentage_change = int(per_change),
                last_percentage_change= F('current_percentage_change'),
                second_last_percentage_change = F('last_percentage_change'),
                D_IF=F('D_IF')+F('D_IF')*(int(per_change)/100),
                D_VV1=F('D_VV1')+F('D_VV1')*(int(per_change)/100),
                D_VV2=F('D_VV2')+F('D_VV2')*(int(per_change)/100),
                D_VS1=F('D_VS1')+F('D_VS1')*(int(per_change)/100),
                D_VS2=F('D_VS2')+F('D_VS2')*(int(per_change)/100),
                D_SI1=F('D_SI1')+F('D_SI1')*(int(per_change)/100),
                D_SI2=F('D_SI2')+F('D_SI2')*(int(per_change)/100),

                E_IF=F('E_IF')+F('E_IF')*(int(per_change)/100),
                E_VV1=F('E_VV1')+F('E_VV1')*(int(per_change)/100),
                E_VV2=F('E_VV2')+F('E_VV2')*(int(per_change)/100),
                E_VS1=F('E_VS1')+F('E_VS1')*(int(per_change)/100),
                E_VS2=F('E_VS2')+F('E_VS2')*(int(per_change)/100),
                E_SI1=F('E_SI1')+F('E_SI1')*(int(per_change)/100),
                E_SI2=F('E_SI2')+F('E_SI2')*(int(per_change)/100),

                F_IF=F('F_IF')+F('F_IF')*(int(per_change)/100),
                F_VV1=F('F_VV1')+F('F_VV1')*(int(per_change)/100),
                F_VV2=F('F_VV2')+F('F_VV2')*(int(per_change)/100),
                F_VS1=F('F_VS1')+F('F_VS1')*(int(per_change)/100),
                F_VS2=F('F_VS2')+F('F_VS2')*(int(per_change)/100),
                F_SI1=F('F_SI1')+F('F_SI1')*(int(per_change)/100),
                F_SI2=F('F_SI2')+F('F_SI2')*(int(per_change)/100),

                G_IF=F('G_IF')+F('G_IF')*(int(per_change)/100),
                G_VV1=F('G_VV1')+F('G_VV1')*(int(per_change)/100),
                G_VV2=F('G_VV2')+F('G_VV2')*(int(per_change)/100),
                G_VS1=F('G_VS1')+F('G_VS1')*(int(per_change)/100),
                G_VS2=F('G_VS2')+F('G_VS2')*(int(per_change)/100),
                G_SI1=F('G_SI1')+F('G_SI1')*(int(per_change)/100),
                G_SI2=F('G_SI2')+F('G_SI2')*(int(per_change)/100),

                H_IF=F('H_IF')+F('H_IF')*(int(per_change)/100),
                H_VV1=F('H_VV1')+F('H_VV1')*(int(per_change)/100),
                H_VV2=F('H_VV2')+F('H_VV2')*(int(per_change)/100),
                H_VS1=F('H_VS1')+F('H_VS1')*(int(per_change)/100),
                H_VS2=F('H_VS2')+F('H_VS2')*(int(per_change)/100),
                H_SI1=F('H_SI1')+F('H_SI1')*(int(per_change)/100),

                I_IF=F('I_IF')+F('I_IF')*(int(per_change)/100),
                I_VV1=F('I_VV1')+F('I_VV1')*(int(per_change)/100),
                I_VV2=F('I_VV2')+F('I_VV2')*(int(per_change)/100),
                I_VS1=F('I_VS1')+F('I_VS1')*(int(per_change)/100),
                I_VS2=F('I_VS2')+F('I_VS2')*(int(per_change)/100),
                I_SI1=F('I_SI1')+F('I_SI1')*(int(per_change)/100),
                I_SI2=F('I_SI2')+F('I_SI2')*(int(per_change)/100),

                J_IF=F('J_IF')+F('J_IF')*(int(per_change)/100),
                J_VV1=F('J_VV1')+F('J_VV1')*(int(per_change)/100),
                J_VV2=F('J_VV2')+F('J_VV2')*(int(per_change)/100),
                J_VS1=F('J_VS1')+F('J_VS1')*(int(per_change)/100),
                J_VS2=F('J_VS2')+F('J_VS2')*(int(per_change)/100),
                J_SI1=F('J_SI1')+F('J_SI1')*(int(per_change)/100),
                J_SI2=F('J_SI2')+F('J_SI2')*(int(per_change)/100),
                )

        else:
            DataManager.objects.filter(parent_table__in = main_tables).update(
                current_percentage_change = int(per_change),
                last_percentage_change= F('current_percentage_change'),
                second_last_percentage_change = F('last_percentage_change'),
                D_IF=F('D_IF')-F('D_IF')*(int(per_change)/100),
                D_VV1=F('D_VV1')-F('D_VV1')*(int(per_change)/100),
                D_VV2=F('D_VV2')-F('D_VV2')*(int(per_change)/100),
                D_VS1=F('D_VS1')-F('D_VS1')*(int(per_change)/100),
                D_VS2=F('D_VS2')-F('D_VS2')*(int(per_change)/100),
                D_SI1=F('D_SI1')-F('D_SI1')*(int(per_change)/100),
                D_SI2=F('D_SI2')-F('D_SI2')*(int(per_change)/100),

                E_IF=F('E_IF')-F('E_IF')*(int(per_change)/100),
                E_VV1=F('E_VV1')-F('E_VV1')*(int(per_change)/100),
                E_VV2=F('E_VV2')-F('E_VV2')*(int(per_change)/100),
                E_VS1=F('E_VS1')-F('E_VS1')*(int(per_change)/100),
                E_VS2=F('E_VS2')-F('E_VS2')*(int(per_change)/100),
                E_SI1=F('E_SI1')-F('E_SI1')*(int(per_change)/100),
                E_SI2=F('E_SI2')-F('E_SI2')*(int(per_change)/100),

                F_IF=F('F_IF')-F('F_IF')*(int(per_change)/100),
                F_VV1=F('F_VV1')-F('F_VV1')*(int(per_change)/100),
                F_VV2=F('F_VV2')-F('F_VV2')*(int(per_change)/100),
                F_VS1=F('F_VS1')-F('F_VS1')*(int(per_change)/100),
                F_VS2=F('F_VS2')-F('F_VS2')*(int(per_change)/100),
                F_SI1=F('F_SI1')-F('F_SI1')*(int(per_change)/100),
                F_SI2=F('F_SI2')-F('F_SI2')*(int(per_change)/100),

                G_IF=F('G_IF')-F('G_IF')*(int(per_change)/100),
                G_VV1=F('G_VV1')-F('G_VV1')*(int(per_change)/100),
                G_VV2=F('G_VV2')-F('G_VV2')*(int(per_change)/100),
                G_VS1=F('G_VS1')-F('G_VS1')*(int(per_change)/100),
                G_VS2=F('G_VS2')-F('G_VS2')*(int(per_change)/100),
                G_SI1=F('G_SI1')-F('G_SI1')*(int(per_change)/100),
                G_SI2=F('G_SI2')-F('G_SI2')*(int(per_change)/100),

                H_IF=F('H_IF')-F('H_IF')*(int(per_change)/100),
                H_VV1=F('H_VV1')-F('H_VV1')*(int(per_change)/100),
                H_VV2=F('H_VV2')-F('H_VV2')*(int(per_change)/100),
                H_VS1=F('H_VS1')-F('H_VS1')*(int(per_change)/100),
                H_VS2=F('H_VS2')-F('H_VS2')*(int(per_change)/100),
                H_SI1=F('H_SI1')-F('H_SI1')*(int(per_change)/100),

                I_IF=F('I_IF')-F('I_IF')*(int(per_change)/100),
                I_VV1=F('I_VV1')-F('I_VV1')*(int(per_change)/100),
                I_VV2=F('I_VV2')-F('I_VV2')*(int(per_change)/100),
                I_VS1=F('I_VS1')-F('I_VS1')*(int(per_change)/100),
                I_VS2=F('I_VS2')-F('I_VS2')*(int(per_change)/100),
                I_SI1=F('I_SI1')-F('I_SI1')*(int(per_change)/100),
                I_SI2=F('I_SI2')-F('I_SI2')*(int(per_change)/100),

                J_IF=F('J_IF')-F('J_IF')*(int(per_change)/100),
                J_VV1=F('J_VV1')-F('J_VV1')*(int(per_change)/100),
                J_VV2=F('J_VV2')-F('J_VV2')*(int(per_change)/100),
                J_VS1=F('J_VS1')-F('J_VS1')*(int(per_change)/100),
                J_VS2=F('J_VS2')-F('J_VS2')*(int(per_change)/100),
                J_SI1=F('J_SI1')-F('J_SI1')*(int(per_change)/100),
                J_SI2=F('J_SI2')-F('J_SI2')*(int(per_change)/100),
                )
        return JsonResponse({'success': True})

def update_report(request):
    if request.method=="POST":
        position = request.POST["table_position"]
        D_IF  = request.POST["D_IF"]
        D_VV1 = request.POST["D_VV1"]
        D_VV2 = request.POST["D_VV2"]
        D_VS1 = request.POST["D_VS1"]
        D_VS2 = request.POST["D_VS2"]
        D_SI1 = request.POST["D_SI1"]
        D_SI2 = request.POST["D_SI2"]

        E_IF = request.POST["E_IF"]
        E_VV1 = request.POST["E_VV1"]
        E_VV2 = request.POST["E_VV2"]
        E_VS1 = request.POST["E_VS1"]
        E_VS2 = request.POST["E_VS2"]
        E_SI1 = request.POST["E_SI1"]
        E_SI2 = request.POST["E_SI2"]

        F_IF = request.POST["F_IF"]
        F_VV1 = request.POST["F_VV1"]
        F_VV2 = request.POST["F_VV2"]
        F_VS1 = request.POST["F_VS1"]
        F_VS2 = request.POST["F_VS2"]
        F_SI1 = request.POST["F_SI1"]
        F_SI2 = request.POST["F_SI2"]

        G_IF = request.POST["G_IF"]
        G_VV1 = request.POST["G_VV1"]
        G_VV2 = request.POST["G_VV2"]
        G_VS1 = request.POST["G_VS1"]
        G_VS2 = request.POST["G_VS2"]
        G_SI1 = request.POST["G_SI1"]
        G_SI2 = request.POST["G_SI2"]

        H_IF = request.POST["H_IF"]
        H_VV1 = request.POST["H_VV1"]
        H_VV2 = request.POST["H_VV2"]
        H_VS1 = request.POST["H_VS1"]
        H_VS2 = request.POST["H_VS2"]
        H_SI1 = request.POST["H_SI1"]
        H_SI2 = request.POST["H_SI2"]

        I_IF = request.POST["I_IF"]
        I_VV1 = request.POST["I_VV1"]
        I_VV2 = request.POST["I_VV2"]
        I_VS1 = request.POST["I_VS1"]
        I_VS2 = request.POST["I_VS2"]
        I_SI1 = request.POST["I_SI1"]
        I_SI2 = request.POST["I_SI2"]

        J_IF = request.POST["J_IF"]
        J_VV1 = request.POST["J_VV1"]
        J_VV2 = request.POST["J_VV2"]
        J_VS1 = request.POST["J_VS1"]
        J_VS2 = request.POST["J_VS2"]
        J_SI1 = request.POST["J_SI1"]
        J_SI2 = request.POST["J_SI2"]

        updated_val = [D_IF,D_VV1,D_VV2,D_VS1,D_VS2,D_SI1,D_SI2,E_IF,E_VV1,E_VV2,E_VS1,E_VS2,E_SI1,E_SI2,F_IF,F_VV1,F_VV2,F_VS1,F_VS2,F_SI1,F_SI2,G_IF,G_VV1,G_VV2,G_VS1,G_VS2,G_SI1,G_SI2,H_IF,H_VV1,H_VV2,H_VS1,H_VS2,H_SI1,H_SI2,I_IF,I_VV1,I_VV2,I_VS1,I_VS2,I_SI1,I_SI2,J_IF,J_VV1,J_VV2,J_VS1,J_VS2,J_SI1,J_SI2]

        q = DataManager.objects.filter(postion=position)
        data = q.values('D_IF','D_VV1','D_VV2','D_VS1','D_VS2','D_SI1','D_SI2','E_IF','E_VV1','E_VV2','E_VS1','E_VS2','E_SI1','E_SI2','F_IF','F_VV1','F_VV2','F_VS1','F_VS2','F_SI1','F_SI2','G_IF','G_VV1','G_VV2','G_VS1','G_VS2','G_SI1','G_SI2','H_IF','H_VV1','H_VV2','H_VS1','H_VS2','H_SI1','H_SI2','I_IF','I_VV1','I_VV2','I_VS1','I_VS2','I_SI1','I_SI2','J_IF','J_VV1','J_VV2','J_VS1','J_VS2','J_SI1','J_SI2')[0]
        count = 0 
        increase = q.first().increased
        drop = q.first().dropped
        flag = True
        query = {}
        
        for x,y in data.items():
            
            if custom_round_up(y) != custom_round_up(updated_val[count]):
                print(round(int(y)) != int(updated_val[count]))
                print(int(updated_val[count]))
                if flag :
                    increase = ''
                    drop = ''
                print(round(int(y)) ,"::",updated_val[count])
                if custom_round_up(y) < custom_round_up(updated_val[count]):
                   increase = ','.join([increase, str(x)])
                else:
                    drop = ','.join([drop, str(x)])
                query[x] = int(updated_val[count])    
                flag = False
            count += 1   
        query['increased'] = increase
        query['dropped'] = drop
        q.update(**query)
        return JsonResponse({'success': True})

def remove_changes(request):
    DataManager.objects.all().update(increased="",dropped="")
    return JsonResponse({'success': True})


    



def excel_creation():
    
    workbook = xlsxwriter.Workbook('files/hello.xlsx')
    worksheet = workbook.add_worksheet()

    # Cell Merging
    # Formating
    title_format = workbook.add_format(
    {
        "bold": 1,
        "font":"Arial Black",
        "font_size":20,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",
        
    })
    subtitle_format = workbook.add_format(
       {
        "font":"Agency FB",
        "font_size":8,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",
    })

    price_box_drop = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":8,
        "bold": 1,
        "border":1,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",

        })
    
    price_box_up = workbook.add_format(
       {
        "font":"Agency FB",
        "font_size":8,
        "bold": 1,
        "border":1,
        "color":"white",
        "align": "center",
        "valign": "vcenter",
        "fg_color": "#808080",
        })
    
    common = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":8,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",
        'right': 5,
        })
    
    table_heading = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":8,
        "color":"white",
        "align": "center",
        "valign": "vcenter",
        "fg_color": "#000000",

        })

    table_tile = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":8,
        "bold": 1,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",

        })

    # Column height
    worksheet.set_column(0, 8, 3.83)
    worksheet.set_column(9, 9, 0.27)
    worksheet.set_column(10, 17, 3.83)

    worksheet.set_default_row(12)
   

    # Title
    worksheet.set_row(0,2)
    worksheet.set_row(1,23.25)
    worksheet.merge_range("A1:R2", "MANAK LG-DIAMOND REPORT", title_format)
    
    worksheet.set_row(2,12)

    worksheet.set_row(3,11.25)
    worksheet.merge_range("B4:R4", "Manak report is based on all major labs and its production of both HPHT & CVD (monthly/annually ). No liability is assumed as to accuracy of this information", subtitle_format)
    
    worksheet.set_row(4,11.25)
    worksheet.set_row(5,7.5)
    worksheet.set_row(6,7.5)
    worksheet.set_row(7,7.5)
    worksheet.set_row(8,4.5)

    worksheet.set_row(9,12)
    worksheet.merge_range("B10:G10", "Price change : Dark Cell - Increased / Bold - Dropped ", common)
    

    worksheet.merge_range("H10:I10", '5.2 | increased',price_box_up)
    worksheet.merge_range("K10:L10", '5.2 | dropped',price_box_drop)
   
    # Footer
    footer_font = workbook.add_format(
        {
        "font":"Bahnschrift",
        "font_size":10,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",

        })
    worksheet.set_row(57,48)
    worksheet.merge_range("A58:I58", "For Price Update : ManakReport.com ", footer_font)


   

    # Table data 
    data = DataManager.objects.all()
    row_1 = 13
    row_2 = 13
    col = 'A'
    side = 0
    for x in data:
        if side == 0:
            # Table Title
            worksheet.merge_range('A'+str(row_1)+':B'+str(row_1), x.parent_table.carat_range,table_tile)
            worksheet.write('D'+str(row_1)+':E'+str(row_1), x.parent_table.tabel_date.strftime("%m/%d/%y"),common)
            worksheet.write('H'+str(row_1), x.parent_table.shape,table_tile) 

            # Table heading
            worksheet.write('A'+str(row_1+1), 'MANAK',table_heading)
            worksheet.write('B'+str(row_1+1), 'D',table_heading)
            worksheet.write('C'+str(row_1+1), 'E',table_heading)
            worksheet.write('D'+str(row_1+1), 'F',table_heading)
            worksheet.write('E'+str(row_1+1), 'G',table_heading)
            worksheet.write('F'+str(row_1+1), 'H',table_heading)
            worksheet.write('G'+str(row_1+1), 'I',table_heading)
            worksheet.write('H'+str(row_1+1), 'J',table_heading)

            worksheet.write('A'+str(row_1+2), 'IF',table_heading)
            worksheet.write('A'+str(row_1+3), 'VV1',table_heading)
            worksheet.write('A'+str(row_1+4), 'VV2',table_heading)
            worksheet.write('A'+str(row_1+5), 'VS1',table_heading)
            worksheet.write('A'+str(row_1+6), 'VS2',table_heading)
            worksheet.write('A'+str(row_1+7), 'SI1',table_heading)
            worksheet.write('A'+str(row_1+8), 'SI2',table_heading)

            worksheet.write('A'+str(row_1+9)+':H'+str(row_1+9), x.parent_table.text_description,common)
            
            # row_1 IF +str(row_1+2)
            worksheet.write('B'+str(row_1+2),x.D_IF,common)
            worksheet.write('C'+str(row_1+2),x.E_IF,common)
            worksheet.write('D'+str(row_1+2),x.F_IF,common)
            worksheet.write('E'+str(row_1+2),x.G_IF,common)
            worksheet.write('F'+str(row_1+2),x.H_IF,common)
            worksheet.write('G'+str(row_1+2),x.I_IF,common)
            worksheet.write('H'+str(row_1+2),x.J_IF,common)

            # row_1 VV1 +str(row_1+3)
            worksheet.write('B'+str(row_1+3), x.D_VV1,common)
            worksheet.write('C'+str(row_1+3), x.E_VV1,common)
            worksheet.write('D'+str(row_1+3), x.F_VV1,common)
            worksheet.write('E'+str(row_1+3), x.G_VV1,common)
            worksheet.write('F'+str(row_1+3), x.H_VV1,common)
            worksheet.write('G'+str(row_1+3), x.I_VV1,common)
            worksheet.write('H'+str(row_1+3), x.J_VV1,common)

            # row_1 VV2 +str(row_1+4)
            worksheet.write('B'+str(row_1+4), x.D_VV2,common)
            worksheet.write('C'+str(row_1+4), x.E_VV2,common)
            worksheet.write('D'+str(row_1+4), x.F_VV2,common)
            worksheet.write('E'+str(row_1+4), x.G_VV2,common)
            worksheet.write('F'+str(row_1+4), x.H_VV2,common)
            worksheet.write('G'+str(row_1+4), x.I_VV2,common)
            worksheet.write('H'+str(row_1+4), x.J_VV2,common)

            # row_1 VS1 +str(row_1+5)
            worksheet.write('B'+str(row_1+5), x.D_VS1,common)
            worksheet.write('C'+str(row_1+5), x.E_VS1,common)
            worksheet.write('D'+str(row_1+5), x.F_VS1,common)
            worksheet.write('E'+str(row_1+5), x.G_VS1,common)
            worksheet.write('F'+str(row_1+5), x.H_VS1,common)
            worksheet.write('G'+str(row_1+5), x.I_VS1,common)
            worksheet.write('H'+str(row_1+5), x.J_VS1,common)

            # row_1 VS2 +str(row_1+6)
            worksheet.write('B'+str(row_1+6), x.D_VS2,common)
            worksheet.write('C'+str(row_1+6), x.E_VS2,common)
            worksheet.write('D'+str(row_1+6), x.F_VS2,common)
            worksheet.write('E'+str(row_1+6), x.G_VS2,common)
            worksheet.write('F'+str(row_1+6), x.H_VS2,common)
            worksheet.write('G'+str(row_1+6), x.I_VS2,common)
            worksheet.write('H'+str(row_1+6), x.J_VS2,common)


            # row_1 SI1 +str(row_1+7)
            worksheet.write('B'+str(row_1+7), x.D_SI1,common)
            worksheet.write('C'+str(row_1+7), x.E_SI1,common)
            worksheet.write('D'+str(row_1+7), x.F_SI1,common)
            worksheet.write('E'+str(row_1+7), x.G_SI1,common)
            worksheet.write('F'+str(row_1+7), x.H_SI1,common)
            worksheet.write('G'+str(row_1+7), x.I_SI1,common)
            worksheet.write('H'+str(row_1+7), x.J_SI1,common)


            # row_1 SI2 +str(row_1+8)
            worksheet.write('B'+str(row_1+8), x.D_SI2,common)
            worksheet.write('C'+str(row_1+8), x.E_SI2,common)
            worksheet.write('D'+str(row_1+8), x.F_SI2,common)
            worksheet.write('E'+str(row_1+8), x.G_SI2,common)
            worksheet.write('F'+str(row_1+8), x.H_SI2,common)
            worksheet.write('G'+str(row_1+8), x.I_SI2,common)
            worksheet.write('H'+str(row_1+8), x.J_SI2,common)

            row_1 += 11
            side = 1
        else:

             # Table Title
            worksheet.merge_range('K'+str(row_2)+':L'+str(row_2), x.parent_table.carat_range,common)
            worksheet.write('N'+str(row_2)+':O'+str(row_2), x.parent_table.tabel_date.strftime("%m/%d/%y"),common)
            worksheet.write('R'+str(row_2), x.parent_table.shape,common) 

            # Table heading
            worksheet.write('K'+str(row_2+1), 'MANAK',table_heading)
            worksheet.write('L'+str(row_2+1), 'N',table_heading)
            worksheet.write('M'+str(row_2+1), 'E',table_heading)
            worksheet.write('N'+str(row_2+1), 'F',table_heading)
            worksheet.write('O'+str(row_2+1), 'G',table_heading)
            worksheet.write('P'+str(row_2+1), 'H',table_heading)
            worksheet.write('Q'+str(row_2+1), 'I',table_heading)
            worksheet.write('R'+str(row_2+1), 'J',table_heading)

            worksheet.write('K'+str(row_2+2), 'IF',table_heading)
            worksheet.write('K'+str(row_2+3), 'VV1',table_heading)
            worksheet.write('K'+str(row_2+4), 'VV2',table_heading)
            worksheet.write('K'+str(row_2+5), 'VS1',table_heading)
            worksheet.write('K'+str(row_2+6), 'VS2',table_heading)
            worksheet.write('K'+str(row_2+7), 'SI1',table_heading)
            worksheet.write('K'+str(row_2+8), 'SI2',table_heading)

            worksheet.write('K'+str(row_2+9)+':R'+str(row_2+9), x.parent_table.text_description,common)
            
            # row_2 IF +str(row_2+2)
            worksheet.write('L'+str(row_2+2),x.D_IF,common)
            worksheet.write('M'+str(row_2+2),x.E_IF,common)
            worksheet.write('N'+str(row_2+2),x.F_IF,common)
            worksheet.write('O'+str(row_2+2),x.G_IF,common)
            worksheet.write('P'+str(row_2+2),x.H_IF,common)
            worksheet.write('Q'+str(row_2+2),x.I_IF,common)
            worksheet.write('R'+str(row_2+2),x.J_IF,common)

            # row_2 VV1 +str(row_2+3)
            worksheet.write('L'+str(row_2+3), x.D_VV1,common)
            worksheet.write('M'+str(row_2+3), x.E_VV1,common)
            worksheet.write('N'+str(row_2+3), x.F_VV1,common)
            worksheet.write('O'+str(row_2+3), x.G_VV1,common)
            worksheet.write('P'+str(row_2+3), x.H_VV1,common)
            worksheet.write('Q'+str(row_2+3), x.I_VV1,common)
            worksheet.write('R'+str(row_2+3), x.J_VV1,common)

            # row_2 VV2 +str(row_2+4)
            worksheet.write('L'+str(row_2+4), x.D_VV2,common)
            worksheet.write('M'+str(row_2+4), x.E_VV2,common)
            worksheet.write('N'+str(row_2+4), x.F_VV2,common)
            worksheet.write('O'+str(row_2+4), x.G_VV2,common)
            worksheet.write('P'+str(row_2+4), x.H_VV2,common)
            worksheet.write('Q'+str(row_2+4), x.I_VV2,common)
            worksheet.write('R'+str(row_2+4), x.J_VV2,common)

            # row_2 VS1 +str(row_2+5)
            worksheet.write('L'+str(row_2+5), x.D_VS1,common)
            worksheet.write('M'+str(row_2+5), x.E_VS1,common)
            worksheet.write('N'+str(row_2+5), x.F_VS1,common)
            worksheet.write('O'+str(row_2+5), x.G_VS1,common)
            worksheet.write('P'+str(row_2+5), x.H_VS1,common)
            worksheet.write('Q'+str(row_2+5), x.I_VS1,common)
            worksheet.write('R'+str(row_2+5), x.J_VS1,common)

            # row_2 VS2 +str(row_2+6)
            worksheet.write('L'+str(row_2+6), x.D_VS2,common)
            worksheet.write('M'+str(row_2+6), x.E_VS2,common)
            worksheet.write('N'+str(row_2+6), x.F_VS2,common)
            worksheet.write('O'+str(row_2+6), x.G_VS2,common)
            worksheet.write('P'+str(row_2+6), x.H_VS2,common)
            worksheet.write('Q'+str(row_2+6), x.I_VS2,common)
            worksheet.write('R'+str(row_2+6), x.J_VS2,common)


            # row_2 SI1 +str(row_2+7)
            worksheet.write('L'+str(row_2+7), x.D_SI1,common)
            worksheet.write('M'+str(row_2+7), x.E_SI1,common)
            worksheet.write('N'+str(row_2+7), x.F_SI1,common)
            worksheet.write('O'+str(row_2+7), x.G_SI1,common)
            worksheet.write('P'+str(row_2+7), x.H_SI1,common)
            worksheet.write('Q'+str(row_2+7), x.I_SI1,common)
            worksheet.write('R'+str(row_2+7), x.J_SI1,common)


            # row_2 SI2 +str(row_2+8)
            worksheet.write('L'+str(row_2+8), x.D_SI2,common)
            worksheet.write('M'+str(row_2+8), x.E_SI2,common)
            worksheet.write('N'+str(row_2+8), x.F_SI2,common)
            worksheet.write('O'+str(row_2+8), x.G_SI2,common)
            worksheet.write('P'+str(row_2+8), x.H_SI2,common)
            worksheet.write('Q'+str(row_2+8), x.I_SI2,common)
            worksheet.write('R'+str(row_2+8), x.J_SI2,common)

            row_2 += 11
            side = 0



    workbook.close()
    import os
    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    excel_path = os.path.join(BASE_DIR,'hello.xlsx')
    

def convert_excel_to_pdf():
    import os
    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    excel_file_path = os.path.join(BASE_DIR,'files/hello.xlsx')
    # Read the Excel file into a DataFrame using pandas
    df = pd.read_excel(excel_file_path)
    pdf_file_path = "oyi.pdf"

    # Create a PDF file
    pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Set the starting position for drawing in the PDF
    x_position = 50
    y_position = letter[1] - 50

    # Loop through the DataFrame and write to the PDF
    for _, row in df.iterrows():
        for col_name, cell_value in row.items():
            pdf_canvas.drawString(x_position, y_position, f"{col_name}: {cell_value}")
            x_position += 150  # Adjust as needed for your layout

        x_position = 50  # Reset X position for the next row
        y_position -= 20  # Move to the next row

    # Save the PDF
    pdf_canvas.save()

    print(f"Conversion from {excel_file_path} to {pdf_file_path} complete.")



def perform_excel_to_pdf():
        import os
        from pathlib import Path

        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
        
        excel_file = os.path.join(BASE_DIR,'files/hello.xlsx')
       
                
        if True: # excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
            try:
                df = pd.read_excel(excel_file)
            except FileNotFoundError:
                print("Excel file not found.")
                return
            except Exception as e:
                print("Error reading Excel file:", e)
                return

            pdf = FPDF()
            pdf.add_page()

            pdf.set_font("Arial", size=12)

            col_width = 40
            row_height = 10

            for col in df.columns:
                pdf.cell(col_width, row_height, txt=str(col), border=1)
            pdf.ln(row_height)

            for index, row in df.iterrows():
                for col in df.columns:
                    pdf.cell(col_width, row_height, txt=str(row[col]), border=1)
                pdf.ln(row_height)

            try:
                pdf_file="output_pdf_file.pdf"
                pdf.output(pdf_file)
                print(f"PDF file '{pdf_file}' created successfully.")
                with open("output_pdf_file.pdf", 'rb') as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="output_pdf_file.pdf"'
                    return response

            except Exception as e:
                print("Error creating PDF file:", e)

        return HttpResponse("Excel uploaded successfully")




