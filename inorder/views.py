import datetime
import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from common.models import Inorder, User, InorderClothes, Customer

from inorder.forms import InorderForm, InorderClothesForm, EditmoreForm


def list(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Inorder.objects.all()
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result
    }
    return render(request, 'inorder/index.html', context)


def add(request):
    if request.method == "POST":
        inorder_form = InorderForm(request.POST)
        if inorder_form.is_valid():
            costomer = inorder_form.cleaned_data['customer']
            uid = request.session.get('user_id')
            user = User.objects.get(id=uid)
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            code = 'IN' + now + str(random.randint(10000, 99999))
            new_inorder = Inorder.objects.create(code=code,
                                                 customer=costomer,
                                                 user=user)
            context = {
                'id': new_inorder.id
            }
            messages.add_message(request, messages.SUCCESS, '添加成功')
            return redirect(reverse('inorder:detail', args={new_inorder.id}))

        else:
            context = {
                'inorder_form': inorder_form
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inorder/add.html', context)
    else:
        inorder_form = InorderForm()
        context = {
            'inorder_form': inorder_form
        }
        return render(request, 'inorder/add.html', context)


def search(request):
    object = Inorder.objects
    qs = object.values()
    id = request.POST.get('id')
    code = request.POST.get('code')
    customer_name = request.POST.get('customer_name')
    user_name = request.POST.get('user_name')
    if id:
        qs = object.filter(id=id)
    if code:
        qs = object.filter(code=code)
    if customer_name:
        customer = Customer.objects.get(name=customer_name)
        qs = object.filter(customer_id=customer.id)
    if user_name:
        user = User.objects.get(name=user_name)
        qs = object.filter(user_id=user.id)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result
    }
    messages.add_message(request, messages.SUCCESS, '查询成功')
    return render(request, 'inorder/index.html', context)


def update(request, inorder_id):
    inorder = Inorder.objects.get(id=inorder_id)
    qs = InorderClothes.objects.filter(inorder_id=inorder_id)

    if request.method == "POST":
        inorder_form = InorderForm(request.POST)
        if inorder_form.is_valid():
            customer = inorder_form.cleaned_data['customer']

            if customer:
                inorder.customer = customer

            inorder.save()
            context = {
                'inorder_id': inorder_id
            }
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect(reverse('inorder:index'))
        else:
            context = {
                'inorder_form': inorder_form,
                'qs': qs
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inorder/edit.html', context)
    else:
        inorder_form = InorderForm({'id': inorder.id,
                                    'code': inorder.code,
                                    'customer': inorder.customer,
                                    'user': inorder.user,
                                    'create_time': inorder.create_time})
        context = {
            'inorder_form': inorder_form,
            'inorder_id': inorder_id,
            'qs': qs
        }
        return render(request, 'inorder/edit.html', context)


def delete(request, inorder_id):
    qs = InorderClothes.objects.filter(inorder_id=inorder_id)
    if qs:
        messages.add_message(request, messages.WARNING, '删除失败，请先删除该订单下的商品')
        return redirect(reverse('inorder:detail', args={inorder_id}))
    inorder = Inorder.objects.get(id=inorder_id)
    inorder.delete()
    messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('inorder:index'))


def detail(request, inorder_id):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs1 = Inorder.objects.filter(id=inorder_id)
    qs2 = InorderClothes.objects.filter(inorder_id=inorder_id)
    sum = 0
    for foo in qs2:
        sum += foo.clothes.price * foo.amount
    context = {
        'qs1': qs1,
        'qs2': qs2,
        'sum': sum,
        'inorder_id': inorder_id
    }
    return render(request, 'inorder/detail.html', context)


def addmore(request, inorder_id):
    if request.method == "POST":
        inorderclothes_form = InorderClothesForm(request.POST)
        if inorderclothes_form.is_valid():
            clothes = inorderclothes_form.cleaned_data['clothes']
            amount = inorderclothes_form.cleaned_data['amount']

            with transaction.atomic():  # 事务
                new_inorderclothes = InorderClothes.objects.create(clothes=clothes,
                                                                   inorder_id=inorder_id,
                                                                   amount=amount)
                # 入库增加库存
                clothes.stock += amount
                clothes.save()

            context = {
                'id': new_inorderclothes.id
            }
            messages.add_message(request, messages.SUCCESS, '添加成功')
            return redirect(reverse('inorder:detail', args={inorder_id}))

        else:
            context = {
                'inorderclothes_form': inorderclothes_form,
                'inorder_id': inorder_id
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inorder/addmore.html', context)
    else:
        inorderclothes_form = InorderClothesForm()
        context = {
            'inorderclothes_form': inorderclothes_form,
            'inorder_id': inorder_id
        }
        return render(request, 'inorder/addmore.html', context)


def editmore(request, inorder_id, inorderclothes_id):
    inorderclothes = InorderClothes.objects.get(id=inorderclothes_id)

    if request.method == "POST":
        editmore_form = EditmoreForm(request.POST)
        if editmore_form.is_valid():
            clothes = editmore_form.cleaned_data['clothes']
            amount = editmore_form.cleaned_data['amount']

            if amount:
                with transaction.atomic():
                    add_amount = amount - inorderclothes.amount
                    inorderclothes.amount = amount
                    inorderclothes.clothes.stock += add_amount
                    inorderclothes.save()
                    inorderclothes.clothes.save()
            context = {
                'inorderclothes_id': inorderclothes_id
            }
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect(reverse('inorder:detail', args={inorder_id}))
        else:
            context = {
                'editmore_form': editmore_form,
                'inorder_id': inorder_id,
                'inorderclothes_id': inorderclothes_id
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inorder/editmore.html', context)
    else:
        editmore_form = EditmoreForm({'clothes': inorderclothes.clothes,
                                      'amount': inorderclothes.amount})
        context = {
            'editmore_form': editmore_form,
            'inorder_id': inorder_id,
            'inorderclothes_id': inorderclothes_id,
        }
        return render(request, 'inorder/editmore.html', context)


def deletemore(request, inorder_id, inorderclothes_id):
    inorderclothes = InorderClothes.objects.get(id=inorderclothes_id)
    with transaction.atomic():
        inorderclothes.delete()
        inorderclothes.clothes.stock -= inorderclothes.amount
        inorderclothes.clothes.save()
    messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('inorder:detail', args={inorder_id}))
