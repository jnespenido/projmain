from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Equipment
from .forms import EquipmentForm
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        equipment = Equipment.objects.filter(name__icontains=query) | Equipment.objects.filter(condition__icontains=query)
    else:
        equipment = Equipment.objects.all()
    return render(request, 'inventory/home.html', {'equipment': equipment})

@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EquipmentForm()
    return render(request, 'inventory/add_equipment.html', {'form': form})

@login_required
def edit_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'inventory/edit_equipment.html', {'form': form})

@login_required
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optional: auto-login after register
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inventory/register.html', {'form': form})

@login_required
def export_pdf(request):
    equipment = Equipment.objects.all()
    template_path = 'inventory/export_pdf.html'
    context = {'equipment': equipment}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response
