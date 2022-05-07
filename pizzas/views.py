from .forms import CommentForm
from django.shortcuts import render, redirect
from .models import Pizza, Topping, Comment
from django.http import HttpResponse
from django.template import loader
from .forms import CommentForm

# Create your views here.

def index(request):
    return render(request, 'pizzas/index.html')

def pizza_options(request):
    pizza_options = Pizza.objects.filter().order_by()

    context = {'pizza_options':pizza_options}

    return render(request,'pizzas/pizza_options.html',context)


def pizza(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.all()

    context = {'toppings':toppings}
    template = loader.get_template('pizzas/pizza.html')
     
    return render(request, 'pizzas/pizza.html', context)
    
         

def toppings(request,topping_id,pizza_id):
    toppings = Topping.objects.get(id=topping_id)
    pizza = Pizza.objects.get(id=pizza_id)

    context = {'toppings':toppings,'pizza':pizza}

    return render(request, 'pizzas/pizza.html', context)

def comments (request):

    if request.method != 'POST':
        form = CommentForm()

    else:
        form = CommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            comment = Comment.objects.get()
            return redirect('pizzas:pizza_options')
    context = {'form':form, 'comments':comments}
    return render(request, 'pizzas/comment.html', context)
