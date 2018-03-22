# --*-- coding: utf-8 --*--
from django.contrib.auth.decorators import login_required

__author__ = 'nolan'

from django.conf.urls import url
from production.views import *


urlpatterns = [
    url(r'^$',  login_required(IndexView.as_view(), login_url='/login/'), name="index"),
    url(r'^phase/list/$', login_required(PhaseListView.as_view(), login_url='/login/'), name="phase_list"),
    url(r'^record/list/$',  login_required(RecordListView.as_view(), login_url='/login/'), name="record_list"),
    url(r'^district/list/$',  login_required(DistrictListView.as_view(), login_url='/login/'), name="district_list"),
    url(r'^district_detail/list/$',  login_required(DistrictDetailListView.as_view(), login_url='/login/'), name="district_detail_list"),
    url(r'^big_type/list/$',  login_required(BigTypeListView.as_view(), login_url='/login/'), name="big_type_list"),
    url(r'^category/list/$',  login_required(CategoryListView.as_view(), login_url='/login/'), name="category_list"),
    url(r'^project/list/$',  login_required(ProjectListView.as_view(), login_url='/login/'), name="project_list"),
    url(r'^organization/list/$',  login_required(OrganizationListView.as_view(), login_url='/login/'), name="organization_list"),
    url(r'^measurement/list/$',  login_required(MeasurementListView.as_view(), login_url='/login/'), name="measurement_list"),

    url(r'^phase/select/$', login_required(phase_select, login_url='/login/'), name="phase_select"),

    url(r'^create/phase/$', login_required(CreatePhaseView.as_view(), login_url='/login/'), name="create_phase"),
    url(r'^create/record/$',  login_required(CreateRecordView.as_view(), login_url='/login/'), name="create_record"),
    url(r'^create/district/$',  login_required(CreateDistrictView.as_view(), login_url='/login/'), name="create_district"),
    url(r'^create/district_detail/$',  login_required(CreateDistrictDetailView.as_view(), login_url='/login/'), name="create_district_detail"),
    url(r'^create/big_type/$',  login_required(CreateBigTypeView.as_view(), login_url='/login/'), name="create_big_type"),
    url(r'^create/category/$',  login_required(CreateCategoryView.as_view(), login_url='/login/'), name="create_category"),
    url(r'^create/project/$',  login_required(CreateProjectView.as_view(), login_url='/login/'), name="create_project"),
    url(r'^create/organization/$',  login_required(CreateOrganizationView.as_view(), login_url='/login/'), name="create_organization"),
    url(r'^create/measurement/$',  login_required(CreateMeasurementView.as_view(), login_url='/login/'), name="create_measurement"),
    url(r'^edit/parameter/$',  login_required(EditParameter.as_view(), login_url='/login/'), name="edit_parameter"),


    url(r'^delete/phase/$', login_required(delete_phase, login_url='/login/'), name="delete_phase"),
    url(r'^delete/record/$',  login_required(delete_record, login_url='/login/'), name="delete_record"),
    url(r'^delete/district/$',  login_required(delete_district, login_url='/login/'), name="delete_district"),
    url(r'^delete/district_detail/$',  login_required(delete_district_detail, login_url='/login/'), name="delete_district_detail"),
    url(r'^delete/big_type/$',  login_required(delete_big_type, login_url='/login/'), name="delete_big_type"),
    url(r'^delete/category/$',  login_required(delete_category, login_url='/login/'), name="delete_category"),
    url(r'^delete/project/$',  login_required(delete_project, login_url='/login/'), name="delete_project"),
    url(r'^delete/organization/$',  login_required(delete_organization, login_url='/login/'), name="delete_organization"),
    url(r'^delete/measurement/$',  login_required(delete_measurement, login_url='/login/'), name="delete_measurement"),


    url(r'^caculate/by/category/$',  login_required(caculate_by_category, login_url='/login/'), name="caculate_by_category"),
    url(r'^record/list/category/$',  login_required(RecordListCategoryView.as_view(), login_url='/login/'), name="record_list_category"),

    url(r'^caculate/by/district_detail/$',  login_required(caculate_by_district_detail, login_url='/login/'), name="caculate_by_district_detail"),
    url(r'^record/list/district_detail/$',  login_required(RecordListDistrictDetailView.as_view(), login_url='/login/'), name="record_list_district_detail"),

    url(r'^caculate/by/district/$',  login_required(caculate_by_district, login_url='/login/'), name="caculate_by_district"),
    url(r'^record/list/district/$',  login_required(RecordListDistrictView.as_view(), login_url='/login/'), name="record_list_district"),



]
