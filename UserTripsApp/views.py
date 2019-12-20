from django.shortcuts import render , HttpResponse , redirect
from .models import Users , Trips
from django.contrib import messages
import bcrypt
# Create your views here.


def index(request):
    return render(request,'index.html')


def register(request):
    errors = Users.objects.basic_validator(request.POST)
    hashPW = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        logged_user = Users.objects.create(first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashPW
        )
        request.session['userID'] = logged_user.id
        return redirect('/dashboard')

def login(request):
    user = Users.objects.filter(email=request.POST['email']) 
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userID'] = logged_user.id
            return redirect('/dashboard')
    messages.error(request,'Invalid email or password')
    return redirect("/")

def dashboard(request):
    if request.session.get('userID', None) == None:
        return redirect("/")
    user = Users.objects.get(id = int(request.session['userID']))
    all_trips = Trips.objects.all()
    other_trips = Trips.objects.exclude(user_participants =user.id)
    user_trips = Trips.objects.filter(user_participants = user.id)

    print(user_trips)

    context = {
        'User' : user,
        'all_trips' : all_trips,
        'user_trips' : user_trips,
        'other_trips' : other_trips
    }

    return render(request,'dashboard.html',context)



def new_trip(request):
    if request.session.get('userID', None) == None:
        return redirect("/")
    context = {
        'User' : Users.objects.get(id = int(request.session['userID']))
    }
    return render(request,'new_trip.html',context)


def trip_create(request):

    if request.session.get('userID', None) == None:
        return redirect("/")
    errors = Trips.objects.basic_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/Trips/New')
    else:
        cur_user = Users.objects.get(id = int(request.session['userID']))
        cur_trip = Trips.objects.create(destination = request.POST['destination'],
            plan = request.POST['plan'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            created_by = cur_user
        )
        cur_trip.user_participants.add(cur_user)
        return redirect('/dashboard')


def view_trip(request,Trip_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    cur_trip = Trips.objects.get(id = Trip_ID)
    cur_user = Users.objects.get(id = int(request.session['userID']))
    cur_participants = cur_trip.user_participants.all()
    context = {
        'Trip' : cur_trip,
        'User' : cur_user,
        'participants' : cur_participants

    }
    return render(request,'view_trip.html',context)
    

def edit_trip(request,Trip_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")

    cur_trip = Trips.objects.get(id = Trip_ID)
    cur_user = Users.objects.get(id = int(request.session['userID']))
    
    context = {
        'Trip' : cur_trip,
        'User' : cur_user
    }

    return render(request,'edit_trip.html',context)


def trip_update(request,Trip_ID):

    if request.session.get('userID', None) == None:
        return redirect("/")
    errors = Trips.objects.basic_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f'/Trips/Edit/{Trip_ID}')
    else:
        cur_user = Users.objects.get(id = int(request.session['userID']))
        cur_trip = Trips.objects.get(id = Trip_ID)

        cur_trip.destination = request.POST['destination']
        cur_trip.plan = request.POST['plan']
        cur_trip.start_date = request.POST['start_date']
        cur_trip.end_date = request.POST['end_date']
        cur_trip.save()
        return redirect('/dashboard')


def remove_trip(request,Trip_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    Trips.objects.get(id = Trip_ID).delete()

    return redirect('/dashboard')


def join_trip(request,Trip_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    cur_user = Users.objects.get(id = int(request.session['userID']))
    cur_trip = Trips.objects.get(id = Trip_ID)
    cur_user.trips_joined.add(cur_trip)

    return redirect('/dashboard')

def cancel_trip(request,Trip_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    
    cur_user = Users.objects.get(id = int(request.session['userID']))
    cur_trip = Trips.objects.get(id = Trip_ID)
    cur_user.trips_joined.remove(cur_trip)
    print("find this right here")
    return redirect('/dashboard')


def log_out(request):
    request.session.flush()
    return redirect('/')
