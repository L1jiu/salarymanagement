from django.views.decorators.csrf import csrf_exempt
from .models import Positiontable
from .forms import PositionForm  # 确保已定义PositionForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect  # 使用csrf_protect代替csrf_exempt
from .models import Employeetable
from .models import Employeepositiontable
from .forms import EmployeePositionForm
import logging

logger = logging.getLogger(__name__)


@csrf_protect  # 确保所有的POST请求都有有效的CSRF token
def employee_management(request: HttpRequest) -> JsonResponse | HttpResponse:
    logger.debug(f"Received POST data: {dict(request.POST)}")
    if request.method == 'POST':
        try:
            action = request.POST.get('action', '').strip().lower()

            if action == 'delete':  # 删除操作
                employee_id = request.POST.get('employeeid')
                if not employee_id or not employee_id.isdigit():
                    return JsonResponse({'status': 'error', 'errors': 'Valid Employee ID is required for deletion.'}, status=400)

                employee = get_object_or_404(Employeetable, employeeid=int(employee_id))
                employee.delete()
                return JsonResponse({'status': 'success'})

            elif action == 'update':  # 更新操作
                employee_id = request.POST.get('employeeid')
                if not employee_id or not employee_id.isdigit():
                    return JsonResponse({'status': 'error', 'errors': 'Valid Employee ID is required for update.'}, status=400)

                employee = get_object_or_404(Employeetable, employeeid=int(employee_id))

                name = request.POST.get('name', '').strip()
                gender = request.POST.get('gender', '').strip()
                phonenumber = request.POST.get('phonenumber', '').strip()

                if any([name, gender, phonenumber]):  # 如果有任意一个字段被提供，则进行更新
                    if name:
                        employee.name = name
                    if gender:
                        employee.gender = gender
                    if phonenumber:
                        employee.phonenumber = phonenumber

                    employee.save()
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'errors': 'At least one field must be provided for update.'}, status=400)

            elif action == 'add':  # 新增操作
                name = request.POST.get('name', '').strip()
                gender = request.POST.get('gender', '').strip()
                phonenumber = request.POST.get('phonenumber', '').strip()

                if not all([name, gender, phonenumber]):
                    return JsonResponse(
                        {'status': 'error', 'errors': 'All fields are required for adding a new employee.'}, status=400)

                new_employee = Employeetable.objects.create(
                    name=name,
                    gender=gender,
                    phonenumber=phonenumber
                )
                return JsonResponse({'status': 'success', 'employeeid': new_employee.employeeid})

            else:
                return JsonResponse({'status': 'error', 'errors': 'Invalid action.'}, status=400)

        except Exception as e:
            logger.error(f"An error occurred during employee management: {e}")
            return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

    else:
        employees = Employeetable.objects.all()
        context = {'employees': employees, 'view_type': 'employees'}
        return render(request, 'employee_management.html', context)


@csrf_exempt  # 注意：仅用于测试，请确保生产环境中正确配置CSRF保护
def position_management(request):
    if request.method == 'POST':
        action = request.POST.get('action', '').strip().lower()

        if action == 'delete':  # 删除操作
            positionname = request.POST.get('positionname')
            if not positionname:
                return JsonResponse({'status': 'error', 'errors': 'Position name is required for deletion.'},
                                    status=400)

            try:
                position = get_object_or_404(Positiontable, positionname=positionname)
                position.delete()
                return JsonResponse({'status': 'success'})
            except Exception as e:
                logger.error(f"An error occurred during position deletion: {e}")
                return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

        else:  # 添加或更新操作
            form = PositionForm(request.POST)

            if not form.is_valid():
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

            try:
                if action == 'update':  # 更新操作
                    positionname = form.cleaned_data.get('positionname')
                    basesalary = form.cleaned_data.get('basesalary')

                    position = get_object_or_404(Positiontable, positionname=positionname)
                    # 只更新提供的非空字段
                    if basesalary is not None:
                        position.basesalary = basesalary

                    position.save()
                    return JsonResponse({'status': 'success'})

                else:  # 添加操作
                    # 检查所有字段是否都有值（假设PositionForm已经做了这个检查）
                    new_position = form.save()  # 使用form保存新的职位信息
                    return JsonResponse({'status': 'success', 'new_position_name': new_position.positionname})

            except Exception as e:
                logger.error(f"An error occurred during position management: {e}")
                return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

    else:
        positions = Positiontable.objects.all()
        context = {'positions': positions, 'view_type': 'positions'}
        return render(request, 'position_management.html', context)


@csrf_protect  # 确保所有的POST请求都有有效的CSRF token
def employee_position_management(request):
    if request.method == 'POST':
        action = request.POST.get('action', '').strip().lower()
        form = EmployeePositionForm(request.POST)

        try:
            if action == 'delete':  # 删除操作
                employee_id = request.POST.get('employeeid')
                if not employee_id or not employee_id.isdigit():
                    return JsonResponse({'status': 'error', 'errors': 'Valid Employee ID is required for deletion.'},
                                        status=400)

                employeeposition = get_object_or_404(Employeepositiontable, employeeid__employeeid=int(employee_id))
                employeeposition.delete()
                return JsonResponse({'status': 'success'})

            elif action in ['update', 'add']:
                if form.is_valid():
                    employee_id = form.cleaned_data.get('employeeid')
                    position_name = form.cleaned_data.get('positionname')

                    if action == 'update' and employee_id:
                        employeeposition = get_object_or_404(Employeepositiontable, employeeid=employee_id)
                        employeeposition.positionname = position_name
                        employeeposition.save()
                    elif action == 'add':
                        employeeposition = form.save()

                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

            else:
                return JsonResponse({'status': 'error', 'errors': 'Invalid action.'}, status=400)

        except Exception as e:
            logger.error(f"An error occurred during employee position management: {e}")
            return JsonResponse({'status': 'error', 'errors': str(e)}, status=500)

    else:  # GET request
        employees = Employeetable.objects.all()
        context = {'employees': employees, 'form': EmployeePositionForm(), 'view_type': 'positions'}
        return render(request, 'employee_position_management.html', context)
