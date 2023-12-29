
from datetime import date
from django.core.serializers.json import DjangoJSONEncoder
import json
import json
from django.http import JsonResponse
from django.shortcuts import render 

from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta , time
from collections import defaultdict
from django.views.decorators.csrf import csrf_protect

from Superv.models import Salerep, Sales



@csrf_protect
def userlogin(response):
    return render(response, 'login.html')

@login_required(login_url='login') 
def dashboard(request):
    context = {}
    
    sales_reps = Salerep.objects.filter(datedepot=date.today()).order_by('datedepot', '-timedepot')
    date_check=date.today()
   
    context = {
        'sales_reps': sales_reps,
        'date_check' : date_check
    }
   
    if request.user.is_authenticated:
       
        context['user_info'] = {
            'username': request.user.username,
            'email': request.user.email,
        }
    return render(request, 'dashboard.html' , context)

@login_required(login_url='login') 
def search_orders(request):
    date_check = None
    search_date=None
    if request.method == 'POST':
        search_date = request.POST.get('search-date')
        today = date.today()

        if not search_date:
            message = 'Please provide a search date.'
            orders = None
        elif search_date > str(today):
            message = 'Search date cannot be in the future.'
            orders = None
        else:
            orders = Salerep.objects.filter(datedepot=search_date).order_by('datedepot', '-timedepot')
            date_check = search_date
            message = None
    else:
       
        message = None
        orders = None
    # timedepot_values = [items.timedepot for items in orders]
  
    context = {'sales_reps': orders, 'message': message ,  'date_check' : date_check}
    print(context)
    return render(request, 'dashboard.html', context)

@login_required(login_url='login') 
def order_detail(request, id):
  
    related_sales = Sales.objects.filter(numdepot=id)
    total=0
    for item in related_sales:
        total +=  item.pricet
    return render(request, 'order_detail.html', {'sales_reps': related_sales , 'total':total})

@login_required(login_url='login') 
def get_orders(request):
    latest_orders = Salerep.objects.filter(datedepot=date.today()).order_by('datedepot', '-timedepot')
    data = [{'order_id':order.numdepot,'date': order.datedepot, 'time':order.timedepot, 'name': order.serveur,'nbrarticle':order.nbrarticle ,
               'price': order.total ,} for order in latest_orders]
   
   
    return JsonResponse({'orders': data})

@login_required(login_url='login') 
def dashboard_by_date(request, date):
    
    sales_reps = Salerep.objects.filter(datedepot=date).order_by('datedepot', 'timedepot')
   
    
    context = {
        'sales_reps': sales_reps,
        'date_check': date,
    }

   
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def get_statistic(request):
    context = data_perDay()
    
    return render(request, 'statistic.html', context)



@login_required(login_url='login')
def chart_data_int(request):

    context = data_perDay()
    
    
    return render(request, 'copy.html', context)

@login_required(login_url='login')
def select_cahrtdates(request):
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    data = data_perDay(start_date,end_date)
  
   
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    
   
    return JsonResponse({'json_data': json_data}, safe=False)

@login_required(login_url='login')
def type_chartdata(request):
    date_type = request.GET.get('date_type')
    first_label = request.GET.get('first_label')
    last_label = request.GET.get('last_label')
    
    column_to_compare = 'datedepot'

    
    lookup = {f'{column_to_compare}__range': [first_label, last_label]}
    data = Salerep.objects.filter(**lookup).values('datedepot', 'total','timedepot').order_by('datedepot')
    
    grouped_data = defaultdict(lambda: {'datedepot': None, 'total': 0, 'timedepot': None})

    j=0

    xtext_options = None
    
    if date_type == 'month':
        for i in range(len(data)-1):
            grouped_data[j]['datedepot'] = data[i]['datedepot'] 
            grouped_data[j]['total'] += data[i]['total']
            grouped_data[j]['timedepot'] = data[i]['timedepot']

            if not same_month(data[i]['datedepot'] , data[i+1]['datedepot'] ):
                j += 1
    
       
        if data:
            grouped_data[j]['datedepot'] = data[len(data)-1]['datedepot']
            grouped_data[j]['total'] += data[len(data)-1]['total']
            grouped_data[j]['timedepot'] = data[len(data)-1]['timedepot']
        xtext_options='Per Month'
    else:
        for i in range(len(data)-1):
            grouped_data[j]['datedepot'] = data[i]['datedepot'] 
            grouped_data[j]['total'] += data[i]['total']
            grouped_data[j]['timedepot'] = data[i]['timedepot']

            if data[i]['datedepot'] != data[i+1]['datedepot']:
                j += 1
  
      
        if data:
            grouped_data[j]['datedepot'] = data[len(data)-1]['datedepot']
            grouped_data[j]['total'] += data[len(data)-1]['total']
            grouped_data[j]['timedepot'] = data[len(data)-1]['timedepot']
        xtext_options='Per Day'    
   
    grouped_list = list(grouped_data.values())  

    
    chart_labels = [item['datedepot'].strftime('%Y-%m-%d') for item in grouped_list]
    chart_data = [item['total'] for item in grouped_list]


    return JsonResponse({
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'xtext_options' : xtext_options
    })

def same_month(date1, date2):
    return date1.year == date2.year and date1.month == date2.month


def data_perDay(date_A=None, date_B=None):
    if date_A is None or date_B is None:
         data = Salerep.objects.order_by('datedepot').values('datedepot', 'total','timedepot','nbrarticle','serveur')
    else:
       
        column_to_compare = 'datedepot'

        
        lookup = {f'{column_to_compare}__range': [date_A, date_B]}
        data = Salerep.objects.filter(**lookup).values('datedepot', 'total','timedepot','nbrarticle','serveur').order_by('datedepot')
   
    nb_items=0
    profite_perday=0
    for i in range(len(data)):
        nb_items += data[i]['nbrarticle']
        profite_perday += data[i]['total']

  
    today = datetime.now().date()
    filtered_data = [item for item in data if (today - item['datedepot']).days <= 90]

    
    unique_servers = set(item['serveur'] for item in filtered_data)

    
    server_totals = []
    for server in unique_servers:
        total_sum = sum(item['total'] for item in filtered_data if item['serveur'] == server)
        server_totals.append({'serveur': server, 'total_sum': total_sum})
    
    chart_serveur = [item['serveur'] for item in server_totals]
    chart_total_vente = [item['total_sum'] for item in server_totals]


    for i in range(len(data)):
        current_date = data[i]['datedepot']
      
        current_time = data[i]['timedepot'] 
       


        
        if time(0, 0) <= current_time <= time(4, 0):
          
            new_date = current_date - timedelta(days=1)

           
            data[i]['datedepot'] = new_date
    
    grouped_data = defaultdict(lambda: {'datedepot': None, 'total': 0, 'timedepot': None})

    j=0
    for i in range(len(data)-1):
        grouped_data[j]['datedepot'] = data[i]['datedepot'] 
        grouped_data[j]['total'] += data[i]['total']
        grouped_data[j]['timedepot'] = data[i]['timedepot']

        if data[i]['datedepot'] != data[i+1]['datedepot']:
            j += 1
  
 
    if data:
        grouped_data[j]['datedepot'] = data[len(data)-1]['datedepot']
        grouped_data[j]['total'] += data[len(data)-1]['total']
        grouped_data[j]['timedepot'] = data[len(data)-1]['timedepot']

    
    grouped_list = list(grouped_data.values())  

    
    chart_labels = [item['datedepot'].strftime('%Y-%m-%d') for item in grouped_list]
    chart_data = [item['total'] for item in grouped_list]

   
    total_sum = sum(item['total'] for item in grouped_list)

   
  

    context = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'data': grouped_list,
        'TotalProfit' :total_sum ,
        'nb_items' : nb_items ,
        'profite_perday' : profite_perday,
        'chart_serveur' : chart_serveur,
        'chart_total_vente' : chart_total_vente,
    }

    return context



