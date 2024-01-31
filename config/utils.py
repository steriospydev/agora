from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin


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


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseListView(LoginRequiredMixin, ListView):
    template_name = ''
    context_object_name = 'objs'
    paginate_by = 8
    form_class = None
    success_message = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class() if self.form_class else None
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if self.success_message:
                messages.success(request, self.success_message)
        return self.get(request, *args, **kwargs)
    
class BaseDeleteView(View):
    model = None
    redirect_url = None
    success_message = None

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        obj.delete()
        if self.success_message:
            messages.success(request, self.success_message.format(obj))
        return redirect(self.redirect_url)