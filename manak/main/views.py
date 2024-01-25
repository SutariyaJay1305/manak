import mimetypes
import os
import uuid
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
import requests

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.conf import settings
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from user_payment.models import UserPayment

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# excel_file_path = os.path.join(BASE_DIR,'files/hello.xlsx')
# df = pd.read_excel(excel_file_path)
# pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'output_file.pdf')


from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.http import FileResponse

def send_pdf_response(request, file_name):
    print(file_name)
    url = f"/media/pdf/" + file_name
    file_path = f"{BASE_DIR}{url}"
    print(file_path)
    if os.path.exists(file_path):
        f = open(file_path, "rb")
        response = FileResponse(f, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="{}"'.format(file_name)
        return response
    else:
        return HttpResponse("File not found.")

@csrf_exempt
def printf(request):
    try:
        shape = request.POST["shape"]
    except Exception as e:
        print(e)
        shape = "round"
    print(shape)
    file_name = str(shape)+".pdf"
    file_path = "/files/" + file_name
    # file_path = os.path.join(BASE_DIR,pdf_file_name)
    print(file_path)
    if os.path.exists(file_path):
        f = open(file_path, "rb")
        response = FileResponse(f, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="{}"'.format(file_name)
        return response
    

    # with open(file_path, 'rb') as pdf_file:
    #     response = FileResponse(pdf_file, content_type='application/pdf')
    #     response['Content-Disposition'] = f'inline; filename="{pdf_file_name}"'
    #     return response


@csrf_exempt  # Use this decorator for simplicity. Consider proper CSRF protection in production.
def printffff(request):
    try:
        shape = request.POST["shape"]
    except Exception as e:
        print(e)
        shape = "round"
    pdf_file = "files/" + str(shape)+".pdf"
    # pdf_file = os.path.join(BASE_DIR,pdf_file_name)
    print(pdf_file)
    # Prepare the response
    with open(pdf_file, 'rb') as file:
        pdf_content = file.read()

    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_file)}"'

    # Delete the generated PDF file after sending it in the response
    os.remove(pdf_file)

    return response

def get_content_type (filename):
        return mimetypes.guess_type (filename)[0] or 'application/octet-stream'


def pdfcon(shape):
   
    file = 'media/pdf/'+ shape +".xlsx"
    excel_file_path = os.path.join(BASE_DIR,file)
    url = "https://pdf4me.p.rapidapi.com/RapidApi/ConvertToPdf"
    
    contenttype =  '%s' % get_content_type(excel_file_path)

    files_dic = { "File": (excel_file_path, open(excel_file_path, 'rb')) }
    boundary = str(uuid.uuid4())
    X_RapidAPI_Key = "4cebfa25b8msh2bd06fc9b25ed3dp13d394jsn1534b21262d4"
    # X_RapidAPI_Key = "453596cdb6msh20a6e1af4fed997p1a862bjsn1db820ae4fc9"
    
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        # "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "*/*",
        'X-RapidAPI-Key': X_RapidAPI_Key,
        
        "X-RapidAPI-Host": "pdf4me.p.rapidapi.com"
    }

    
    response = requests.post(url, files=files_dic, headers=headers)
    # lll

    

    print(response.json())
    try:
        b64 = response.json()['file']
    except Exception as e:
        print("error 1:::",e)
        files_dic1 = { "File": (excel_file_path, open(excel_file_path, 'rb')) }
        X_RapidAPI_Key = "453596cdb6msh20a6e1af4fed997p1a862bjsn1db820ae4fc9"
        # X_RapidAPI_Key = "4cebfa25b8msh2bd06fc9b25ed3dp13d394jsn1534b21262d4"
        headers['X-RapidAPI-Key'] = X_RapidAPI_Key
        print(headers)
        response1 = requests.post(url, files=files_dic1, headers=headers)
        print(response1.json())
        try:
            b64 = response1.json()['file']
        except Exception as e:
            print("error 2:::",e)
            try:
                print("error 1:::",e)
                files_dic1 = { "File": (excel_file_path, open(excel_file_path, 'rb')) }
                X_RapidAPI_Key = "d3e6296aabmsh39bcde3ff806342p1d79eajsn9ab46bf74945"
                headers['X-RapidAPI-Key'] = X_RapidAPI_Key
                print(headers)
                response1 = requests.post(url, files=files_dic1, headers=headers)
                print(response1.json())
                
                b64 = response1.json()['file']
                
            except Exception as e:
                print("error 2:::",e)

    # print(b64)
    file1 = open("myfile.txt", "w")
    
    # \n is placed to indicate EOL (End of Line)
    file1.write(b64)
    file1.close()
    
    
    # print(b64)
    # Import only b64decode function from the base64 module
    from base64 import b64decode

    # Define the Base64 string of the PDF file
        # Decode the Base64 string, making sure that it contains only valid characters
    bytes = b64decode(b64, validate=True)

    # Perform a basic validation to make sure that the result is a valid PDF file
    # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
    # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
    if bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    # Write the PDF contents to a local file
    pdf_file_name = "media/pdf/" + str(shape)+".pdf"
    pdf_file = os.path.join(BASE_DIR,pdf_file_name)
    f = open(pdf_file, 'wb')
    f.write(bytes)
    f.close()

 

    # import jpype
    # import asposecells
    # jpype.startJVM()
    # from asposecells.api import Workbook

    # # Create an instance of the Workbook class.
    # workbook = Workbook()

    # # Insert the words Hello World! into a cell accessed.
    # workbook.getWorksheets().get(0).getCells().get("A1").putValue("Hello World")

    # # Save as XLS file
    # workbook.save("output.xls")

    # # Save as XLSX file
    # workbook.save("output.xlsx")

    # # Save as ods file
    # workbook.save("output.ods")

    # jpype.shutdownJVM()

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
    text3 = UIManager.objects.get(UI_position=3).text_description
    if text3 == "-":
        text3=""
    context = {
        "text1":text1,
        "text2":text2,
        "text3":text3,
        
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
                return redirect('checkout')
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
                is_paid= UserPayment.objects.filter(app_user = request.user,stripe_checkout_id__isnull=False)
                if not is_paid.exists():
                    return redirect("checkout")
                
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
    # pdfcon()
    # excel_creation()
    is_paid= UserPayment.objects.filter(app_user = request.user.id,stripe_checkout_id__isnull=False)
    if not is_paid.exists():
        return redirect("checkout")
    # convert_excel_to_pdf()
    if request.method == "GET":
        try:
            shape = request.GET['shape']
        except :
            shape = "round"
        main_tables = MainTables.objects.filter(shape__iexact=shape)
        data = DataManager.objects.filter(parent_table__in = main_tables)
    text = "Manak rerport is based on all major labs and its production of both HPHT & CVD(monthly/annually). No liability is assumed as to accuracy of this information"
    try:
        text = UIManager.objects.get(UI_position=4).text_description
    except Exception as e:
        print(e)
    return render(request,'report.html',{"data":data,'type':shape,"text":text})


def guest(request):
    if request.method == "GET":
        try:
            shape = request.GET['shape']
        except :
            shape = "round"
        main_tables = MainTables.objects.filter(shape__iexact=shape)
        data = DataManager.objects.filter(parent_table__in = main_tables)
        text = "Manak rerport is based on all major labs and its production of both HPHT & CVD(monthly/annually). No liability is assumed as to accuracy of this information"
        try:
            text = UIManager.objects.get(UI_position=4).text_description
        except Exception as e:
            print(e)

    
    return render(request,'guest_report.html',{"data":data,'type':shape,"text":text})



def admin_report(request):
    user=request.user
    try:
        is_superuser = User.objects.get(id=user.id).is_superuser
        if is_superuser == True:
            
            try:
                shape = request.GET['shape']
            except :
                shape = "round"
            main_tables = MainTables.objects.filter(shape__iexact=shape)
            data = DataManager.objects.filter(parent_table__in = main_tables)
            
            text = "Manak rerport is based on all major labs and its production of both HPHT & CVD(monthly/annually). No liability is assumed as to accuracy of this information"
            try:
                text = UIManager.objects.get(UI_position=4).text_description
            except Exception as e:
                print(e)
            return render(request,'admin_report.html',{"data":data,'type':shape,"text":text})
        else:
            return redirect('index')
    except Exception as e:
        print(e)
        return redirect('index')
    

@csrf_exempt
def download_pdf(request):
    pass


@csrf_exempt
def admin_generate_pdf(request):
    if request.method == "POST":
        try:
            shape = request.POST["shape"]
        except Exception as e:
            print(e)
            shape = "round"
        if shape == "":
            shape = "round"
        print(shape)
        main_tables = MainTables.objects.filter(shape__iexact=shape)
        data = DataManager.objects.filter(parent_table__in = main_tables)
        excel_creation(data,shape)
        pdfcon(shape)
        return JsonResponse({'success': True})

        
    

def update_price(request):
    if request.method=="POST":
        per_change = request.POST["per_change"]
        change = request.POST["change"]
        shape = request.POST["shape"]
        table_position_update = request.POST["table_position_update"]
        print(table_position_update)
       
        main_tables = MainTables.objects.filter(shape__iexact=shape)
       
        if change=="increase":
            if table_position_update == "All":
                datamanager = DataManager.objects.filter(parent_table__in = main_tables)
            else:
                datamanager = DataManager.objects.filter(parent_table__in = main_tables,postion=table_position_update)
            datamanager.update(
                increased = "D_IF,D_VV1,D_VV2,D_VS1,D_VS2,D_SI1,D_SI2,E_IF,E_VV1,E_VV2,E_VS1,E_VS2,E_SI1,E_SI2,F_IF,F_VV1,F_VV2,F_VS1,F_VS2,F_SI1,F_SI2,G_IF,G_VV1,G_VV2,G_VS1,G_VS2,G_SI1,G_SI2,H_IF,H_VV1,H_VV2,H_VS1,H_VS2,H_SI1,H_SI2,I_IF,I_VV1,I_VV2,I_VS1,I_VS2,I_SI1,I_SI2,J_IF,J_VV1,J_VV2,J_VS1,J_VS2,J_SI1,J_SI2",
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
                H_SI2=F('H_SI2')+F('H_SI2')*(int(per_change)/100),

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
            if table_position_update == "All":
                datamanager = DataManager.objects.filter(parent_table__in = main_tables)
            else:
                datamanager = DataManager.objects.filter(parent_table__in = main_tables,postion=table_position_update)
            
            datamanager.update(
                dropped = "D_IF,D_VV1,D_VV2,D_VS1,D_VS2,D_SI1,D_SI2,E_IF,E_VV1,E_VV2,E_VS1,E_VS2,E_SI1,E_SI2,F_IF,F_VV1,F_VV2,F_VS1,F_VS2,F_SI1,F_SI2,G_IF,G_VV1,G_VV2,G_VS1,G_VS2,G_SI1,G_SI2,H_IF,H_VV1,H_VV2,H_VS1,H_VS2,H_SI1,H_SI2,I_IF,I_VV1,I_VV2,I_VS1,I_VS2,I_SI1,I_SI2,J_IF,J_VV1,J_VV2,J_VS1,J_VS2,J_SI1,J_SI2",

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
                H_SI2=F('H_SI2')-F('H_SI2')*(int(per_change)/100),

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
        
        admin_generate_pdf(request)
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


    



def excel_creation(data,shape):
    file = 'media/pdf/'+ shape +".xlsx"
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()

    # Cell Merging
    # Formating
    title_format = workbook.add_format(
    {
        "bold": 1,
        "font":"Agency FB",
        "font_size":20,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",
        
    })
    subtitle_format = workbook.add_format(
       {
        "font":"Agency FB",
        "font_size":10,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",
    })

    price_box_drop = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "bold": 1,
        "border":1,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",

        })
    
    price_box_up = workbook.add_format(
       {
        "font":"Agency FB",
        "font_size":10,
        "bold": 1,
        "border":1,
        "color":"white",
        "align": "center",
        "valign": "vcenter",
        "fg_color": "#808080",
        })
    
    
    
    table_heading = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "color":"white",
        "align": "center",
        "valign": "vcenter",
        "fg_color": "#000000",

        })
    
    last_row_table_heading = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "color":"white",
        "align": "center",
        "valign": "vcenter",
        "fg_color": "#000000",
        'bottom': 5,
        })
    
    last_col_table_heading = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "color":"white",
        "align": "center",
        "valign": "vcenter",
        "fg_color": "#000000",
        'right': 5,
        })

    table_tile = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "bold": 1,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",

        })
    
    table_date = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",

        })

    table_descritption = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",
        'bottom' : 1
        })
    
    
    common_format = {
            "font":"Agency FB",
            "font_size":10,
            "align": "center",
            "valign": "vcenter",
            "fg_color": "white",
            
            }
    
    common = workbook.add_format(common_format)
    up_common = workbook.add_format(dict(common_format, fg_color='#808080',font_color="white"))
    down_common = workbook.add_format(dict(common_format, bold=True))

    row_common = workbook.add_format(dict(common_format, bottom=1))
    up_row_common = workbook.add_format(dict(common_format, bottom=1, fg_color='#808080',font_color ="white"))
    down_row_common = workbook.add_format(dict(common_format, bottom=1, bold=True))
    
    divider = workbook.add_format(dict(common_format, right=1))
    up_divider = workbook.add_format(dict(common_format, right=1, fg_color='#808080',font_color ="white"))
    down_divider = workbook.add_format(dict(common_format, right=1, bold=True))

    row_divider = workbook.add_format(dict(common_format, right=1, bottom=1))
    up_row_divider = workbook.add_format(dict(common_format, right=1, bottom=1, fg_color='#808080',font_color ="white"))
    down_row_divider = workbook.add_format(dict(common_format, right=1, bottom=1, bold=True))
    
    last_common = workbook.add_format(dict(common_format, bottom=1))  
    up_last_common = workbook.add_format(dict(common_format, bottom=1, fg_color='#808080',font_color ="white"))  
    down_last_common = workbook.add_format(dict(common_format, bottom=1, bold=True))  
    
    last_divider = workbook.add_format(dict(common_format, right=1, bottom=1))
    up_last_divider = workbook.add_format(dict(common_format, right=1, bottom=1, fg_color='#808080',font_color ="white"))
    down_last_divider = workbook.add_format(dict(common_format, right=1, bottom=1, bold=True))



       
    
    

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
    text = "Manak rerport is based on all major labs and its production of both HPHT & CVD(monthly/annually). No liability is assumed as to accuracy of this information"
    try:
        text = UIManager.objects.get(UI_position=4).text_description
    except Exception as e:
        print(e)
    worksheet.merge_range("B4:R4", text, subtitle_format)
    
    worksheet.set_row(4,11.25)
    worksheet.set_row(5,7.5)
    worksheet.set_row(6,7.5)
    worksheet.set_row(7,7.5)
    worksheet.set_row(8,4.5)

    worksheet.set_row(9,12)
    worksheet.merge_range("B10:G10", "Price change : Dark Cell - Increased / Bold - Dropped ", common)
    

    worksheet.merge_range("H10:I10", 'increased',price_box_up)
    worksheet.merge_range("K10:L10", 'dropped',price_box_drop)
   
    # Footer
    footer_font = workbook.add_format(
        {
        "font":"Agency FB",
        "font_size":10,
        "align": "center",
        "valign": "vcenter",
        "fg_color": "white",

        })
    worksheet.set_row(57,48)
    worksheet.merge_range("A58:I58", "For Price Update : ManakReport.com ", footer_font)

    

    # Table data 
    
    row_1 = 13
    row_2 = 13
    col = 'A'
    side = 0
    for x in data:
        if side == 0:
            # Table Title
            worksheet.merge_range('A'+str(row_1)+':B'+str(row_1), x.parent_table.carat_range,table_tile)
            worksheet.merge_range('D'+str(row_1)+':E'+str(row_1), x.parent_table.tabel_date.strftime("%m/%d/%y"),table_date)
            worksheet.write('H'+str(row_1), x.parent_table.shape,table_tile) 

            # Table heading
            worksheet.write('A'+str(row_1+1), 'MANAK',table_heading)
            worksheet.write('B'+str(row_1+1), 'D',table_heading)
            worksheet.write('C'+str(row_1+1), 'E',table_heading)
            worksheet.write('D'+str(row_1+1), 'F',table_heading)
            worksheet.write('E'+str(row_1+1), 'G',table_heading)
            worksheet.write('F'+str(row_1+1), 'H',table_heading)
            worksheet.write('G'+str(row_1+1), 'I',table_heading)
            worksheet.write('H'+str(row_1+1), 'J',last_col_table_heading)

            worksheet.write('A'+str(row_1+2), 'IF',table_heading)
            worksheet.write('A'+str(row_1+3), 'VV1',table_heading)
            worksheet.write('A'+str(row_1+4), 'VV2',table_heading)
            worksheet.write('A'+str(row_1+5), 'VS1',table_heading)
            worksheet.write('A'+str(row_1+6), 'VS2',table_heading)
            worksheet.write('A'+str(row_1+7), 'SI1',table_heading)
            worksheet.write('A'+str(row_1+8), 'SI2',last_row_table_heading)

            worksheet.merge_range('A'+str(row_1+9)+':D'+str(row_1+9), x.parent_table.text_description,table_descritption)
            worksheet.merge_range('E'+str(row_1+9)+':H'+str(row_1+9), "",table_descritption)
            
            # row_1 IF +str(row_1+2)

            worksheet.write('B'+str(row_1+2),x.D_IF,down_common) if "D_IF" in x.dropped  else (worksheet.write('B'+str(row_1+2),x.D_IF,up_common) if "D_IF" in x.increased else worksheet.write('B'+str(row_1+2),x.D_IF,common))
            worksheet.write('C'+str(row_1+2),x.E_IF,down_common) if "E_IF" in x.dropped  else (worksheet.write('C'+str(row_1+2),x.E_IF,up_common) if "E_IF" in x.increased else worksheet.write('C'+str(row_1+2),x.E_IF,common))
            worksheet.write('D'+str(row_1+2),x.F_IF,down_divider) if "F_IF" in x.dropped  else (worksheet.write('D'+str(row_1+2),x.F_IF,up_divider) if "F_IF" in x.increased else worksheet.write('D'+str(row_1+2),x.F_IF,divider))
            worksheet.write('E'+str(row_1+2),x.G_IF,down_common) if "G_IF" in x.dropped  else (worksheet.write('E'+str(row_1+2),x.G_IF,up_common) if "G_IF" in x.increased else worksheet.write('E'+str(row_1+2),x.G_IF,common))
            worksheet.write('F'+str(row_1+2),x.H_IF,down_divider) if "H_IF" in x.dropped  else (worksheet.write('F'+str(row_1+2),x.H_IF,up_divider) if "H_IF" in x.increased else worksheet.write('F'+str(row_1+2),x.H_IF,divider))
            worksheet.write('G'+str(row_1+2),x.I_IF,down_common) if "I_IF" in x.dropped  else (worksheet.write('G'+str(row_1+2),x.I_IF,up_common) if "I_IF" in x.increased else worksheet.write('G'+str(row_1+2),x.I_IF,common))
            worksheet.write('H'+str(row_1+2),x.J_IF,down_divider) if "J_IF" in x.dropped  else (worksheet.write('H'+str(row_1+2),x.J_IF,up_divider) if "J_IF" in x.increased else worksheet.write('H'+str(row_1+2),x.J_IF,divider))

            # row_1 VV1 +str(row_1+3)
            worksheet.write('B'+str(row_1+3),x.D_VV1,down_common) if "D_VV1" in x.dropped  else (worksheet.write('B'+str(row_1+3),x.D_VV1,up_common) if "D_VV1" in x.increased else worksheet.write('B'+str(row_1+3),x.D_VV1,common))
            worksheet.write('C'+str(row_1+3),x.E_VV1,down_common) if "E_VV1" in x.dropped  else (worksheet.write('C'+str(row_1+3),x.E_VV1,up_common) if "E_VV1" in x.increased else worksheet.write('C'+str(row_1+3),x.E_VV1,common))
            worksheet.write('D'+str(row_1+3),x.F_VV1,down_divider) if "F_VV1" in x.dropped  else (worksheet.write('D'+str(row_1+3),x.F_VV1,up_divider) if "F_VV1" in x.increased else worksheet.write('D'+str(row_1+3),x.F_VV1,divider))
            worksheet.write('E'+str(row_1+3),x.F_VV1,down_common) if "G_VV1" in x.dropped  else (worksheet.write('E'+str(row_1+3),x.G_VV1,up_common) if "G_VV1" in x.increased else worksheet.write('E'+str(row_1+3),x.G_VV1,common))
            worksheet.write('F'+str(row_1+3),x.H_VV1,down_divider) if "H_VV1" in x.dropped  else (worksheet.write('F'+str(row_1+3),x.H_VV1,up_divider) if "H_VV1" in x.increased else worksheet.write('F'+str(row_1+3),x.H_VV1,divider))
            worksheet.write('G'+str(row_1+3),x.I_VV1,down_common) if "I_VV1" in x.dropped  else (worksheet.write('G'+str(row_1+3),x.I_VV1,up_common) if "I_VV1" in x.increased else worksheet.write('G'+str(row_1+3),x.I_VV1,common))
            worksheet.write('H'+str(row_1+3),x.J_VV1,down_divider) if "J_VV1" in x.dropped  else (worksheet.write('H'+str(row_1+3),x.J_VV1,up_divider) if "J_VV1" in x.increased else worksheet.write('H'+str(row_1+3),x.J_VV1,divider))

            

            # row_1 VV2 +str(row_1+4)
            worksheet.write('B'+str(row_1+4),x.D_VV2,down_row_common) if "D_VV2" in x.dropped  else (worksheet.write('B'+str(row_1+4),x.D_VV2,up_row_common) if "D_VV2" in x.increased else worksheet.write('B'+str(row_1+4),x.D_VV2,row_common))
            worksheet.write('C'+str(row_1+4),x.E_VV2,down_row_common) if "E_VV2" in x.dropped  else (worksheet.write('C'+str(row_1+4),x.E_VV2,up_row_common) if "E_VV2" in x.increased else worksheet.write('C'+str(row_1+4),x.E_VV2,row_common))
            worksheet.write('D'+str(row_1+4),x.F_VV2,down_row_divider) if "F_VV2" in x.dropped  else (worksheet.write('D'+str(row_1+4),x.F_VV2,up_row_divider) if "F_VV2" in x.increased else worksheet.write('D'+str(row_1+4),x.F_VV2,row_divider))
            worksheet.write('E'+str(row_1+4),x.F_VV2,down_row_common) if "G_VV2" in x.dropped  else (worksheet.write('E'+str(row_1+4),x.G_VV2,up_row_common) if "G_VV2" in x.increased else worksheet.write('E'+str(row_1+4),x.G_VV2,row_common))
            worksheet.write('F'+str(row_1+4),x.H_VV2,down_row_divider) if "H_VV2" in x.dropped  else (worksheet.write('F'+str(row_1+4),x.H_VV2,up_row_divider) if "H_VV2" in x.increased else worksheet.write('F'+str(row_1+4),x.H_VV2,row_divider))
            worksheet.write('G'+str(row_1+4),x.I_VV2,down_row_common) if "I_VV2" in x.dropped  else (worksheet.write('G'+str(row_1+4),x.I_VV2,up_row_common) if "I_VV2" in x.increased else worksheet.write('G'+str(row_1+4),x.I_VV2,row_common))
            worksheet.write('H'+str(row_1+4),x.J_VV2,down_row_divider) if "J_VV2" in x.dropped  else (worksheet.write('H'+str(row_1+4),x.J_VV2,up_row_divider) if "J_VV2" in x.increased else worksheet.write('H'+str(row_1+4),x.J_VV2,row_divider))

            # row_1 VS1 +str(row_1+5)
            worksheet.write('B'+str(row_1+5),x.D_VS1,down_common) if "D_VS1" in x.dropped  else (worksheet.write('B'+str(row_1+5),x.D_VS1,up_common) if "D_VS1" in x.increased else worksheet.write('B'+str(row_1+5),x.D_VS1,common))
            worksheet.write('C'+str(row_1+5),x.E_VS1,down_common) if "E_VS1" in x.dropped  else (worksheet.write('C'+str(row_1+5),x.E_VS1,up_common) if "E_VS1" in x.increased else worksheet.write('C'+str(row_1+5),x.E_VS1,common))
            worksheet.write('D'+str(row_1+5),x.F_VS1,down_divider) if "F_VS1" in x.dropped  else (worksheet.write('D'+str(row_1+5),x.F_VS1,up_divider) if "F_VS1" in x.increased else worksheet.write('D'+str(row_1+5),x.F_VS1,divider))
            worksheet.write('E'+str(row_1+5),x.F_VS1,down_common) if "G_VS1" in x.dropped  else (worksheet.write('E'+str(row_1+5),x.G_VS1,up_common) if "G_VS1" in x.increased else worksheet.write('E'+str(row_1+5),x.G_VS1,common))
            worksheet.write('F'+str(row_1+5),x.H_VS1,down_divider) if "H_VS1" in x.dropped  else (worksheet.write('F'+str(row_1+5),x.H_VS1,up_divider) if "H_VS1" in x.increased else worksheet.write('F'+str(row_1+5),x.H_VS1,divider))
            worksheet.write('G'+str(row_1+5),x.I_VS1,down_common) if "I_VS1" in x.dropped  else (worksheet.write('G'+str(row_1+5),x.I_VS1,up_common) if "I_VS1" in x.increased else worksheet.write('G'+str(row_1+5),x.I_VS1,common))
            worksheet.write('H'+str(row_1+5),x.J_VS1,down_divider) if "J_VS1" in x.dropped  else (worksheet.write('H'+str(row_1+5),x.J_VS1,up_divider) if "J_VS1" in x.increased else worksheet.write('H'+str(row_1+5),x.J_VS1,divider))

        

            # row_1 VS2 +str(row_1+6)
            worksheet.write('B'+str(row_1+6),x.D_VS2,down_row_common) if "D_VS2" in x.dropped  else (worksheet.write('B'+str(row_1+6),x.D_VS2,up_row_common) if "D_VS2" in x.increased else worksheet.write('B'+str(row_1+6),x.D_VS2,row_common))
            worksheet.write('C'+str(row_1+6),x.E_VS2,down_row_common) if "E_VS2" in x.dropped  else (worksheet.write('C'+str(row_1+6),x.E_VS2,up_row_common) if "E_VS2" in x.increased else worksheet.write('C'+str(row_1+6),x.E_VS2,row_common))
            worksheet.write('D'+str(row_1+6),x.F_VS2,down_row_divider) if "F_VS2" in x.dropped  else (worksheet.write('D'+str(row_1+6),x.F_VS2,up_row_divider) if "F_VS2" in x.increased else worksheet.write('D'+str(row_1+6),x.F_VS2,row_divider))
            worksheet.write('E'+str(row_1+6),x.F_VS2,down_row_common) if "G_VS2" in x.dropped  else (worksheet.write('E'+str(row_1+6),x.G_VS2,up_row_common) if "G_VS2" in x.increased else worksheet.write('E'+str(row_1+6),x.G_VS2,row_common))
            worksheet.write('F'+str(row_1+6),x.H_VS2,down_row_divider) if "H_VS2" in x.dropped  else (worksheet.write('F'+str(row_1+6),x.H_VS2,up_row_divider) if "H_VS2" in x.increased else worksheet.write('F'+str(row_1+6),x.H_VS2,row_divider))
            worksheet.write('G'+str(row_1+6),x.I_VS2,down_row_common) if "I_VS2" in x.dropped  else (worksheet.write('G'+str(row_1+6),x.I_VS2,up_row_common) if "I_VS2" in x.increased else worksheet.write('G'+str(row_1+6),x.I_VS2,row_common))
            worksheet.write('H'+str(row_1+6),x.J_VS2,down_row_divider) if "J_VS2" in x.dropped  else (worksheet.write('H'+str(row_1+6),x.J_VS2,up_row_divider) if "J_VS2" in x.increased else worksheet.write('H'+str(row_1+6),x.J_VS2,row_divider))



            # row_1 SI1 +str(row_1+7)
            worksheet.write('B'+str(row_1+7),x.D_SI1,down_common) if "D_SI1" in x.dropped  else (worksheet.write('B'+str(row_1+7),x.D_SI1,up_common) if "D_SI1" in x.increased else worksheet.write('B'+str(row_1+7),x.D_SI1,common))
            worksheet.write('C'+str(row_1+7),x.E_SI1,down_common) if "E_SI1" in x.dropped  else (worksheet.write('C'+str(row_1+7),x.E_SI1,up_common) if "E_SI1" in x.increased else worksheet.write('C'+str(row_1+7),x.E_SI1,common))
            worksheet.write('D'+str(row_1+7),x.F_SI1,down_divider) if "F_SI1" in x.dropped  else (worksheet.write('D'+str(row_1+7),x.F_SI1,up_divider) if "F_SI1" in x.increased else worksheet.write('D'+str(row_1+7),x.F_SI1,divider))
            worksheet.write('E'+str(row_1+7),x.F_SI1,down_common) if "G_SI1" in x.dropped  else (worksheet.write('E'+str(row_1+7),x.G_SI1,up_common) if "G_SI1" in x.increased else worksheet.write('E'+str(row_1+7),x.G_SI1,common))
            worksheet.write('F'+str(row_1+7),x.H_SI1,down_divider) if "H_SI1" in x.dropped  else (worksheet.write('F'+str(row_1+7),x.H_SI1,up_divider) if "H_SI1" in x.increased else worksheet.write('F'+str(row_1+7),x.H_SI1,divider))
            worksheet.write('G'+str(row_1+7),x.I_SI1,down_common) if "I_SI1" in x.dropped  else (worksheet.write('G'+str(row_1+7),x.I_SI1,up_common) if "I_SI1" in x.increased else worksheet.write('G'+str(row_1+7),x.I_SI1,common))
            worksheet.write('H'+str(row_1+7),x.J_SI1,down_divider) if "J_SI1" in x.dropped  else (worksheet.write('H'+str(row_1+7),x.J_SI1,up_divider) if "J_SI1" in x.increased else worksheet.write('H'+str(row_1+7),x.J_SI1,divider))


            # row_1 SI2 +str(row_1+8)
            worksheet.write('B'+str(row_1+8),x.D_SI2,down_last_common) if "D_SI2" in x.dropped  else (worksheet.write('B'+str(row_1+8),x.D_SI2,up_last_common) if "D_SI2" in x.increased else worksheet.write('B'+str(row_1+8),x.D_SI2,last_common))
            worksheet.write('C'+str(row_1+8),x.E_SI2,down_last_common) if "E_SI2" in x.dropped  else (worksheet.write('C'+str(row_1+8),x.E_SI2,up_last_common) if "E_SI2" in x.increased else worksheet.write('C'+str(row_1+8),x.E_SI2,last_common))
            worksheet.write('D'+str(row_1+8),x.F_SI2,down_last_divider) if "F_SI2" in x.dropped  else (worksheet.write('D'+str(row_1+8),x.F_SI2,up_last_divider) if "F_SI2" in x.increased else worksheet.write('D'+str(row_1+8),x.F_SI2,last_divider))
            worksheet.write('E'+str(row_1+8),x.F_SI2,down_last_common) if "G_SI2" in x.dropped  else (worksheet.write('E'+str(row_1+8),x.G_SI2,up_last_common) if "G_SI2" in x.increased else worksheet.write('E'+str(row_1+8),x.G_SI2,last_common))
            worksheet.write('F'+str(row_1+8),x.H_SI2,down_last_divider) if "H_SI2" in x.dropped  else (worksheet.write('F'+str(row_1+8),x.H_SI2,up_last_divider) if "H_SI2" in x.increased else worksheet.write('F'+str(row_1+8),x.H_SI2,last_divider))
            worksheet.write('G'+str(row_1+8),x.I_SI2,down_last_common) if "I_SI2" in x.dropped  else (worksheet.write('G'+str(row_1+8),x.I_SI2,up_last_common) if "I_SI2" in x.increased else worksheet.write('G'+str(row_1+8),x.I_SI2,last_common))
            worksheet.write('H'+str(row_1+8),x.J_SI2,down_last_divider) if "J_SI2" in x.dropped  else (worksheet.write('H'+str(row_1+8),x.J_SI2,up_last_divider) if "J_SI2" in x.increased else worksheet.write('H'+str(row_1+8),x.J_SI2,last_divider))


            row_1 += 11
            side = 1
        else:

             # Table Title
            worksheet.merge_range('K'+str(row_2)+':L'+str(row_2), x.parent_table.carat_range,table_tile)
            worksheet.merge_range('N'+str(row_2)+':O'+str(row_2), x.parent_table.tabel_date.strftime("%m/%d/%y"),table_date)
            worksheet.write('R'+str(row_2), x.parent_table.shape,table_tile) 

            # Table heading
            worksheet.write('K'+str(row_2+1), 'MANAK',table_heading)
            worksheet.write('L'+str(row_2+1), 'N',table_heading)
            worksheet.write('M'+str(row_2+1), 'E',table_heading)
            worksheet.write('N'+str(row_2+1), 'F',table_heading)
            worksheet.write('O'+str(row_2+1), 'G',table_heading)
            worksheet.write('P'+str(row_2+1), 'H',table_heading)
            worksheet.write('Q'+str(row_2+1), 'I',table_heading)
            worksheet.write('R'+str(row_2+1), 'J',last_col_table_heading)

            worksheet.write('K'+str(row_2+2), 'IF',table_heading)
            worksheet.write('K'+str(row_2+3), 'VV1',table_heading)
            worksheet.write('K'+str(row_2+4), 'VV2',table_heading)
            worksheet.write('K'+str(row_2+5), 'VS1',table_heading)
            worksheet.write('K'+str(row_2+6), 'VS2',table_heading)
            worksheet.write('K'+str(row_2+7), 'SI1',table_heading)
            worksheet.write('K'+str(row_2+8), 'SI2',last_row_table_heading)

            worksheet.merge_range('K'+str(row_2+9)+':N'+str(row_2+9), x.parent_table.text_description,table_descritption)
            worksheet.merge_range('O'+str(row_2+9)+':R'+str(row_2+9),"",table_descritption)
            
            # row_2 IF +str(row_2+2)
            worksheet.write('L'+str(row_2+2),x.D_IF,down_common) if "D_IF" in x.dropped  else (worksheet.write('L'+str(row_2+2),x.D_IF,up_common) if "D_IF" in x.increased else worksheet.write('L'+str(row_2+2),x.D_IF,common))
            worksheet.write('M'+str(row_2+2),x.E_IF,down_common) if "E_IF" in x.dropped  else (worksheet.write('M'+str(row_2+2),x.E_IF,up_common) if "E_IF" in x.increased else worksheet.write('M'+str(row_2+2),x.E_IF,common))
            worksheet.write('N'+str(row_2+2),x.F_IF,down_divider) if "F_IF" in x.dropped  else (worksheet.write('N'+str(row_2+2),x.F_IF,up_divider) if "F_IF" in x.increased else worksheet.write('N'+str(row_2+2),x.F_IF,divider))
            worksheet.write('O'+str(row_2+2),x.G_IF,down_common) if "G_IF" in x.dropped  else (worksheet.write('O'+str(row_2+2),x.G_IF,up_common) if "G_IF" in x.increased else worksheet.write('O'+str(row_2+2),x.G_IF,common))
            worksheet.write('P'+str(row_2+2),x.H_IF,down_divider) if "H_IF" in x.dropped  else (worksheet.write('P'+str(row_2+2),x.H_IF,up_divider) if "H_IF" in x.increased else worksheet.write('P'+str(row_2+2),x.H_IF,divider))
            worksheet.write('Q'+str(row_2+2),x.I_IF,down_common) if "I_IF" in x.dropped  else (worksheet.write('Q'+str(row_2+2),x.I_IF,up_common) if "I_IF" in x.increased else worksheet.write('Q'+str(row_2+2),x.I_IF,common))
            worksheet.write('R'+str(row_2+2),x.J_IF,down_divider) if "J_IF" in x.dropped  else (worksheet.write('R'+str(row_2+2),x.J_IF,up_divider) if "J_IF" in x.increased else worksheet.write('R'+str(row_2+2),x.J_IF,divider))

            # row_2 VV1 +str(row_2+3)
            worksheet.write('L'+str(row_2+3),x.D_VV1,down_common) if "D_VV1" in x.dropped  else (worksheet.write('L'+str(row_2+3),x.D_VV1,up_common) if "D_VV1" in x.increased else worksheet.write('L'+str(row_2+3),x.D_VV1,common))
            worksheet.write('M'+str(row_2+3),x.E_VV1,down_common) if "E_VV1" in x.dropped  else (worksheet.write('M'+str(row_2+3),x.E_VV1,up_common) if "E_VV1" in x.increased else worksheet.write('M'+str(row_2+3),x.E_VV1,common))
            worksheet.write('N'+str(row_2+3),x.F_VV1,down_divider) if "F_VV1" in x.dropped  else (worksheet.write('N'+str(row_2+3),x.F_VV1,up_divider) if "F_VV1" in x.increased else worksheet.write('N'+str(row_2+3),x.F_VV1,divider))
            worksheet.write('O'+str(row_2+3),x.G_VV1,down_common) if "G_VV1" in x.dropped  else (worksheet.write('O'+str(row_2+3),x.G_VV1,up_common) if "G_VV1" in x.increased else worksheet.write('O'+str(row_2+3),x.G_VV1,common))
            worksheet.write('P'+str(row_2+3),x.H_VV1,down_divider) if "H_VV1" in x.dropped  else (worksheet.write('P'+str(row_2+3),x.H_VV1,up_divider) if "H_VV1" in x.increased else worksheet.write('P'+str(row_2+3),x.H_VV1,divider))
            worksheet.write('Q'+str(row_2+3),x.I_VV1,down_common) if "I_VV1" in x.dropped  else (worksheet.write('Q'+str(row_2+3),x.I_VV1,up_common) if "I_VV1" in x.increased else worksheet.write('Q'+str(row_2+3),x.I_VV1,common))
            worksheet.write('R'+str(row_2+3),x.J_VV1,down_divider) if "J_VV1" in x.dropped  else (worksheet.write('R'+str(row_2+3),x.J_VV1,up_divider) if "J_VV1" in x.increased else worksheet.write('R'+str(row_2+3),x.J_VV1,divider))


            # row_2 VV2 +str(row_2+4)
            worksheet.write('L'+str(row_2+4),x.D_VV2,down_row_common) if "D_VV2" in x.dropped  else (worksheet.write('L'+str(row_2+4),x.D_VV2,up_row_common) if "D_VV2" in x.increased else worksheet.write('L'+str(row_2+4),x.D_VV2,row_common))
            worksheet.write('M'+str(row_2+4),x.E_VV2,down_row_common) if "E_VV2" in x.dropped  else (worksheet.write('M'+str(row_2+4),x.E_VV2,up_row_common) if "E_VV2" in x.increased else worksheet.write('M'+str(row_2+4),x.E_VV2,row_common))
            worksheet.write('N'+str(row_2+4),x.F_VV2,down_row_divider) if "F_VV2" in x.dropped  else (worksheet.write('N'+str(row_2+4),x.F_VV2,up_row_divider) if "F_VV2" in x.increased else worksheet.write('N'+str(row_2+4),x.F_VV2,row_divider))
            worksheet.write('O'+str(row_2+4),x.G_VV2,down_row_common) if "G_VV2" in x.dropped  else (worksheet.write('O'+str(row_2+4),x.G_VV2,up_row_common) if "G_VV2" in x.increased else worksheet.write('O'+str(row_2+4),x.G_VV2,row_common))
            worksheet.write('P'+str(row_2+4),x.H_VV2,down_row_divider) if "H_VV2" in x.dropped  else (worksheet.write('P'+str(row_2+4),x.H_VV2,up_row_divider) if "H_VV2" in x.increased else worksheet.write('P'+str(row_2+4),x.H_VV2,row_divider))
            worksheet.write('Q'+str(row_2+4),x.I_VV2,down_row_common) if "I_VV2" in x.dropped  else (worksheet.write('Q'+str(row_2+4),x.I_VV2,up_row_common) if "I_VV2" in x.increased else worksheet.write('Q'+str(row_2+4),x.I_VV2,row_common))
            worksheet.write('R'+str(row_2+4),x.J_VV2,down_row_divider) if "J_VV2" in x.dropped  else (worksheet.write('R'+str(row_2+4),x.J_VV2,up_row_divider) if "J_VV2" in x.increased else worksheet.write('R'+str(row_2+4),x.J_VV2,row_divider))


            # row_2 VS1 +str(row_2+5)
            worksheet.write('L'+str(row_2+5),x.D_VS1,down_common) if "D_VS1" in x.dropped  else (worksheet.write('L'+str(row_2+5),x.D_VS1,up_common) if "D_VS1" in x.increased else worksheet.write('L'+str(row_2+5),x.D_VS1,common))
            worksheet.write('M'+str(row_2+5),x.E_VS1,down_common) if "E_VS1" in x.dropped  else (worksheet.write('M'+str(row_2+5),x.E_VS1,up_common) if "E_VS1" in x.increased else worksheet.write('M'+str(row_2+5),x.E_VS1,common))
            worksheet.write('N'+str(row_2+5),x.F_VS1,down_divider) if "F_VS1" in x.dropped  else (worksheet.write('N'+str(row_2+5),x.F_VS1,up_divider) if "F_VS1" in x.increased else worksheet.write('N'+str(row_2+5),x.F_VS1,divider))
            worksheet.write('O'+str(row_2+5),x.G_VS1,down_common) if "G_VS1" in x.dropped  else (worksheet.write('O'+str(row_2+5),x.G_VS1,up_common) if "G_VS1" in x.increased else worksheet.write('O'+str(row_2+5),x.G_VS1,common))
            worksheet.write('P'+str(row_2+5),x.H_VS1,down_divider) if "H_VS1" in x.dropped  else (worksheet.write('P'+str(row_2+5),x.H_VS1,up_divider) if "H_VS1" in x.increased else worksheet.write('P'+str(row_2+5),x.H_VS1,divider))
            worksheet.write('Q'+str(row_2+5),x.I_VS1,down_common) if "I_VS1" in x.dropped  else (worksheet.write('Q'+str(row_2+5),x.I_VS1,up_common) if "I_VS1" in x.increased else worksheet.write('Q'+str(row_2+5),x.I_VS1,common))
            worksheet.write('R'+str(row_2+5),x.J_VS1,down_divider) if "J_VS1" in x.dropped  else (worksheet.write('R'+str(row_2+5),x.J_VS1,up_divider) if "J_VS1" in x.increased else worksheet.write('R'+str(row_2+5),x.J_VS1,divider))


            # row_2 VS2 +str(row_2+6)
            worksheet.write('L'+str(row_2+6),x.D_VS2,down_row_common) if "D_VS2" in x.dropped  else (worksheet.write('L'+str(row_2+6),x.D_VS2,up_row_common) if "D_VS2" in x.increased else worksheet.write('L'+str(row_2+6),x.D_VS2,row_common))
            worksheet.write('M'+str(row_2+6),x.E_VS2,down_row_common) if "E_VS2" in x.dropped  else (worksheet.write('M'+str(row_2+6),x.E_VS2,up_row_common) if "E_VS2" in x.increased else worksheet.write('M'+str(row_2+6),x.E_VS2,row_common))
            worksheet.write('N'+str(row_2+6),x.F_VS2,down_row_divider) if "F_VS2" in x.dropped  else (worksheet.write('N'+str(row_2+6),x.F_VS2,up_row_divider) if "F_VS2" in x.increased else worksheet.write('N'+str(row_2+6),x.F_VS2,row_divider))
            worksheet.write('O'+str(row_2+6),x.G_VS2,down_row_common) if "G_VS2" in x.dropped  else (worksheet.write('O'+str(row_2+6),x.G_VS2,up_row_common) if "G_VS2" in x.increased else worksheet.write('O'+str(row_2+6),x.G_VS2,row_common))
            worksheet.write('P'+str(row_2+6),x.H_VS2,down_row_divider) if "H_VS2" in x.dropped  else (worksheet.write('P'+str(row_2+6),x.H_VS2,up_row_divider) if "H_VS2" in x.increased else worksheet.write('P'+str(row_2+6),x.H_VS2,row_divider))
            worksheet.write('Q'+str(row_2+6),x.I_VS2,down_row_common) if "I_VS2" in x.dropped  else (worksheet.write('Q'+str(row_2+6),x.I_VS2,up_row_common) if "I_VS2" in x.increased else worksheet.write('Q'+str(row_2+6),x.I_VS2,row_common))
            worksheet.write('R'+str(row_2+6),x.J_VS2,down_row_divider) if "J_VS2" in x.dropped  else (worksheet.write('R'+str(row_2+6),x.J_VS2,up_row_divider) if "J_VS2" in x.increased else worksheet.write('R'+str(row_2+6),x.J_VS2,row_divider))


            # row_2 SI1 +str(row_2+7)
            worksheet.write('L'+str(row_2+7),x.D_SI1,down_common) if "D_SI1" in x.dropped  else (worksheet.write('L'+str(row_2+7),x.D_SI1,up_common) if "D_SI1" in x.increased else worksheet.write('L'+str(row_2+7),x.D_SI1,common))
            worksheet.write('M'+str(row_2+7),x.E_SI1,down_common) if "E_SI1" in x.dropped  else (worksheet.write('M'+str(row_2+7),x.E_SI1,up_common) if "E_SI1" in x.increased else worksheet.write('M'+str(row_2+7),x.E_SI1,common))
            worksheet.write('N'+str(row_2+7),x.F_SI1,down_divider) if "F_SI1" in x.dropped  else (worksheet.write('N'+str(row_2+7),x.F_SI1,up_divider) if "F_SI1" in x.increased else worksheet.write('N'+str(row_2+7),x.F_SI1,divider))
            worksheet.write('O'+str(row_2+7),x.G_SI1,down_common) if "G_SI1" in x.dropped  else (worksheet.write('O'+str(row_2+7),x.G_SI1,up_common) if "G_SI1" in x.increased else worksheet.write('O'+str(row_2+7),x.G_SI1,common))
            worksheet.write('P'+str(row_2+7),x.H_SI1,down_divider) if "H_SI1" in x.dropped  else (worksheet.write('P'+str(row_2+7),x.H_SI1,up_divider) if "H_SI1" in x.increased else worksheet.write('P'+str(row_2+7),x.H_SI1,divider))
            worksheet.write('Q'+str(row_2+7),x.I_SI1,down_common) if "I_SI1" in x.dropped  else (worksheet.write('Q'+str(row_2+7),x.I_SI1,up_common) if "I_SI1" in x.increased else worksheet.write('Q'+str(row_2+7),x.I_SI1,common))
            worksheet.write('R'+str(row_2+7),x.J_SI1,down_divider) if "J_SI1" in x.dropped  else (worksheet.write('R'+str(row_2+7),x.J_SI1,up_divider) if "J_SI1" in x.increased else worksheet.write('R'+str(row_2+7),x.J_SI1,divider))



            # row_2 SI2 +str(row_2+8)
            worksheet.write('L'+str(row_2+8),x.D_SI2,down_last_common) if "D_SI2" in x.dropped  else (worksheet.write('L'+str(row_2+8),x.D_SI2,up_last_common) if "D_SI2" in x.increased else worksheet.write('L'+str(row_2+8),x.D_SI2,last_common))
            worksheet.write('M'+str(row_2+8),x.E_SI2,down_last_common) if "E_SI2" in x.dropped  else (worksheet.write('M'+str(row_2+8),x.E_SI2,up_last_common) if "E_SI2" in x.increased else worksheet.write('M'+str(row_2+8),x.E_SI2,last_common))
            worksheet.write('N'+str(row_2+8),x.F_SI2,down_last_divider) if "F_SI2" in x.dropped  else (worksheet.write('N'+str(row_2+8),x.F_SI2,up_last_divider) if "F_SI2" in x.increased else worksheet.write('N'+str(row_2+8),x.F_SI2,last_divider))
            worksheet.write('O'+str(row_2+8),x.G_SI2,down_last_common) if "G_SI2" in x.dropped  else (worksheet.write('O'+str(row_2+8),x.G_SI2,up_last_common) if "G_SI2" in x.increased else worksheet.write('O'+str(row_2+8),x.G_SI2,last_common))
            worksheet.write('P'+str(row_2+8),x.H_SI2,down_last_divider) if "H_SI2" in x.dropped  else (worksheet.write('P'+str(row_2+8),x.H_SI2,up_last_divider) if "H_SI2" in x.increased else worksheet.write('P'+str(row_2+8),x.H_SI2,last_divider))
            worksheet.write('Q'+str(row_2+8),x.I_SI2,down_last_common) if "I_SI2" in x.dropped  else (worksheet.write('Q'+str(row_2+8),x.I_SI2,up_last_common) if "I_SI2" in x.increased else worksheet.write('Q'+str(row_2+8),x.I_SI2,last_common))
            worksheet.write('R'+str(row_2+8),x.J_SI2,down_last_divider) if "J_SI2" in x.dropped  else (worksheet.write('R'+str(row_2+8),x.J_SI2,up_last_divider) if "J_SI2" in x.increased else worksheet.write('R'+str(row_2+8),x.J_SI2,last_divider))

            row_2 += 11
            side = 0



    workbook.close()
    
    

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




