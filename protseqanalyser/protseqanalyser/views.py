from django.shortcuts import render
from django.http import HttpResponse

visitors = 0

# Create your views here.
def home(request):
        global visitors

        request.session.set_expiry(0) #Session ends when the browser is closed
        
        if request.session.get('has_visited') == None:
                visitors+=1
                request.session['has_visited'] = True

        context = {"visitors": visitors}
        return render(request,'home.html',context)
