from django.shortcuts import render,redirect
from .forms import catform,vehicleform
from .models import Category,Vehicle
from django.db.models import Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='accounts/loginpage/')
def dashboard(request):
    parked=Vehicle.objects.filter(status="parked").count
    departed=Vehicle.objects.filter(status="leaved").count
    available_category=Category.objects.all().count
    total_earnings=Vehicle.objects.aggregate(total=Sum('parking_charge'))['total']
    total_records=Vehicle.objects.all().count
    total_parking_slots=Category.objects.aggregate(total=Sum('vehicle_limit'))['total']
    context={
        'parked':parked,
        'departed':departed,
        'available_category':available_category,
        'total_earnings':total_earnings,
        'total_records':total_records,
        'total_parking_slots':total_parking_slots
    }
    return render(request,'dashboard.html', context)


def addvehicle(request):
    form = vehicleform()
    # limit=Category.objects.filter(status="activated")
    current_vehicle=Vehicle.objects.filter(status="parked")
    categories = Category.objects.all()
    try:
        if request.method=='POST':
            form=vehicleform(request.POST)
            if form.is_valid():
                form.save()
                return redirect('addvehcile')
    except ValueError as e:
            error_message = str(e)
            messages.error(request, error_message)

    context={
        'form':form,
        'current_vehicle':current_vehicle,
        'categories':categories,
    }
    return render(request,'vechile_entry.html',context)

def receipt(request,pk):
    r=Vehicle.objects.get(id=pk)
    context={
        'receipt':r
    }
    return render(request,'receipt.html',context)


def addcat(request):
    details=Category.objects.filter(status='activated')
    form = catform()
    if request.method=='POST':
        form=catform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addcat')

    details=Category.objects.all()
    c=Category.objects.all().count()
    page_num=request.GET.get('page') # Creating total pages
    paginator=Paginator(details,3)  # setting total Number of peoducts in a page.
    try:
        details=paginator.page(page_num)
    except PageNotAnInteger:
        details=paginator.page(1)
    except EmptyPage:
        details=paginator.page(paginator.num_pages)    
    
    context={
        'form':form,
        'details':details,
        'total_category':c
    }
    return render(request,'addcat.html',context)







def update_category(request,id):
    e=Category.objects.get(cat_id=id)
    form=catform(instance=e)
    if request.method=="POST":
        form=catform(request.POST,instance=e)
        if form.is_valid():
            form.save()
            return redirect('addcat')
    context={
        'form':form
    }
    return render(request,'updatecat.html',context)

def delete_category(request,id):
    e=Category.objects.get(cat_id=id)
    e.delete()
    return redirect('addcat')



def update_status_cat(request, id):
    record = Category.objects.get(cat_id=id)
    record.status = 'Dactivated'
    record.save()
    return redirect('addcat')



def searchbar(request):
    if request.method=='GET':
        queres = request.GET.get('query')
        if queres:
            search =Vehicle.objects.filter(vehicle_no__iexact=queres)
            return render(request, 'search.html', {'search':search})
        else:
            return render(request, 'search.html')

def manage(request):
    if request.method=='GET':
        manage=Vehicle.objects.all()
        queres = request.GET.get('query')
        if queres:
            search =Vehicle.objects.filter(vehicle_no__iexact=queres)
            return render(request, 'search.html', {'search':search,'manage':manage})
        else:
            return render(request,"manage.html",{'manage':manage})
  
def update_status(request, id):
    record = Vehicle.objects.get(id=id)
    record.status = 'leaved'
    record.save()
    return redirect('manage')

# def reports(request):
#     return render(request,'reports.html')

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import style
style.use('ggplot')
matplotlib.use('Agg') 
import matplotlib.dates as mdates
from io import BytesIO
import base64

def reports(request):
    # Retrieve the data for parked vehicles within the 10-day range
    start_date = datetime.now() - timedelta(days=9)
    end_date = datetime.now()
    parked_vehicles = Vehicle.objects.filter(status='parked', arrival_time__range=(start_date, end_date))

    # Group the parked vehicles by date
    date_counts = {}
    for vehicle in parked_vehicles:
        date = vehicle.arrival_time.date()
        if date in date_counts:
            date_counts[date] += 1
        else:
            date_counts[date] = 1

    # Sort the dates in ascending order
    sorted_dates = sorted(date_counts.keys())

    # Prepare the data for plotting
    dates = [datetime.strptime(date.strftime('%m/%d/%Y'), '%m/%d/%Y') for date in sorted_dates]
    counts = [date_counts[date] for date in sorted_dates]

    # Generate the plot
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(dates, counts, marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Parked Vehicles')
    ax.set_title('Statistical Report: Parked Vehicles within 10-Day Range')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot in a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = buffer.getvalue()
    buffer.close()

    # Encode the plot data as base64 for embedding in the HTML
    plot_base64 = base64.b64encode(plot_data).decode('utf-8')

    # Pass the base64-encoded plot data to the template
    context = {'plot_base64': plot_base64}
    return render(request, 'reports.html', context)



