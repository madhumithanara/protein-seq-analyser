from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from . import models
from . import forms

# Create your views here.
def predict(request):
    if request.method == 'POST':
        form = forms.ProteinSequenceForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('multiprotseqalign:result', id=obj.id)
    else:
        form = forms.ProteinSequenceForm
    return render(request, 'multiprotseqalign/predict.html', {'form':form})

def result(request,id):
    try:
        id=int(id)
    except:
        message = 'Invalid link entered. Please check your URL again.'
        return render(request, 'multiprotseqalign/message.html', {'message':message})
    try:
        obj = models.ProteinSequence.objects.get(id=id)
    except:
        message = 'Requested object not found. Please check your URL again.'
        return render(request, 'multiprotseqalign/message.html', {'message':message})
    if obj.completed:
        try:
            with open(f'../../VGST_Scripts/1-MSA/Output/{id}', 'r') as f:
                content = f.read()
        except:
            message = "Couldn't process your input. Please check your input sequence again."
            return render(request, 'multiprotseqalign/message.html', {'message':message})    
        return render(request, 'multiprotseqalign/result.html', {'result':content})    
    else:
        DOMAIN_NAME = 'localhost:8000'
        message = f'Your entered input sequence is still under process. Please come back later to the same url {DOMAIN_NAME}{request.get_full_path()}'
        return render(request, 'multiprotseqalign/message.html', {'message':message})
