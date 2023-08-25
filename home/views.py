from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
import mysql.connector as sql
from .forms import ImagefieldForm
from .models import cardetails
from .models import bookingg
from datetime import datetime

fn=''
ln=''
un=''
em=''
pd=''
id=''
id1=''
id2=''
a=''
b=''
lic=''
adh=''
ph=''
didd=''

# Create your views here.

def home(request):
    return render(request,'home.html')


def dsignup(request):
    global fn,ln,un,em,pd
    if request.method=='POST':
        m=sql.connect(host='localhost',user='root',passwd='Sanju@2002',database='car',autocommit= True)
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=='firstname':
                fn=value
            if key=='lastname':
                ln=value
            if key=='username':
                un=value
            if key=='email':
                em=value
            if key=='password':
                pd=value
            if key=='password2':
                pdd=value
        if pd==pdd:
            cursor.execute("insert into dealer(un,fn,ln,email,pwd)values(%s,%s,%s,%s,%s)",(un,fn,ln,em,pd,))
            m.commit()
            return redirect('/dlogin')
        else:
            return redirect('/dsignup')

    else:
        return render(request,'dsignup.html')



def dlogin(request):
    global un,pd,id
    if request.method=='POST':
        m=sql.connect(host='localhost',user='root',passwd='Sanju@2002',database='car',autocommit= True)
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=='username':
                un=value
            if key=='password':
                pd=value
        
        cursor.execute("select * from dealer where un=%s and pwd=%s",(un,pd,))
        t=tuple(cursor.fetchall())
        if t==():
            return redirect('/dlogin')
        else:
            cursor.execute("select user_id from dealer where un=%s",(un,))
            idd=str(cursor.fetchall())
            id=idd[2:4]
            return redirect('/dhome')

    else:
        return render(request,'dlogin.html')


def clogin(request):
    global un,pd,idd,id1,a,b
    if request.method=='POST':
        m=sql.connect(host='localhost',user='root',passwd='Sanju@2002',database='car',autocommit= True)
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=='username':
                un=value
            if key=='password':
                pd=value
            if key=='pickup':
                a=value
            if key=='drop':
                b=value
        
        cursor.execute("select * from customer where un=%s and pwd=%s",(un,pd,))
        t=tuple(cursor.fetchall())
        if t==():
            return redirect('/clogin')
        else:
            cursor.execute("select id,un from customer where un=%s",(un,))
            idd=str(cursor.fetchall())
            id1=idd[2:4]
            return redirect('/search')

    else:
        return render(request,'clogin.html')



def csignup(request):
    global fn,ln,un,em,pd,ph,lic,adh
    if request.method=='POST':
        m=sql.connect(host='localhost',user='root',passwd='Sanju@2002',database='car',autocommit= True)
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=='firstname':
                fn=value
            if key=='lastname':
                ln=value
            if key=='username':
                un=value
            if key=='email':
                em=value
            if key=='phone':
                ph=value
            if key=='license':
                lic=value
            if key=='adhar':
                adh=value
            if key=='password':
                pd=value
            if key=='password2':
                pdd=value
        if pd==pdd:
            cursor.execute("insert into customer(un,fn,ln,email,phone,license,adhar,pwd)values(%s,%s,%s,%s,%s,%s,%s,%s)",(un,fn,ln,em,ph,lic,adh,pd,))
            m.commit()
            return redirect('/clogin')
        else:
            return redirect('/csignup')
            print("password not match")

    else:
        return render(request,'csignup.html') 

def dhome(request): 
    context = {}
    if request.method == "POST":
        form = ImagefieldForm(request.POST, request.FILES) 
        if form.is_valid(): 
            name = form.cleaned_data.get("Car_name") 
            color = form.cleaned_data.get("Color")
            city = form.cleaned_data.get("City")
            pinc = form.cleaned_data.get("Pincode")
            capac = form.cleaned_data.get("Capacity")
            transm = form.cleaned_data.get("Transmission")
            fuel= form.cleaned_data.get("Fuel")
            price= form.cleaned_data.get("Price")
            obj = cardetails.objects.create(
                                 uid=id,
                                 carname = name,
                                 color=color,
                                 city=city,
                                 pincode=pinc,
                                 capacity=capac,
                                 transmission=transm,
                                 fuel=fuel,
                                 price=price,
                                 ) 
            obj.save() 
            print(obj)
            return redirect('/success') 
    else: 
        form = ImagefieldForm()
        context['form'] = form
        return render( request, "dhome.html", context) 

def search(request):
    m=sql.connect(host='localhost',user='root',passwd='Sanju@2002',database='car',autocommit= True)
    cursor=m.cursor()
    cursor.execute("select cid from booking where (pickup between (%s)and(%s)) or (dp between (%s)and (%s))",(a,b,a,b,))
    iddd=tuple(cursor.fetchall())
    n=len(iddd)
    idd=str(iddd)
    if iddd==():
        car = cardetails.objects.all()
        return render(request,'search.html',{'car':car})
    if n==1:
        id2=idd[2:4]
        car = cardetails.objects.exclude(id=id2)
        return render(request,'search.html',{'car':car})
    elif n==2:
        id2=idd[2:4]
        id3=idd[9:11]
        car = cardetails.objects.exclude(id=id2).exclude(id=id3)
        return render(request,'search.html',{'car':car})
    elif n==3:
        id2=idd[2:4]
        id3=idd[9:11]
        id4=idd[16:18]
        car = cardetails.objects.exclude(id=id2).exclude(id=id3).exclude(id=id4)
        return render(request,'search.html',{'car':car})
    elif n==4:
        id2=idd[2:4]
        id3=idd[9:11]
        id4=idd[16:18]
        id5=idd[23:25]
        car = cardetails.objects.exclude(id=id2).exclude(id=id3).exclude(id=id4).exclude(id=id5)
        return render(request,'search.html',{'car':car})
    elif n==5:
        id2=idd[2:4]
        id3=idd[9:11]
        id4=idd[16:18]
        id5=idd[23:25]
        id6=idd[30:33]
        car = cardetails.objects.exclude(id=id2).exclude(id=id3).exclude(id=id4).exclude(id=id5).exclude(id6)
        return render(request,'search.html',{'car':car})
    elif n==6:
        id2=idd[2:4]
        id3=idd[9:11]
        id4=idd[16:18]
        id5=idd[23:25]
        id6=idd[30:33]
        id7=idd[37:39]
        car = cardetails.objects.exclude(id=id2).exclude(id=id3).exclude(id=id4).exclude(id=id5).exclude(id6).exclude(id=id7)
        return render(request,'search.html',{'car':car})
    elif n==7:
        id2=idd[2:4]
        id3=idd[9:11]
        id4=idd[16:18]
        id5=idd[23:25]
        id6=idd[30:33]
        id7=idd[37:39]
        id8=idd[44:46]
        car = cardetails.objects.exclude(id=id2).exclude(id=id3).exclude(id=id4).exclude(id=id5).exclude(id6).exclude(id=id7).exclude(id=id8)
        return render(request,'search.html',{'car':car})

    else:
        id2=idd[2:4]
        id3=idd[9:11]
        id4=idd[16:18]
        id5=idd[23:25]
        id6=idd[30:33]
        id7=idd[37:39]
        id8=idd[44:46]
        id9=idd[51:53]
        car = cardetails.objects.exclude(id=id2).exclude(id=id3).exclude(id=id4).exclude(id=id5).exclude(id6).exclude(id=id7).exclude(id=id8).exclude(id=id9)
        return render(request,'search.html',{'car':car})
      
def booking(request):
    if request.method=="POST":
        m=sql.connect(host='localhost',user='root',passwd='Sanju@2002',database='car',autocommit= True)
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=='carid':
                ci=value
            if key=='cname':
                cn=value    
        cursor.execute("select uid from cdetails where id=(%s)",(ci,))
        di=str(cursor.fetchall())
        didd=di[2:4]
        do=datetime.strptime(a,'%Y-%m-%d')
        do1=datetime.strptime(b,'%Y-%m-%d')
        dc=(do1-do)
        dc1=str(dc)
        dc2=int(dc1[0])
        cursor.execute("select price from cdetails where id=(%s)",(ci,))
        di=str(cursor.fetchall())
        didd1=int(di[3:7])
        dc3=dc2*didd1
        cursor.execute("insert into booking(cid,did,uid,uname,carname,pickup,dp,tot_days,tot_price)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(ci,didd,id1,un,cn,a,b,dc2,dc3,))    
        return redirect('/conform')
    else:
        return render(request,"search.html")

def conform(request):
    return render(request,"bookconform.html")

def book(request):
    bk = bookingg.objects.all()
    return render(request,'uhistory.html',{'book':bk})
    
def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def manage(request):
    mng=bookingg.objects.filter(did=id)
    return render(request,'manage.html',{'manage':mng})

def managee(request):
    mng=bookingg.objects.filter(uid=id1)
    return render(request,'history.html',{'managee':mng})

def history(request):
    if request.method=="POST":
        m=sql.connect(host='localhost',user='root',passwd='Sanju@2002',database='car',autocommit= True)
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=='bid':
                cancel=value  
        cursor.execute("delete from booking where id=(%s)",(cancel,))
        return redirect('/search')
    else:
        return render(request,"history.html")

def succes(request):
    return render(request,'successful.html')
    