from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector as sql
from .forms import ImagefieldForm
from .models import cardetails, bookingg
from datetime import datetime

# HOME
def home(request):
    return render(request, 'home.html')

# DEALER SIGNUP
def dsignup(request):
    if request.method == 'POST':
        data = request.POST
        fn = data.get('firstname')
        ln = data.get('lastname')
        un = data.get('username')
        em = data.get('email')
        pd = data.get('password')
        pdd = data.get('password2')

        if pd == pdd:
            conn = sql.connect(host='localhost', user='root', passwd='Sanju@2002', database='car', autocommit=True)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO dealer(un, fn, ln, email, pwd) VALUES (%s, %s, %s, %s, %s)", (un, fn, ln, em, pd))
            return redirect('/dlogin')
        else:
            return render(request, 'dsignup.html', {'error': 'Passwords do not match'})
    return render(request, 'dsignup.html')

# DEALER LOGIN
def dlogin(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        pd = request.POST.get('password')

        conn = sql.connect(host='localhost', user='root', passwd='Sanju@2002', database='car', autocommit=True)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM dealer WHERE un=%s AND pwd=%s", (un, pd))
        result = cursor.fetchone()

        if result:
            request.session['dealer_id'] = result[0]
            return redirect('/dhome')
        else:
            return render(request, 'dlogin.html', {'error': 'Invalid username or password'})
    return render(request, 'dlogin.html')

# CUSTOMER SIGNUP
def csignup(request):
    if request.method == 'POST':
        data = request.POST
        fn = data.get('firstname')
        ln = data.get('lastname')
        un = data.get('username')
        em = data.get('email')
        ph = data.get('phone')
        lic = data.get('license')
        adh = data.get('adhar')
        pd = data.get('password')
        pdd = data.get('password2')

        if pd == pdd:
            conn = sql.connect(host='localhost', user='root', passwd='Sanju@2002', database='car', autocommit=True)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customer(un, fn, ln, email, phone, license, adhar, pwd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (un, fn, ln, em, ph, lic, adh, pd))
            return redirect('/clogin')
        else:
            return render(request, 'csignup.html', {'error': 'Passwords do not match'})
    return render(request, 'csignup.html')

# CUSTOMER LOGIN
def clogin(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        pd = request.POST.get('password')
        a = request.POST.get('pickup')
        b = request.POST.get('drop')

        conn = sql.connect(host='localhost', user='root', passwd='Sanju@2002', database='car', autocommit=True)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM customer WHERE un=%s AND pwd=%s", (un, pd))
        result = cursor.fetchone()

        if result:
            request.session['customer_id'] = result[0]
            request.session['username'] = un
            request.session['pickup'] = a
            request.session['drop'] = b
            return redirect('/search')
        else:
            return render(request, 'clogin.html', {'error': 'Invalid username or password'})
    return render(request, 'clogin.html')

# DEALER HOME (Add Car)
def dhome(request):
    dealer_id = request.session.get('dealer_id')
    if not dealer_id:
        return redirect('/dlogin')

    context = {}
    if request.method == "POST":
        form = ImagefieldForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = dealer_id
            obj.save()
            return redirect('/success')
    else:
        form = ImagefieldForm()
    context['form'] = form
    return render(request, "dhome.html", context)

# SEARCH AVAILABLE CARS
def search(request):
    a = request.session.get('pickup')
    b = request.session.get('drop')

    conn = sql.connect(host='localhost', user='root', passwd='Sanju@2002', database='car', autocommit=True)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cid FROM booking 
        WHERE (pickup BETWEEN %s AND %s) OR (dp BETWEEN %s AND %s)
    """, (a, b, a, b))
    booked_ids = [row[0] for row in cursor.fetchall()]
    if booked_ids:
        car = cardetails.objects.exclude(id__in=booked_ids)
    else:
        car = cardetails.objects.all()
    return render(request, 'search.html', {'car': car})

# BOOKING A CAR
def booking(request):
    if request.method == "POST":
        customer_id = request.session.get('customer_id')
        username = request.session.get('username')
        a = request.session.get('pickup')
        b = request.session.get('drop')

        car_id = request.POST.get('carid')
        car_name = request.POST.get('cname')

        conn = sql.connect(host='localhost', user='root', passwd='Sanju@2002', database='car', autocommit=True)
        cursor = conn.cursor()

        # Get dealer ID of selected car
        cursor.execute("SELECT uid FROM cdetails WHERE id=%s", (car_id,))
        dealer_id = cursor.fetchone()[0]

        # Calculate total days and price
        start = datetime.strptime(a, '%Y-%m-%d')
        end = datetime.strptime(b, '%Y-%m-%d')
        total_days = (end - start).days

        cursor.execute("SELECT price FROM cdetails WHERE id=%s", (car_id,))
        price = int(cursor.fetchone()[0])
        total_price = total_days * price

        # Insert booking
        cursor.execute("""
            INSERT INTO booking(cid, did, uid, uname, carname, pickup, dp, tot_days, tot_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (car_id, dealer_id, customer_id, username, car_name, a, b, total_days, total_price))

        return redirect('/conform')
    return render(request, "search.html")

# BOOKING CONFIRMATION
def conform(request):
    return render(request, "bookconform.html")

# DEALER BOOKING MANAGEMENT
def manage(request):
    dealer_id = request.session.get('dealer_id')
    bookings = bookingg.objects.filter(did=dealer_id)
    return render(request, 'manage.html', {'manage': bookings})

# CUSTOMER BOOKING HISTORY
def managee(request):
    customer_id = request.session.get('customer_id')
    bookings = bookingg.objects.filter(uid=customer_id)
    return render(request, 'history.html', {'managee': bookings})

# CANCEL BOOKING
def history(request):
    if request.method == "POST":
        cancel_id = request.POST.get('bid')
        conn = sql.connect(host='localhost', user='root', passwd='Sanju@2002', database='car', autocommit=True)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM booking WHERE id=%s", (cancel_id,))
        return redirect('/search')
    return render(request, "history.html")

# STATIC PAGES
def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def succes(request):
    return render(request, 'successful.html')

def book(request):
    bookings = bookingg.objects.all()
    return render(request, 'uhistory.html', {'book': bookings})