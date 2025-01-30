from django.shortcuts import render

def gym_rules(request):
    return render(request, 'facilities/rules.html')