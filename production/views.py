# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from production.models import *
from functools import reduce
from django.db.models import Sum
import json

def get_status():
    """
    获取全局状态
    """
    status = Status.objects.all()
    if status:
        status = status[0]
    else:
        # 获取第几期的数据明细
        phase = Phase.objects.all()
        if not phase:
            status = Status.objects.create()
        else:
            phase = Phase.objects.latest('created_at')
            status = Status.objects.create(current_phase=phase)
    return status


def get_last_phase():
    phase_list = Phase.objects.all()
    if len(phase_list) < 2:
        return None
    else:
        return phase_list[1]

@csrf_exempt
def search_by_district(request):
    district_id = request.GET.get("districtId")
    res = { 'district_detail_items': json.dumps(list(DistrictDetail.objects.filter(district_id=district_id).values('id', 'name')),ensure_ascii=False)}
    if res.get('district_detail_items'):
        return JsonResponse(res)

@csrf_exempt
def search_by_category(request):
    category_id = request.GET.get("categoryId")
    res = { 'project_items': json.dumps(list(Project.objects.filter(category_id=category_id).values('id', 'name')), ensure_ascii=False)}
    if res.get('project_items'):
        return JsonResponse(res)

class IndexView(TemplateView):
    template_name = "production/index.html"

    def get_data(self):
        status = get_status()
        return {'status': status}

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class PhaseListView(TemplateView):
    template_name = 'production/phase_list.html'

    def get_data(self):
        phase_list = Phase.objects.all()
        status = get_status()
        return {'phase_list': phase_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(PhaseListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class RecordListView(TemplateView):
    template_name = 'production/record_list.html'

    def get_data(self):
        status = get_status()
        record_list = []
        if status.current_phase:
            record_list = Record.objects.filter(phase=status.current_phase)
        # parameter = Parameter.objects.all()
        # if parameter:
        #     parameter = parameter[0]
        # else:
        #     parameter = Parameter.objects.create(ratio=1.0)
        # return {'record_list': record_list, 'status': status, 'parameter': parameter}
        return { 'record_list': record_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class DistrictListView(TemplateView):
    template_name = 'production/district_list.html'

    def get_data(self):
        district_list = District.objects.all()
        status = get_status()
        return {'district_list': district_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(DistrictListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context



class DistrictDetailListView(TemplateView):
    template_name = 'production/district_detail_list.html'

    def get_data(self):
        district_detail_list = DistrictDetail.objects.all()
        status = get_status()
        return {'district_detail_list': district_detail_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(DistrictDetailListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context



class BigTypeListView(TemplateView):
    template_name = 'production/big_type_list.html'

    def get_data(self):
        big_type_list = BigType.objects.all()
        status = get_status()
        return {'big_type_list': big_type_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(BigTypeListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class CategoryListView(TemplateView):
    template_name = 'production/category_list.html'

    def get_data(self):
        category_list = Category.objects.all()
        status = get_status()
        return {'category_list': category_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class ProjectListView(TemplateView):
    template_name = 'production/project_list.html'

    def get_data(self):
        project_list = Project.objects.all()
        status = get_status()
        return {'project_list': project_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class OrganizationListView(TemplateView):
    template_name = 'production/organization_list.html'

    def get_data(self):
        organization_list = Organization.objects.all()
        status = get_status()
        return {'organization_list': organization_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class MeasurementListView(TemplateView):
    template_name = 'production/measurement_list.html'

    def get_data(self):
        measurement_list = Measurement.objects.all()
        status = get_status()
        return {'measurement_list': measurement_list, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(MeasurementListView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class CreatePhaseView(TemplateView):
    template_name = 'production/create_phase.html'

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('phase_name')
            description = self.request.POST.get('description')
            begin = self.request.POST.get('begin')
            end = self.request.POST.get('end')

            if not name:
                res["msg"] = "请输入月报名称！"
                return JsonResponse(res)

            if not begin:
                res["msg"] = "请输入起始日期！"
                return JsonResponse(res)

            if not end:
                res["msg"] = "请输入结束日期！"
                return JsonResponse(res)

            count = Phase.objects.count()
            data = {
                'number': count + 1,
                'name': name,
                'begin': begin,
                'end': end,
                'description': description
            }
            phase = Phase.objects.create(**data)
            status = get_status()
            status.current_phase = phase
            status.save()

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreatePhaseView, self).get_context_data(**kwargs)
        context.update()
        return context


class CreateRecordView(TemplateView):
    template_name = 'production/create_record.html'


    def get_data(self):
        district_list = District.objects.all()
        # district_detail_list = DistrictDetail.objects.all()
        measurement_list =Measurement.objects.all()
        category_list = Category.objects.all()
        # project_list = Project.objects.all()
        organization_list = Organization.objects.all()
        return {
            'district_list': district_list,
            # 'district_detail_list': district_detail_list,
            'measurement_list': measurement_list,
            'category_list': category_list,
            # 'project_list': project_list,
            'organization_list': organization_list
        }


    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            district_id = self.request.POST.get('district')
            district_detail_id = self.request.POST.get('district_detail')
            organization_id = self.request.POST.get('organization')
            category_id = self.request.POST.get('category')
            project_id = self.request.POST.get('project')
            measurement_id = self.request.POST.get('measurement')
            contract_unit_price = self.request.POST.get('contract_unit_price')
            current_month_project_quantities = self.request.POST.get('current_month_project_quantities')
            current_month_contract_price = self.request.POST.get('current_month_contract_price')
            current_month_project_parameter = self.request.POST.get('current_month_project_parameter')
            remark = self.request.POST.get('remark')

            if not district_id:
                res["msg"] = "请选择区域"
                return JsonResponse(res)

            if not district_detail_id:
                res["msg"] = "请选择区域明细"
                return JsonResponse(res)

            if not organization_id:
                res["msg"] = "请选择单位"
                return JsonResponse(res)

            if not category_id:
                res["msg"] = "请选择工程分类"
                return JsonResponse(res)

            if not project_id:
                res["msg"] = "请选择工程名称"
                return JsonResponse(res)

            if not measurement_id:
                res["msg"] = "请选择计量单位"
                return JsonResponse(res)

            if not contract_unit_price:
                res["msg"] = "请填写合同单价"
                return JsonResponse(res)

            if not current_month_project_quantities:
                res["msg"] = "请填写当月工程量"
                return JsonResponse(res)

            if not current_month_project_parameter:
                res["msg"] = "请填写当月进度完成合同比"
                return JsonResponse(res)

            district = District.objects.get(id=district_id)
            district_detail = DistrictDetail.objects.get(id=district_detail_id)
            organization = Organization.objects.get(id=organization_id)
            category = Category.objects.get(id=category_id)
            project = Project.objects.get(id=project_id)
            measurement = Measurement.objects.get(id=measurement_id)

            status = get_status()
            if not status:
                res["msg"] = "请设置当前月报期数"
                return JsonResponse(res)
            else:
                if not status.current_phase:
                    res["msg"] = "请设置当前月报期数"
                    return JsonResponse(res)

            # record_list = Record.objects.filter(
            #     district=district,
            #     district_detail=district_detail,
            #     organization=organization,
            #     category=category,
            #     project=project,
            #     phase=status.current_phase
            # )
            # if len(record_list) != 0:
            #     res["msg"] = "该条目已存在，请勿重复提交！"
            #     return JsonResponse(res)


            current_month_contract_price = float(contract_unit_price) * float(current_month_project_quantities)
            parameter = Parameter.objects.all()
            if not parameter:
                parameter = Parameter.objects.create(ratio=1.0)
            else:
                parameter = parameter[0]

            current_month_progress_payment = current_month_contract_price * float(current_month_project_parameter)

            last_E, last_F, last_G = 0, 0, 0
            last_phase = get_last_phase()
            if last_phase:
                last_phase_record = Record.objects.filter(
                    district=district,
                    district_detail=district_detail,
                    organization=organization,
                    category=category,
                    project=project,
                    phase = last_phase
                )
                if last_phase_record:
                    last_phase_record = last_phase_record[0]
                    last_E = last_phase_record.accumulative_project_quantities
                    last_F = last_phase_record.accumulative_contract_price
                    last_G = last_phase_record.accumulative_progress_payment

            accumulative_project_quantities = float(current_month_project_quantities) + last_E
            accumulative_contract_price = float(current_month_contract_price) + last_F
            accumulative_progress_payment = float(current_month_progress_payment) + last_G

            # create Record的时候传入bigtype结构
            bigtype=BigType.objects.filter(id=Category.objects.select_related().filter(name=category.name).values('big_type'))[0]

            if not bigtype:
                res["msg"] = "当前项目工程未属于任何大项"
                return JsonResponse(res)

            data = {
                'district': district,
                'district_detail': district_detail,
                'organization': organization,
                'bigtype': bigtype,
                'category': category,
                'project': project,
                'measurement': measurement,
                'contract_unit_price': contract_unit_price,
                'current_month_project_quantities': current_month_project_quantities,
                'current_month_contract_price': current_month_contract_price,
                'current_month_project_parameter': current_month_project_parameter,
                'current_month_progress_payment': current_month_progress_payment,
                'accumulative_project_quantities': accumulative_project_quantities,
                'accumulative_contract_price': accumulative_contract_price,
                'accumulative_progress_payment': accumulative_progress_payment,
                'remark': remark,
                'phase': status.current_phase,
            }

            Record.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateRecordView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class CreateDistrictView(TemplateView):
    template_name = 'production/create_distrct.html'

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('district')
            if not name:
                res["msg"] = "区域名称不能为空！"
                return JsonResponse(res)

            data = {
                'name': name
            }
            District.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateDistrictView, self).get_context_data(**kwargs)
        context.update()
        return context


class CreateDistrictDetailView(TemplateView):
    template_name = 'production/create_district_detail.html'

    def get_data(self):
        district_list = District.objects.all()
        return {'district_list': district_list}

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('district_detail')
            d_id = self.request.POST.get('district_id')
            if not d_id:
                res["msg"] = "请选择所属区域"
                return JsonResponse(res)
            if not name:
                res["msg"] = "区域明细不能为空"
                return JsonResponse(res)
            district = District.objects.get(id=d_id)

            data = {
                'name': name,
                'district': district
            }
            DistrictDetail.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateDistrictDetailView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class CreateProjectView(TemplateView):
    template_name = 'production/create_project.html'

    def get_data(self):
        category_list = Category.objects.all()
        return {'category_list': category_list}

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('project')
            category_id = self.request.POST.get('category_id')
            if not category_id:
                res["msg"] = "请选择工程分类！"
                return JsonResponse(res)

            if not name:
                res["msg"] = "工程名称不能为空！"
                return JsonResponse(res)
            category = Category.objects.get(id=category_id)

            data = {
                'name': name,
                'category': category
            }
            Project.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class CreateBigTypeView(TemplateView):
    template_name = 'production/create_big_type.html'

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('big_type')
            if not name:
                res["msg"] = "工程大类不能为空！"
                return JsonResponse(res)

            data = {
                'name': name
            }
            BigType.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateBigTypeView, self).get_context_data(**kwargs)
        context.update()
        return context


class CreateCategoryView(TemplateView):
    template_name = 'production/create_category.html'


    def get_data(self):
        big_type_list = BigType.objects.all()
        return {'big_type_list': big_type_list}

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('category')
            big_type_id = self.request.POST.get('big_type_id')
            if not big_type_id:
                res["msg"] = "请选择项目类型！"
                return JsonResponse(res)

            if not name:
                res["msg"] = "工程分类不能为空！"
                return JsonResponse(res)
            big_type = BigType.objects.get(id=big_type_id)

            data = {
                'name': name,
                'big_type': big_type
            }
            Category.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateCategoryView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context


class CreateOrganizationView(TemplateView):
    template_name = 'production/create_organization.html'

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('organization')
            if not name:
                res["msg"] = "单位名称不能为空！"
                return JsonResponse(res)
            data = {
                'name': name
            }
            Organization.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateOrganizationView, self).get_context_data(**kwargs)
        context.update()
        return context


class CreateMeasurementView(TemplateView):
    template_name = 'production/create_measurement.html'

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            name = self.request.POST.get('measurement')
            if not name:
                res["msg"] = "计量单位不能为空！"
                return JsonResponse(res)
            data = {
                'name': name
            }
            Measurement.objects.create(**data)

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(CreateMeasurementView, self).get_context_data(**kwargs)
        context.update()
        return context



class EditParameter(TemplateView):
    template_name = 'production/parameter.html'

    def post(self, *args, **kwargs):
        res = {"success": False, "msg": ""}
        try:
            ratio = self.request.POST.get('ratio')
            if not ratio:
                res["msg"] = "比率不能为空！"
                return JsonResponse(res)

            parameter = Parameter.objects.all()
            if not parameter:
                Parameter.objects.create(ratio=ratio)
            else:
                parameter = parameter[0]
                parameter.ratio = ratio
                parameter.save()

            res["success"] = True
            res["msg"] = "提交成功"
            return JsonResponse(res)

        except Exception as e:
            res["msg"] = str(e)
            return JsonResponse(res)

    def get_context_data(self, **kwargs):
        context = super(EditParameter, self).get_context_data(**kwargs)
        context.update()
        return context


@csrf_exempt
def delete_phase(request):

    res = {"success": False, "msg": ""}
    try:
        p_id = request.POST.get('phase_id')
        Phase.objects.get(id=p_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def delete_record(request):

    res = {"success": False, "msg": ""}
    try:
        r_id = request.POST.get('record_id')
        Record.objects.get(id=r_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)

@csrf_exempt
def delete_district(request):

    res = {"success": False, "msg": ""}
    try:
        d_id = request.POST.get('district_id')
        District.objects.get(id=d_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def delete_district_detail(request):

    res = {"success": False, "msg": ""}
    try:
        d_id = request.POST.get('district_detail_id')
        DistrictDetail.objects.get(id=d_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def phase_select(request):
    res = {"success": False, "msg": ""}
    try:
        phase_id = request.POST.get('phase_id')
        status = Status.objects.all()
        phase = Phase.objects.get(id=phase_id)
        if not status:
            Status.objects.create(current_phase=phase)
        else:
            status = status[0]
            status.current_phase = phase
            status.save()

        res["success"] = True
        res["msg"] = "提交成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)



@csrf_exempt
def delete_big_type(request):

    res = {"success": False, "msg": ""}
    try:
        t_id = request.POST.get('big_type_id')
        BigType.objects.get(id=t_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def delete_category(request):

    res = {"success": False, "msg": ""}
    try:
        c_id = request.POST.get('category_id')
        Category.objects.get(id=c_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def delete_project(request):

    res = {"success": False, "msg": ""}
    try:
        p_id = request.POST.get('project_id')
        Project.objects.get(id=p_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def delete_organization(request):

    res = {"success": False, "msg": ""}
    try:
        o_id = request.POST.get('organization_id')
        Organization.objects.get(id=o_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def delete_measurement(request):

    res = {"success": False, "msg": ""}
    try:
        m_id = request.POST.get('measurement_id')
        Measurement.objects.get(id=m_id).delete()
        res["success"] = True
        res["msg"] = "删除成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


@csrf_exempt
def caculate_by_category(request):
    res = {"success": False, "msg": ""}
    try:
        status = get_status()
        phase = status.current_phase
        if not phase:
            res["msg"] = "请设置月报期数"
            return JsonResponse(res)

        bigtype_list = BigType.objects.all()
        category_list = Category.objects.all()
        organization_list = Organization.objects.all()
        record_list = Record.objects.filter(phase=phase)


        for bigtype_item in bigtype_list:
            for category_item in category_list:
                for organization_item in organization_list:
                    current_month_contract_price = record_list.filter(bigtype_id=bigtype_item.id).filter(category_id=category_item.id).filter(organization_id=organization_item.id).aggregate(Sum('current_month_contract_price'))
                    current_month_progress_payment = record_list.filter(bigtype_id=bigtype_item.id).filter(category_id=category_item.id).filter(organization_id=organization_item.id).aggregate(Sum('current_month_progress_payment'))
                    accumulative_contract_price = record_list.filter(bigtype_id=bigtype_item.id).filter(category_id=category_item.id).filter(organization_id=organization_item.id).aggregate(Sum('accumulative_contract_price'))
                    accumulative_progress_payment = record_list.filter(bigtype_id=bigtype_item.id).filter(category_id=category_item.id).filter(organization_id=organization_item.id).aggregate(Sum('accumulative_progress_payment'))
                    if current_month_contract_price.get('current_month_contract_price__sum'):
                        CategoryRecord.objects.create(
                            bigtype=BigType.objects.filter(id=bigtype_item.id)[0],
                            category=Category.objects.filter(id=category_item.id)[0],
                            organization=Organization.objects.filter(id=organization_item.id)[0],
                            current_month_contract_price=current_month_contract_price.get('current_month_contract_price__sum'),
                            current_month_progress_payment=current_month_progress_payment.get('current_month_progress_payment__sum'),
                            accumulative_contract_price=accumulative_contract_price.get('accumulative_contract_price__sum'),
                            accumulative_progress_payment=accumulative_progress_payment.get('accumulative_progress_payment__sum'),
                            phase=phase)
                    else:
                        continue
        res["success"] = True
        res["msg"] = "汇总计算成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


class RecordListCategoryView(TemplateView):
    template_name = 'production/caculate_by_category.html'
    def get_data(self):
        bigtypes = BigType.objects.all()
        status = get_status()
        # eg:
        #     {
        #      "bigtype_a":
        #         {
        #           "current_month_contract_price": 1000,
        #           "current_month_progress_payment": 500,
        #           "accumulative_contract_price": 1000,
        #           "accumulative_progress_payment": 500,
        #           "category_list":
        #           {
        #               "category_a": "categoryrecord_a",
        #               "category_b": "categoryrecord_b"
        #           },
        #         },
        #      "bigtype_b":
        #         {
        #           "current_month_contract_price": 1000,
        #           "current_month_progress_payment": 500,
        #           "accumulative_contract_price": 1000,
        #           "accumulative_progress_payment": 500
        #           "category_list":
        #           {
        #               "category_c": "categoryrecord_c"
        #           },
        #         }
        #     }
        categoryrecord_list = {}
        for bigtype in bigtypes:
            current_month_contract_price = 0
            current_month_progress_payment = 0
            accumulative_contract_price = 0
            accumulative_progress_payment = 0
            category_list = {}
            for category in bigtype.category_bigtype.all():
                try:
                    categoryrecord = category.categoryrecord_category.all()[0]
                except IndexError:
                    continue
                category_list.update({
                    category.name: categoryrecord
                })
                current_month_contract_price = categoryrecord.current_month_contract_price + current_month_contract_price
                current_month_progress_payment = categoryrecord.current_month_progress_payment + current_month_progress_payment
                accumulative_contract_price = categoryrecord.accumulative_contract_price + accumulative_contract_price
                accumulative_progress_payment = categoryrecord.accumulative_progress_payment + accumulative_progress_payment
            categoryrecord_list.update(
                {
                    bigtype.name:
                    {
                        "current_month_contract_price": current_month_contract_price,
                        "current_month_progress_payment" : current_month_progress_payment,
                        "accumulative_contract_price" : accumulative_contract_price,
                        "accumulative_progress_payment" : accumulative_progress_payment,
                        "category_list" : category_list
                    }
                })

        return {'categoryrecord_list': categoryrecord_list, 'status': status}


    def get_context_data(self, **kwargs):
        context = super(RecordListCategoryView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context




@csrf_exempt
def caculate_by_district_detail(request):
    # 根据区域明细汇总
    res = {"success": False, "msg": ""}
    try:
        status = get_status()
        phase = status.current_phase
        if not phase:
            res["msg"] = "请设置月报期数"
            return JsonResponse(res)

        record_list = Record.objects.filter(phase=phase)
        district_detail_list = DistrictDetail.objects.all()
        for district_detail_item in district_detail_list:
            current_month_contract_price = record_list.filter(district_detail_id=district_detail_item.id).aggregate(Sum('current_month_contract_price'))
            current_month_progress_payment = record_list.filter(district_detail_id=district_detail_item.id).aggregate(Sum('current_month_progress_payment'))
            accumulative_contract_price  = record_list.filter(district_detail_id=district_detail_item.id).aggregate(Sum('accumulative_contract_price'))
            accumulative_progress_payment = record_list.filter(district_detail_id=district_detail_item.id).aggregate(Sum('accumulative_progress_payment'))
            if current_month_contract_price.get('current_month_contract_price__sum'):
                DistrictDetailRecord.objects.create(
                    district=District.objects.filter(id=district_detail_item.district_id)[0],
                    district_detail=DistrictDetail.objects.filter(id=district_detail_item.id)[0],
                    current_month_contract_price=current_month_contract_price.get('current_month_contract_price__sum'),
                    current_month_progress_payment=current_month_progress_payment.get('current_month_progress_payment__sum'),
                    accumulative_contract_price=accumulative_contract_price.get('accumulative_contract_price__sum'),
                    accumulative_progress_payment=accumulative_progress_payment.get('accumulative_progress_payment__sum'),
                    phase=phase
                )
            else:
                continue

                #
                # if not organization:
                #     continue
                #
                # ddr_list = DistrictDetailRecord.objects.filter(
                #     district=district,
                #     district_detail=district_detail,
                #     organization=organization,
                #     phase=phase
                # )
                # if len(ddr_list) != 0:
                #     continue

        res["success"] = True
        res["msg"] = "汇总计算成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


class RecordListDistrictDetailView(TemplateView):
    template_name = 'production/caculate_by_district_detail.html'
    def get_data(self):
        district_detail_record_list = DistrictDetailRecord.objects.all()
        status = get_status()
        return {'district_detail_record_list': district_detail_record_list, 'status': status}


    def get_context_data(self, **kwargs):
        context = super(RecordListDistrictDetailView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context



@csrf_exempt
def caculate_by_district(request):
    res = {"success": False, "msg": ""}
    try:
        bigtype_list = BigType.objects.all()
        district_list = District.objects.all()
        organization_list = Organization.objects.all()

        status = get_status()
        phase = status.current_phase
        if not phase:
            res["msg"] = "请设置月报期数"
            return JsonResponse(res)

        record_list = Record.objects.filter(phase=phase)

        for district_item in district_list:
            for bigtype_item in bigtype_list:
                for organization_item in organization_list:
                    current_month_contract_price = record_list.filter(district_id=district_item.id).filter(bigtype_id=bigtype_item.id).filter(organization_id=organization_item.id).aggregate(Sum('current_month_contract_price'))
                    current_month_progress_payment = record_list.filter(district_id=district_item.id).filter(bigtype_id=bigtype_item.id).filter(organization_id=organization_item.id).aggregate(Sum('current_month_progress_payment'))
                    accumulative_contract_price = record_list.filter(district_id=district_item.id).filter(bigtype_id=bigtype_item.id).filter(organization_id=organization_item.id).aggregate(Sum('accumulative_contract_price'))
                    accumulative_progress_payment = record_list.filter(district_id=district_item.id).filter(bigtype_id=bigtype_item.id).filter(organization_id=organization_item.id).aggregate(Sum('accumulative_progress_payment'))
                    if current_month_contract_price.get('current_month_contract_price__sum'):
                        DistrictRecord.objects.create(
                            district=District.objects.filter(id=district_item.id)[0],
                            bigtype=BigType.objects.filter(id=bigtype_item.id)[0],
                            organization=Organization.objects.filter(id=organization_item.id)[0],
                            current_month_contract_price=current_month_contract_price.get('current_month_contract_price__sum'),
                            current_month_progress_payment=current_month_progress_payment.get('current_month_progress_payment__sum'),
                            accumulative_contract_price=accumulative_contract_price.get('accumulative_contract_price__sum'),
                            accumulative_progress_payment=accumulative_progress_payment.get('accumulative_progress_payment__sum'),
                            phase=phase)
                    else:
                        continue

        res["success"] = True
        res["msg"] = "汇总计算成功"
        return JsonResponse(res)

    except Exception as e:
        res["msg"] = str(e)
        return JsonResponse(res)


class RecordListDistrictView(TemplateView):
    template_name = 'production/caculate_by_district.html'
    def get_data(self):
        status = get_status()
        phase = status.current_phase
        district_record_list = DistrictRecord.objects.filter(phase=phase)
        districts = district_record_list
        district_list = {
            d.district.name: list(d.district.records.filter(phase=phase))
            for d in districts
        }
        # example like blow block:
        # """
        # district_list = {}
        # for d in district:
        #     dl = district_list[d.name] = []
        #     for record in d.records.all():
        #         dl.append(record)
        # print(district_list)
        # """

        return {
                'district_list': district_list,
                'status': status
                }


    def get_context_data(self, **kwargs):
        context = super(RecordListDistrictView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context
