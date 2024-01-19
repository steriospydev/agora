from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect


def create_instance(request, form_class,
                    success_message, template_name):
    # TO BE DELETED
    context = {}
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
    else:
        form = form_class()
    context['form'] = form
    return render(request, template_name, context)




# Create your models here.

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True