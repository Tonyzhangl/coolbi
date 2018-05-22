from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


class District(Model):
    """
    项目区域
    """
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class DistrictDetail(Model):
    """
    项目区域明细
    """
    name = models.CharField(max_length=512)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class BigType(Model):
    """
    工程大类
    """
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Category(Model):
    """
    工程分类，隶属于工程大类
    """
    name = models.CharField(max_length=512)
    # 通过主键来查找主键下由多少个副键，eg: BigType 下对应的 Category记录
    big_type = models.ForeignKey(BigType, related_name='category_bigtype', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Project(Model):
    """
    自定义工程名称, 隶属于工程分类
    """
    name = models.CharField(max_length=512)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Organization(Model):
    """
    单位名称
    """
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Measurement(Model):
    """
    计量单位
    """
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Phase(Model):
    """
    第几期
    """
    number = models.IntegerField() #从1递增
    name = models.CharField(max_length=64, blank=True, null=True)
    begin = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Record(Model):
    """
    项目区域，项目区域明细，序号，工程大项，工程分类，工程名称, 单位名称，计量单位，合同单价A，当月工程量B，当月合同价款C，当月进度款D，
    累计工程量E，累计合同价款，累计进度款，备注
    """
    district = models.ForeignKey(District, related_name='record_district', on_delete=models.CASCADE)
    district_detail = models.ForeignKey(DistrictDetail, on_delete=models.CASCADE, blank=True, null=True)
    number = models.CharField(max_length=64, blank=True, null=True)
    bigtype = models.ForeignKey(BigType, on_delete=models.CASCADE) #工程大项
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    contract_unit_price = models.FloatField(blank=True, null=True)
    current_month_project_quantities = models.FloatField(blank=True, null=True)
    current_month_project_parameter = models.FloatField(blank=True, null=True)
    current_month_contract_price = models.FloatField(blank=True, null=True)
    current_month_progress_payment = models.FloatField(blank=True, null=True)
    accumulative_project_quantities = models.FloatField(blank=True, null=True)
    accumulative_contract_price = models.FloatField(blank=True, null=True)
    accumulative_progress_payment = models.FloatField(blank=True, null=True)
    remark = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE) #第几期/几月份的数据

    class Meta:
        ordering = ['-created_at', '-updated_at']


class CategoryRecord(Model):
    # district = models.ForeignKey(District, on_delete=models.CASCADE)
    # district_detail = models.ForeignKey(DistrictDetail, on_delete=models.CASCADE, blank=True, null=True)
    bigtype = models.ForeignKey(BigType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='categoryrecord_category', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    current_month_contract_price = models.FloatField(blank=True, null=True) #C
    current_month_progress_payment = models.FloatField(blank=True, null=True) #D
    accumulative_contract_price = models.FloatField(blank=True, null=True) #F
    accumulative_progress_payment = models.FloatField(blank=True, null=True) #G
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE) #第几期/几月份的数据

    class Meta:
        ordering = ['-created_at']


class DistrictDetailRecord(Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    district_detail = models.ForeignKey(DistrictDetail, on_delete=models.CASCADE, blank=True, null=True)
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    current_month_contract_price = models.FloatField(blank=True, null=True) #C
    current_month_progress_payment = models.FloatField(blank=True, null=True) #D
    accumulative_contract_price = models.FloatField(blank=True, null=True) #F
    accumulative_progress_payment = models.FloatField(blank=True, null=True) #G
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE) #第几期/几月份的数据

    class Meta:
        ordering = ['-created_at']


class DistrictRecord(Model):
    district = models.ForeignKey(District, related_name='records', on_delete=models.CASCADE)
    # district_detail = models.ForeignKey(DistrictDetail, on_delete=models.CASCADE)
    bigtype = models.ForeignKey(BigType, on_delete=models.CASCADE) #工程大项
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    current_month_contract_price = models.FloatField(blank=True, null=True) #C
    current_month_progress_payment = models.FloatField(blank=True, null=True) #D
    accumulative_contract_price = models.FloatField(blank=True, null=True) #F
    accumulative_progress_payment = models.FloatField(blank=True, null=True) #G
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE) #第几期/几月份的数据

    class Meta:
        ordering = ['-created_at']


class Status(Model):
    """
    系统全局状态
    """
    current_phase = models.ForeignKey(Phase, on_delete=models.CASCADE, blank=True, null=True) #当前期数



class Parameter(Model):
    """
    计算所用参数
    """
    ratio = models.FloatField(default=1.00, blank=True, null=True)
