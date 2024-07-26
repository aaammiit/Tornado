from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import *
from datetime import datetime
import json
from Krima_project import settings
import smtplib
import random
import math
import os
import pandas as pd
from django.urls import reverse
from django.conf import settings
import openpyxl

# Create your views here.


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'amistreetecom0101@gmail.com'
SMTP_PASSWORD = 'xmxj ztoo dfvw bxtm'
sender_email = 'amistreetecom0101@gmail.com'

def Page(request):
    if request.method=='POST':
        u=request.POST.get('un')
        p=request.POST.get('p')
        user=authenticate(User,username=u,password=p)  
        try: 
            if user.is_staff:
                request.session['uid']=user.id
                login(request,user)
                err='no' 
                return redirect('/home')                
        except:
            err='yes'                                
    return render(request,'index.html',locals())
    

def home(request):
    file_data=My_Upload_file.objects.all()
    pm=Pm_user.objects.all()
    data={'data':file_data,'pm':pm}
    try:
        list_date=[]
        date_obj=[]
        first_index=0
        last_index=-1
        if request.method=='POST':
            u=My_Upload_file()
            fsh=request.FILES.get('file')
            u.file=fsh
            u.save()
        with open(f'{settings.BASE_DIR}//{fsh}','r') as f:
            f1=json.load(f)
        u.count=len(f1)
        for i in f1:
            if i['Date'] != 'None' or i['Date'] != 'null':
               list_date.append((i['Date']))
        for i in list_date:
            date_str =i
            datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
            date_object = datetime_object.date()
            date_obj.append(date_object)
        sorted_date=sorted(date_obj)
        u.from_date=sorted_date[0]
        u.to_date=sorted_date[-1]
        u.save()
        return redirect('/home')
    except:
        ...  
    return render(request,'home.html',data)

def Delete(request,id):
    u=My_Upload_file.objects.filter(id=id)   
    u.delete()
    return redirect('/home') 

def view_file(request,id):
    list_date=[]
    date_obj=[]
    from_date=''
    to_date=''
    try:    
        file_obj=My_Upload_file.objects.get(id=id)
        file_obj1=My_Upload_file.objects.filter(id=id)
        for i in file_obj1:
            file=i.file
        with open(f'{settings.BASE_DIR}//{file}','r') as f:
            f1=json.load(f)
        for i in f1:
            if i['Date'] != 'None' or i['Date'] != 'null':
               list_date.append((i['Date']))
        for i in list_date:
            date_str =i
            datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
            date_object = datetime_object.date()
            date_obj.append(date_object)
        sorted_date=sorted(date_obj)
        from_date=sorted_date[0]
        to_date=sorted_date[-1] 
        data={'data':f1,'f':from_date,'t':to_date}
          
    except:
        return render(request,'admin_view_file.html',)
    return render(request,'admin_view_file.html',data)

def Make_pm(request):
    err=''
    if request.method=='POST':
        f_n=request.POST.get('f_n')
        l_n=request.POST.get('l_n')  
        email=request.POST.get('email')
        p=request.POST.get('p')
        try:
            user=User.objects.create_user(first_name=f_n,last_name=l_n,email=email,username=email,password=p)
            Pm_user.objects.create(user=user)
            err='no'    
            return redirect('/home')
        except:
            err='yes'
    return render(request,'make_pm.html') 

def Pm_login(request):
    if request.method == 'POST':
        u = request.POST.get('email')
        p = request.POST.get('p')
        user = authenticate(User, username=u, password=p)
        if user is not None:
            request.session['uid'] = user.id
            receiver_email = u
            otp_length = 6
            otp = math.floor(random.random() * 10**(otp_length-1) + 10**(otp_length-1))
            # Send OTP via email
            subject = "OTP Verification"
            body = f"Your OTP is: {otp}"
            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{body}")
                server.quit()
                print("OTP sent successfully")    
                # Store OTP in session
                request.session['otp'] = otp   
                # Redirect to OTP verification page
                return redirect('/verify_otp1')
            except :
                err = 'yes'
                print('err')
                return render(request, 'pm_login.html', locals())
        else:
            err = 'yes'
            return render(request, 'pm_login.html', locals())
    return render(request, 'pm_login.html', locals())

def verify_otp1(request):    
    us=request.session.get('uid')
    user=User.objects.get(id=us)
    # print(user)      
    if request.method == 'POST':
        otp_user = request.POST.get('otp')
        otp_session = request.session.get('otp')
        if otp_user == str(otp_session):
            msg = 'Successfully Verified'
            login(request, user)
            err = 'no'
            return redirect('/pm_home')
        else:
            msg = 'Invalid OTP'
            err = 'yes'
            return render(request, 'verify_otp.html', locals())
    return render(request, 'verify_otp.html', locals())

def Push_PM_file(request,id):
    u=My_Upload_file.objects.get(id=id) 
    pd=Push_to_pm_file()
    pd.my_file=u 
    # pd.save()
    u.status=True
    u.save()
    pd.save()

    return redirect('/home')

def Pm_home(request):
    p=Push_to_pm_file.objects.all()
    data={'data':p}
    return render(request,'pm_home.html',data)

def Pm_view_file(request,id):
    list_date=[]
    date_obj=[]
    from_date=''
    to_date=''
    try:    
        file_obj=Push_to_pm_file.objects.get(id=id)
        file_obj1=Push_to_pm_file.objects.filter(id=id)
        for i in file_obj1:
            file=i.my_file.file
        with open(f'{settings.BASE_DIR}//{file}','r') as f:
            f1=json.load(f)
        for i in f1:
            if i['Date'] != 'None' or i['Date'] != 'null':
               list_date.append((i['Date']))
        for i in list_date:
            date_str =i
            datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
            date_object = datetime_object.date()
            date_obj.append(date_object)
        sorted_date=sorted(date_obj)
        from_date=sorted_date[0]
        to_date=sorted_date[-1] 
        data={'data':f1,'f':from_date,'t':to_date}
          
    except:
        return render(request,'pm_view_file.html',)
    return render(request,'pm_view_file.html',data)







def Make_qc(request):
    err=''
    if request.method=='POST':
        f_n=request.POST.get('f_n')
        l_n=request.POST.get('l_n')  
        email=request.POST.get('email')
        p=request.POST.get('p')
        try:
            user=User.objects.create_user(first_name=f_n,last_name=l_n,email=email,username=email,password=p)
            Qc_user.objects.create(user=user)
            err='no'    
            return redirect('/')
        except:
            err='yes'
    return render(request,'make_qc.html') 

def Qc_login(request):
    if request.method == 'POST':
        u = request.POST.get('email')
        p = request.POST.get('p')
        user = authenticate(User, username=u, password=p)
        if user is not None:
            request.session['uid'] = user.id
            receiver_email = u
            otp_length = 6
            otp = math.floor(random.random() * 10**(otp_length-1) + 10**(otp_length-1))
            # Send OTP via email
            subject = "OTP Verification"
            body = f"Your OTP is: {otp}"
            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{body}")
                server.quit()
                print("OTP sent successfully")    
                # Store OTP in session
                request.session['otp'] = otp   
                # Redirect to OTP verification page
                return redirect('/verify_otp2')
            except:
                err = 'yes'
                return render(request, 'qc_login.html', locals())
        else:
            err = 'yes'
            return render(request, 'qc_login.html', locals())
    return render(request, 'qc_login.html', locals())

def verify_otp2(request):    
    us=request.session.get('uid')
    user=User.objects.get(id=us)
    # print(user)      
    if request.method == 'POST':
        otp_user = request.POST.get('otp')
        otp_session = request.session.get('otp')
        if otp_user == str(otp_session):
            msg = 'Successfully Verified'
            login(request, user)
            err = 'no'
            return redirect('/qc_home')
        else:
            msg = 'Invalid OTP'
            err = 'yes'
            return render(request, 'verify_otp.html', locals())
    return render(request, 'verify_otp.html', locals())

def Logout_user(request):
    logout(request)
    return redirect('/')

def Push_file(request,id):
    if request.method == 'POST':
        my_file = Push_to_pm_file.objects.get(id=id)
        file_name = request.POST.get('file_name')
        user_id = request.POST.get('user')
        end_index = int(request.POST.get('end'))
        print(end_index)

        # Load the original file
        file_path = f'{settings.BASE_DIR}/{my_file.my_file.file}'
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Extract the desired chunk from the original file
        chunk = data[0:end_index]
        # print(chunk)

        # Create a new QC data instance
        qc = my_Qc_data()
        qc.qc_file = f'{file_name}.json'
        qc.my_file = my_file
        qc.end = end_index
        qc.user = Qc_user.objects.get(id=user_id)
        qc.save()

        # Save the chunk to a new file
        chunk_file_path = f'{settings.BASE_DIR}/{qc.qc_file}'
        if not os.path.exists(chunk_file_path):
            with open(chunk_file_path, 'w') as file:
                json.dump(chunk, file)
        else:
            print(f"File {chunk_file_path} already exists.")

        # Update the original file by removing the chunk
        data = data[end_index:]
        with open(file_path, 'w') as file:
            json.dump(data, file)

        # Extract dates from the updated original file
        dates = [datetime.strptime(item['Date'], '%Y-%m-%d').date() for item in data if item['Date'] not in ['None', 'null']]
        if dates:
            my_file.my_file.from_date = min(dates)
            my_file.my_file.to_date = max(dates)
        else:
            my_file.my_file.from_date = None
            my_file.my_file.to_date = None
        my_file.my_file.count = len(data)
        my_file.my_file.save()

        # Extract dates from the chunk file
        with open(chunk_file_path, 'r') as file:
            chunk_data = json.load(file)
        dates = [datetime.strptime(item['Date'], '%Y-%m-%d').date() for item in chunk_data if item['Date'] not in ['None', 'null']]
        if dates:
            qc.from_date = min(dates)
            qc.to_date = max(dates)
        else:
            qc.from_date = None
            qc.to_date = None
        qc.save()
        with open(f'{settings.BASE_DIR}/{qc.qc_file}','r+') as f:
            f.seek(0)  # move file pointer to the beginning of the file
            f1 = json.load(f)
            for item in f1:
                item['Ok'] = 0
            f.seek(0)  # move file pointer to the beginning of the file again
            json.dump(f1, f)
            f.truncate()  # remove any remaining characters after the new JSON data

        return redirect('/pm_home')
    else:
        form = qc_Form()
        return render(request, 'push_form.html', {'form': form})

def Qc_home(request):
    pid=request.session.get('uid')
    user=Qc_user.objects.get(user=pid)
    data=my_Qc_data.objects.filter(user=user)

    for i in data:
        ...
    d={'dat':data}
    return render(request,'qc_home.html',d)

# def Delete1(request,id):
#     u=my_Qc_data.objects.filter(id=id)   
#     u.delete()
#     return redirect('/qc_home')

def Qc_view(request,id):
    list_date=[]
    date_obj=[]
    from_date=''
    to_date=''
    file_id=0
    try:    
        file_obj=my_Qc_data.objects.get(id=id)
        file_obj1=my_Qc_data.objects.filter(id=id)
        for i in file_obj1:
            file=i.qc_file
            file_id=i.id
        with open(f'{settings.BASE_DIR}//{file}','r') as f:
            f1=json.load(f)
        for i in f1:
            if i['Date'] != 'None' or i['Date'] != 'null':
               list_date.append((i['Date']))
        for i in list_date:
            date_str =i
            datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
            date_object = datetime_object.date()
            date_obj.append(date_object)
        sorted_date=sorted(date_obj)
        from_date=sorted_date[0]
        to_date=sorted_date[-1] 
        data={'data':f1,'f':from_date,'t':to_date,'id':file_id}
          
    except:
        return render(request,'qc_view.html',)
    return render(request,'qc_view.html',data)

def Filter_srh(request, id):
    file_obj = my_Qc_data.objects.get(id=id)
    file_obj1 = my_Qc_data.objects.filter(id=id)
    data1 = []
    length = 0

    if request.method == 'POST':
        keyword1 = request.POST.get('keyword')
        keyword2 = request.POST.get('keyword1')
        keyword3 = request.POST.get('keyword2')

        fil1 = request.POST.get('fil1')
        fil2 = request.POST.get('fil2')
        fil3 = request.POST.get('fil3')

        data = []
        for i in file_obj1:
            file = i.qc_file
            ide = i.id

        with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
            original_data = json.load(f)

        data = original_data[:]  # Create a copy of the original data

        if keyword1:
            data = [item for item in original_data if keyword1 in str(item.get(fil1, ''))]

        if keyword2:
            data = [item for item in data if keyword2 in str(item.get(fil2, ''))]

        if keyword3:
            data = [item for item in data if keyword3 in str(item.get(fil3, ''))]
        request.session['data_re'] =data
        data1 = data
        length = len(data1)

    data_record = {'data': data1, 'length': length, 'id': ide}
    return render(request, 'filter.html', data_record)

def Data_save(request, id):
    data = request.session.get('data_re')

    if request.method == 'POST':
        word = request.POST.get('Words')
        column = request.POST.get('col')

        if column is None or column == "None":
            file_obj = my_Qc_data.objects.get(id=id)
            file = file_obj.qc_file

            with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
                original_data = json.load(f)

            for i in range(len(original_data)):
                for item in data:
                    if item == original_data[i]:
                        original_data[i] = [word] * len(original_data[i])

            with open(f'{settings.BASE_DIR}//{file}', 'w') as f:
                json.dump(original_data, f)
            # print('Data Saved')
            return redirect(f'/qc_view_file/{id}')  # redirect to the desired view
        else:
            file_obj = my_Qc_data.objects.get(id=id)
            file = file_obj.qc_file

            with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
                original_data = json.load(f)

            header = original_data[0]  # Assuming the first row is the header

            if column not in header.keys():  # Check if column exists in header
                print('Error: Column not found')
                return redirect('/qc_home')  # redirect to the desired view

            column_key = list(header.keys())[list(header.keys()).index(column)]  # Get the key of the column

            filtered_data = [item for item in data if item in original_data]  # Filtered data

            for i in range(len(original_data)):
                if original_data[i] in filtered_data:
                    original_data[i][column_key] = word

            with open(f'{settings.BASE_DIR}//{file}', 'w') as f:
                json.dump(original_data, f)
            # print('Data Saved')
            return redirect(f'/qc_view_file/{id}')  # redirect to the desired view
    return redirect(f'/qc_home')

def Edit_data(request,id,pid):
    pid=pid
    id=id
    if request.method=='POST':
        a1=request.POST.get('a1')
        a2=request.POST.get('a2')
        a3=request.POST.get('a3')
        a4=request.POST.get('a4')
        a6=request.POST.get('a6')
        a7=request.POST.get('a7')
        a8=request.POST.get('a8')
        a9=request.POST.get('a9')
        a10=request.POST.get('a10')
        a11=request.POST.get('a11')
        a12=request.POST.get('a12')
        a13=request.POST.get('a13')
        a14=request.POST.get('a14')
        a15=request.POST.get('a15')
        a16=request.POST.get('a16')
        a17=request.POST.get('a17')
        a18=request.POST.get('a18')
        a19=request.POST.get('a19')
        a20=request.POST.get('a20')
        a21=request.POST.get('a21')
        a22=request.POST.get('a22')
        
        file_obj = my_Qc_data.objects.get(id=id)
        file = file_obj.qc_file
        id=file_obj.id
        with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
            data = json.load(f)
    
        data[pid]['sr_no']=a1
        data[pid]['Date']=a2
        data[pid]['Regulatory']=a3
        data[pid]['Title']=a4
        data[pid]['KRIMA_status']=a7
        data[pid]['KRIMA_true_false']=a8
        data[pid]['KRIMA_type']=a9
        data[pid]['KRIMA_notes']=a10
        data[pid]['KRIMA_edited_gpt_person_or_business']=a11
        data[pid]['KRIMA_edited_gpt_company_check']=a12
        data[pid]['parent_company_name']=a13
        data[pid]['KRIMA_civil_penalty_validated']=a14
        data[pid]['KRIMA_civil_penalty_cleansed']=a15
        data[pid]['KRIMA_currency']=a16
        data[pid]['KRIMA_civil_penalty_usd']=a17
        data[pid]['KRIMA_disgorgement_restitution_usd']=a18
        data[pid]['KRIMA_imposed_penalty']=a19
        data[pid]['KRIMA_settled_value']=a20
        data[pid]['KRIMA_non_monetary_penalty']=a21
        data[pid]['Ok']=a22

        with open(f'{settings.BASE_DIR}//{file}', 'w') as f:
            json.dump(data,f)
        return redirect(f'/qc_view_file/{id}')
    else:
        file_obj = my_Qc_data.objects.get(id=id)
        file = file_obj.qc_file
        id=file_obj.id
        with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
            data = json.load(f)
        sr_no=data[pid]['sr_no']
        Article=data[pid]['Article']
        Date=data[pid]['Date']
        Regulatory=data[pid]['Regulatory']
        Title=data[pid]['Title']

        URL=data[pid]['URL']
        KRIMA_status=data[pid]['KRIMA_status']
        KRIMA_true_false=data[pid]['KRIMA_true_false']
        KRIMA_type=data[pid]['KRIMA_type']

        KRIMA_notes=data[pid]['KRIMA_notes']
        KRIMA_edited_gpt_person_or_business=data[pid]['KRIMA_edited_gpt_person_or_business']
        KRIMA_edited_gpt_company_check=data[pid]['KRIMA_edited_gpt_company_check']
        parent_company_name=data[pid]['parent_company_name']
        KRIMA_civil_penalty_validated=data[pid]['KRIMA_civil_penalty_validated']

        KRIMA_civil_penalty_cleansed=data[pid]['KRIMA_civil_penalty_cleansed']
        KRIMA_currency=data[pid]['KRIMA_currency']
        KRIMA_civil_penalty_usd=data[pid]['KRIMA_civil_penalty_usd']
        KRIMA_disgorgement_restitution_usd=data[pid]['KRIMA_disgorgement_restitution_usd']
        KRIMA_imposed_penalty=data[pid]['KRIMA_imposed_penalty']

        KRIMA_settled_value=data[pid]['KRIMA_settled_value']
        KRIMA_non_monetary_penalty=data[pid]['KRIMA_non_monetary_penalty']
        ok=data[pid]['Ok']

    return render(request,'edit.html',locals())



import copy
def Add_rows(request, id, pid):
    if request.method == 'POST':
        file_obj = my_Qc_data.objects.get(id=id)
        file = file_obj.qc_file
        id = file_obj.id
        with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
            data1 = json.load(f)
        
        No_rec = request.POST.get('no_rec')
        no_rec = int(No_rec)
        
        # Get the record at position pid
        record_to_copy = data1[pid]  # subtract 1 because pid is 1-indexed
        
        # Copy the record no_rec times and append to the data
        for i in range(no_rec):
            data1.append(copy.deepcopy(record_to_copy))
            print('done')
        
        # Save the updated data back to the file
        with open(f'{settings.BASE_DIR}//{file}', 'w') as f:
            json.dump(data1, f)
        return redirect(f'/qc_view_file/{id}')
    
    else:
        print('no')
    
    data={'id':id,'pid':pid}
    return render(request,'add_row.html',data)

def Qc_filter_edit(request,id,pid):
    file_obj = my_Qc_data.objects.get(id=id)
    file = file_obj.qc_file
    id = file_obj.id
    data = request.session.get('data_re')


    if request.method == 'POST':
        fields = {
            'sr_no': 'a1',
            'Date': 'a2',
            'Regulatory': 'a3',
            'Title': 'a4',
            'KRIMA_status': 'a7',
            'KRIMA_true_false': 'a8',
            'KRIMA_type': 'a9',
            'KRIMA_notes': 'a10',
            'KRIMA_edited_gpt_person_or_business': 'a11',
            'KRIMA_edited_gpt_company_check': 'a12',
            'parent_company_name': 'a13',
            'KRIMA_civil_penalty_validated': 'a14',
            'KRIMA_civil_penalty_cleansed': 'a15',
            'KRIMA_currency': 'a16',
            'KRIMA_civil_penalty_usd': 'a17',
            'KRIMA_disgorgement_restitution_usd': 'a18',
            'KRIMA_imposed_penalty': 'a19',
            'KRIMA_settled_value': 'a20',
            'KRIMA_non_monetary_penalty': 'a21',
            'Ok':'a22',
        }

        for field, key in fields.items():
            data[pid][field] = request.POST.get(key)

        with open(f'{settings.BASE_DIR}/{file}', 'r') as f:
            data1 = json.load(f)
        
        # Assuming pid is the index of the session data in the JSON file
        data1[pid] = data[pid]
        
        with open(f'{settings.BASE_DIR}/{file}', 'w') as f:
            json.dump(data1, f)
        print('done')
        da={'data':data,'id':id}

        return render(request,'filter.html',da)
    else:
        uid=pid
        context = {
            'sr_no': data[pid]['sr_no'],
            'Article': data[pid]['Article'],
            'Date': data[pid]['Date'],
            'Regulatory': data[pid]['Regulatory'],
            'Title': data[pid]['Title'],
            'URL': data[pid]['URL'],
            'KRIMA_status': data[pid]['KRIMA_status'],
            'KRIMA_true_false': data[pid]['KRIMA_true_false'],
            'KRIMA_type': data[pid]['KRIMA_type'],
            'KRIMA_notes': data[pid]['KRIMA_notes'],
            'KRIMA_edited_gpt_person_or_business': data[pid]['KRIMA_edited_gpt_person_or_business'],
            'KRIMA_edited_gpt_company_check': data[pid]['KRIMA_edited_gpt_company_check'],
            'parent_company_name': data[pid]['parent_company_name'],
            'KRIMA_civil_penalty_validated': data[pid]['KRIMA_civil_penalty_validated'],
            'KRIMA_civil_penalty_cleansed': data[pid]['KRIMA_civil_penalty_cleansed'],
            'KRIMA_currency': data[pid]['KRIMA_currency'],
            'KRIMA_civil_penalty_usd': data[pid]['KRIMA_civil_penalty_usd'],
            'KRIMA_disgorgement_restitution_usd': data[pid]['KRIMA_disgorgement_restitution_usd'],
            'KRIMA_imposed_penalty': data[pid]['KRIMA_imposed_penalty'],
            'KRIMA_settled_value': data[pid]['KRIMA_settled_value'],
            'KRIMA_non_monetary_penalty': data[pid]['KRIMA_non_monetary_penalty'],
            'ok':data[pid]['Ok'],
            'pid':uid,
            'id':id
            
        }

        return render(request, 'fil_edit.html', context)
    

import copy

def fil_Add_rows(request, id, pid):
    file_obj = my_Qc_data.objects.get(id=id)
    file = file_obj.qc_file
    data = request.session.get('data_re')
    if request.method == 'POST':
        no_rec = int(request.POST.get('no_rec'))
        
        # Get the record at position pid (assuming pid is 0-indexed)
        record_to_copy = data[pid]
        
        # Copy the record no_rec times and append to the data
        new_data = []
        for _ in range(no_rec):
            new_data.append(copy.deepcopy(record_to_copy))
        
        # Load the existing data from the file
        with open(f'{settings.BASE_DIR}/{file}', 'r') as f:
            existing_data = json.load(f)
        
        # Append the new data to the existing data
        existing_data.extend(new_data)
        
        # Save the updated data back to the file
        with open(f'{settings.BASE_DIR}/{file}', 'w') as f:
            json.dump(existing_data, f)
        return redirect(f'/qc_view_file/{id}')
    
    else:
        print('no')
    
    context = {'id': id, 'pid': pid}
    return render(request, 'fil_add_row.html', context)




    
def Qc_push(request,id):
    upid = request.session.get('uid')
    user = Qc_user.objects.get(user=upid)

    if request.method == 'POST':
        form = pushForm(request.POST)
        if form.is_valid():
            ed_ed = form.cleaned_data['Editior']
            qc_data = my_Qc_data.objects.get(id=id)
            file=qc_data.qc_file
            with open(f'{settings.BASE_DIR}/{file}', 'r') as f:
                f1=json.load(f)
            length=len(f1)
            qc_data.status = True
            try:
                ed_push = Editor_push(
                    Editior=ed_ed,
                    qc_data=qc_data,
                    qc_user=user,
                    rec_length=length,
                )
                ed_push.save()
                qc_data.save()
                return redirect('/qc_home')
            except Exception as e:
                print(f"Error: {e}")
                return render(request, 'push_ed.html', {'form': form})
    else:
        form = pushForm()
    return render(request, 'push_ed.html', {'form': form})
    
def Make_ed(request):
    err=''
    if request.method=='POST':
        f_n=request.POST.get('f_n')
        l_n=request.POST.get('l_n')  
        email=request.POST.get('email')
        p=request.POST.get('p')
        try:
            user=User.objects.create_user(first_name=f_n,last_name=l_n,email=email,username=email,password=p)
            ED_User.objects.create(user=user)
            err='no'    
            return redirect('/home')
        except:
            err='yes'
    return render(request,'make_ed.html')

def Ed_login(request):
    if request.method == 'POST':
        u = request.POST.get('email')
        p = request.POST.get('p')
        user = authenticate(User, username=u, password=p)
        if user is not None:
            request.session['uid'] = user.id
            receiver_email = u
            otp_length = 6
            otp = math.floor(random.random() * 10**(otp_length-1) + 10**(otp_length-1))
            # Send OTP via email
            subject = "OTP Verification"
            body = f"Your OTP is: {otp}"
            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{body}")
                server.quit()
                print("OTP sent successfully")    
                # Store OTP in session
                request.session['otp'] = otp   
                # Redirect to OTP verification page
                return redirect('/verify_otp')
            except:
                err = 'yes'
                return render(request, 'ed_login.html', locals())
        else:
            err = 'yes'
            return render(request, 'ed_login.html', locals())
    return render(request, 'ed_login.html', locals())

def verify_otp(request):    
    us=request.session.get('uid')
    user=User.objects.get(id=us)
    # print(user)      
    if request.method == 'POST':
        otp_user = request.POST.get('otp')
        otp_session = request.session.get('otp')
        if otp_user == str(otp_session):
            msg = 'Successfully Verified'
            login(request, user)
            err = 'no'
            return redirect('/ed_home')
        else:
            msg = 'Invalid OTP'
            err = 'yes'
            return render(request, 'verify_otp.html', locals())
    return render(request, 'verify_otp.html', locals())

def Ed_home(request):
    pid=request.session.get('uid')
    user=ED_User.objects.get(user=pid)
    data=Editor_push.objects.filter(Editior=user)    
    d={'dat':data}
    return render(request,'ed_home.html',d)

def Ed_view_file(request,id):
    list_date=[]
    date_obj=[]
    from_date=''
    to_date=''
    file_id=0
    try:    
        file_obj=Editor_push.objects.get(id=id)
        file_obj1=Editor_push.objects.filter(id=id)
        for i in file_obj1:
            file=i.qc_data.qc_file
            file_id=i.id
        with open(f'{settings.BASE_DIR}//{file}','r') as f:
            f1=json.load(f)
        for i in f1:
            if i['Date'] != 'None' or i['Date'] != 'null':
               list_date.append((i['Date']))
        for i in list_date:
            date_str =i
            datetime_object = datetime.strptime(date_str,'%Y-%m-%d')
            date_object = datetime_object.date()
            date_obj.append(date_object)
        sorted_date=sorted(date_obj)
        from_date=sorted_date[0]
        to_date=sorted_date[-1] 
        data={'data':f1,'f':from_date,'t':to_date,'id':file_id}
          
    except:
        return render(request,'ed_view.html',)
    return render(request,'ed_view.html',data)


def Ed_Filter_srh(request, id):
    file_obj = Editor_push.objects.get(id=id)
    file_obj1 = Editor_push.objects.filter(id=id)
    data1 = []
    length = 0

    if request.method == 'POST':
        keyword1 = request.POST.get('keyword')
        keyword2 = request.POST.get('keyword1')
        keyword3 = request.POST.get('keyword2')

        fil1 = request.POST.get('fil1')
        fil2 = request.POST.get('fil2')
        fil3 = request.POST.get('fil3')

        data = []
        for i in file_obj1:
            file = i.qc_data.qc_file
            ide = i.id

        with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
            original_data = json.load(f)

        data = original_data[:]  # Create a copy of the original data

        if keyword1:
            data = [item for item in original_data if keyword1 in str(item.get(fil1, ''))]

        if keyword2:
            data = [item for item in data if keyword2 in str(item.get(fil2, ''))]

        if keyword3:
            data = [item for item in data if keyword3 in str(item.get(fil3, ''))]
        request.session['data_re1'] =data
        data1 = data
        length = len(data1)

    data_record = {'data': data1, 'length': length, 'id': ide}
    return render(request, 'ed_filter.html', data_record)

def Ed_Data_save(request, id):
    data = request.session.get('data_re')

    if request.method == 'POST':
        word = request.POST.get('Words')
        column = request.POST.get('col')

        if column is None or column == "None":
            file_obj = Editor_push.objects.get(id=id)
            file = file_obj.qc_data.qc_file

            with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
                original_data = json.load(f)

            for i in range(len(original_data)):
                for item in data:
                    if item == original_data[i]:
                        original_data[i] = [word] * len(original_data[i])

            with open(f'{settings.BASE_DIR}//{file}', 'w') as f:
                json.dump(original_data, f)
            # print('Data Saved')
            return redirect(f'/ed_view_file/{id}')  # redirect to the desired view
        else:
            file_obj = Editor_push.objects.get(id=id)
            file = file_obj.qc_data.qc_file

            with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
                original_data = json.load(f)

            header = original_data[0]  # Assuming the first row is the header

            if column not in header.keys():  # Check if column exists in header
                print('Error: Column not found')
                return redirect('/ed_home')  # redirect to the desired view

            column_key = list(header.keys())[list(header.keys()).index(column)]  # Get the key of the column

            filtered_data = [item for item in data if item in original_data]  # Filtered data

            for i in range(len(original_data)):
                if original_data[i] in filtered_data:
                    original_data[i][column_key] = word

            with open(f'{settings.BASE_DIR}//{file}', 'w') as f:
                json.dump(original_data, f)
            # print('Data Saved')
            return redirect(f'/ed_view_file/{id}')  # redirect to the desired view
    return redirect(f'/ed_home')

def Ed_Edit_data(request, id, pid):
    pid=pid
    id=id
    if request.method=='POST':
        a1=request.POST.get('a1')
        a2=request.POST.get('a2')
        a3=request.POST.get('a3')
        a4=request.POST.get('a4')
        a6=request.POST.get('a6')
        a7=request.POST.get('a7')
        a8=request.POST.get('a8')
        a9=request.POST.get('a9')
        a10=request.POST.get('a10')
        a11=request.POST.get('a11')
        a12=request.POST.get('a12')
        a13=request.POST.get('a13')
        a14=request.POST.get('a14')
        a15=request.POST.get('a15')
        a16=request.POST.get('a16')
        a17=request.POST.get('a17')
        a18=request.POST.get('a18')
        a19=request.POST.get('a19')
        a20=request.POST.get('a20')
        a21=request.POST.get('a21')
        a22=request.POST.get('a22')
        
        file_obj = Editor_push.objects.get(id=id)
        file = file_obj.qc_data.qc_file
        id=file_obj.id
        with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
            data = json.load(f)
    
        data[pid]['sr_no']=a1
        data[pid]['Date']=a2
        data[pid]['Regulatory']=a3
        data[pid]['Title']=a4
        data[pid]['KRIMA_status']=a7
        data[pid]['KRIMA_true_false']=a8
        data[pid]['KRIMA_type']=a9
        data[pid]['KRIMA_notes']=a10
        data[pid]['KRIMA_edited_gpt_person_or_business']=a11
        data[pid]['KRIMA_edited_gpt_company_check']=a12
        data[pid]['parent_company_name']=a13
        data[pid]['KRIMA_civil_penalty_validated']=a14
        data[pid]['KRIMA_civil_penalty_cleansed']=a15
        data[pid]['KRIMA_currency']=a16
        data[pid]['KRIMA_civil_penalty_usd']=a17
        data[pid]['KRIMA_disgorgement_restitution_usd']=a18
        data[pid]['KRIMA_imposed_penalty']=a19
        data[pid]['KRIMA_settled_value']=a20
        data[pid]['KRIMA_non_monetary_penalty']=a21
        data[pid]['Ok']=a22

        with open(f'{settings.BASE_DIR}//{file}', 'w') as f:
            json.dump(data,f)
        return redirect(f'/ed_view_file/{id}')
    else:
        file_obj = Editor_push.objects.get(id=id)
        file = file_obj.qc_data.qc_file
        id=file_obj.id
        with open(f'{settings.BASE_DIR}//{file}', 'r') as f:
            data = json.load(f)
        sr_no=data[pid]['sr_no']
        Article=data[pid]['Article']
        Date=data[pid]['Date']
        Regulatory=data[pid]['Regulatory']
        Title=data[pid]['Title']

        URL=data[pid]['URL']
        KRIMA_status=data[pid]['KRIMA_status']
        KRIMA_true_false=data[pid]['KRIMA_true_false']
        KRIMA_type=data[pid]['KRIMA_type']

        KRIMA_notes=data[pid]['KRIMA_notes']
        KRIMA_edited_gpt_person_or_business=data[pid]['KRIMA_edited_gpt_person_or_business']
        KRIMA_edited_gpt_company_check=data[pid]['KRIMA_edited_gpt_company_check']
        parent_company_name=data[pid]['parent_company_name']
        KRIMA_civil_penalty_validated=data[pid]['KRIMA_civil_penalty_validated']

        KRIMA_civil_penalty_cleansed=data[pid]['KRIMA_civil_penalty_cleansed']
        KRIMA_currency=data[pid]['KRIMA_currency']
        KRIMA_civil_penalty_usd=data[pid]['KRIMA_civil_penalty_usd']
        KRIMA_disgorgement_restitution_usd=data[pid]['KRIMA_disgorgement_restitution_usd']
        KRIMA_imposed_penalty=data[pid]['KRIMA_imposed_penalty']

        KRIMA_settled_value=data[pid]['KRIMA_settled_value']
        KRIMA_non_monetary_penalty=data[pid]['KRIMA_non_monetary_penalty']
        ok=data[pid]['Ok']

    return render(request,'ed_edit.html',locals())

def Ed_filter_edit(request,id,pid):
    file_obj = Editor_push.objects.get(id=id)
    file = file_obj.qc_data.qc_file
    id = file_obj.id
    data = request.session.get('data_re1')

    if request.method == 'POST':
        fields = {
            'sr_no': 'a1',
            'Date': 'a2',
            'Regulatory': 'a3',
            'Title': 'a4',
            'KRIMA_status': 'a7',
            'KRIMA_true_false': 'a8',
            'KRIMA_type': 'a9',
            'KRIMA_notes': 'a10',
            'KRIMA_edited_gpt_person_or_business': 'a11',
            'KRIMA_edited_gpt_company_check': 'a12',
            'parent_company_name': 'a13',
            'KRIMA_civil_penalty_validated': 'a14',
            'KRIMA_civil_penalty_cleansed': 'a15',
            'KRIMA_currency': 'a16',
            'KRIMA_civil_penalty_usd': 'a17',
            'KRIMA_disgorgement_restitution_usd': 'a18',
            'KRIMA_imposed_penalty': 'a19',
            'KRIMA_settled_value': 'a20',
            'KRIMA_non_monetary_penalty': 'a21',
            'Ok':'a22',
        }

        for field, key in fields.items():
            data[pid][field] = request.POST.get(key)

        with open(f'{settings.BASE_DIR}/{file}', 'r') as f:
            data1 = json.load(f)
        
        # Assuming pid is the index of the session data in the JSON file
        data1[pid] = data[pid]
        
        with open(f'{settings.BASE_DIR}/{file}', 'w') as f:
            json.dump(data1, f)
        print('done')
        da={'data':data,'id':id}

        return render(request,'ed_filter.html',da)
    else:
        context = {
            'sr_no': data[pid]['sr_no'],
            'Article': data[pid]['Article'],
            'Date': data[pid]['Date'],
            'Regulatory': data[pid]['Regulatory'],
            'Title': data[pid]['Title'],
            'URL': data[pid]['URL'],
            'KRIMA_status': data[pid]['KRIMA_status'],
            'KRIMA_true_false': data[pid]['KRIMA_true_false'],
            'KRIMA_type': data[pid]['KRIMA_type'],
            'KRIMA_notes': data[pid]['KRIMA_notes'],
            'KRIMA_edited_gpt_person_or_business': data[pid]['KRIMA_edited_gpt_person_or_business'],
            'KRIMA_edited_gpt_company_check': data[pid]['KRIMA_edited_gpt_company_check'],
            'parent_company_name': data[pid]['parent_company_name'],
            'KRIMA_civil_penalty_validated': data[pid]['KRIMA_civil_penalty_validated'],
            'KRIMA_civil_penalty_cleansed': data[pid]['KRIMA_civil_penalty_cleansed'],
            'KRIMA_currency': data[pid]['KRIMA_currency'],
            'KRIMA_civil_penalty_usd': data[pid]['KRIMA_civil_penalty_usd'],
            'KRIMA_disgorgement_restitution_usd': data[pid]['KRIMA_disgorgement_restitution_usd'],
            'KRIMA_imposed_penalty': data[pid]['KRIMA_imposed_penalty'],
            'KRIMA_settled_value': data[pid]['KRIMA_settled_value'],
            'KRIMA_non_monetary_penalty': data[pid]['KRIMA_non_monetary_penalty'],
            'ok':data[pid]['Ok'],
        }

        return render(request, 'ed_fi.html', context)
    


def Qc_send_file_record(request):
    qc_data=my_Qc_data.objects.all()
    data={'data':qc_data}
    return render(request,'qc_record.html',data)


def Ed_push(request,id):
    uid=request.session.get('uid')
    u=Editor_push.objects.get(id=id) 
    user=User.objects.get(id=uid)
    ed=ED_User.objects.get(user=user)
    # print(user)
    pd=Final_data_PM()
    pd.Editior=ed
    pd.Edited_file=u
    pd.save()
    u.sta=True
    u.save()
    return redirect('/ed_home')

def Ed_send_file_record(request):
    qc_data=Final_data_PM.objects.all()
    data={'data':qc_data}
    return render(request,'ed_record.html',data)



def Download_file(request, id):
    files = ''
    name = ''
    fd = Final_data_PM.objects.filter(id=id)
    for i in fd:
        files = i.Edited_file.qc_data.qc_file
        name = i.Edited_file.qc_data.qc_file.name
    directory = os.path.join(settings.BASE_DIR, 'data_file')
    if not os.path.exists(directory):
        os.makedirs(directory)
    n = os.path.splitext(name)[0]
    with open(files.path, 'r') as f:
        f1 = json.load(f)
    data = []
    for i in f1:
        del i["GPT_Description_Automated"]
        del i['parent_company_name']
        if 'Ok' in i:
           del i['Ok']
        data.append(i)
    df = pd.DataFrame(data)
    output_file = os.path.join(directory, f'{n}.xlsx')
    df.to_excel(output_file, index=False)
    # Send the file as a response to the client
    response = HttpResponse(open(output_file, 'rb').read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_file)}"'
    return response

def About_us(request):
    return render(request,'about_us.html')

def All_user(request):
    user_types = {
        'PM': Pm_user.objects.all(),
        'QC': Qc_user.objects.all(),
        'Editor': ED_User.objects.all()
    }
    return render(request, 'User_list.html', {'user_types': user_types})

# def Feautre(request):
#     return render(request,'feature.html')