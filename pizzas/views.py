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
     
    return HttpResponse(template.render(context,'pizzas/pizza.html', request))
    
         

def toppings(request,topping_id,pizza_id):
    toppings = Topping.objects.get(id=topping_id)
    pizza = Pizza.objects.get(id=pizza_id)

    context = {'toppings':toppings,'pizza':pizza}

    return render(request, 'pizzas/pizza.html', context)

def comments (request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method != 'POST':
        form = CommentForm()

    else:
        form = CommentForm(data=request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.pizzas = comment
            new_comment.save()
            return redirect('pizzas:pizza_menu', id= comment_id)
    context = {'form':form, 'comment': comment}
    return render(request, 'pizzas/new_comment.html', context)
