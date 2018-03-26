# CoolBI
CoolBI  system,devlopmented by django 1.11.3

# Requirements
## python libs

Django==1.11.3
mysqlclient==1.3.12
Pillow==5.0.0
pytz==2018.3

## db
mysql 5.7.21

## 20180323 完成内容
- models 中对表 DistrictRecord 增加了 category 字段，后期汇总需要
- record_list.html 中增加 /caculate/by/district/ 请求的处理，但是这个汇总结果还需调试，
- 在 caculate_by_district.html 增加 gather-submit 按钮，后期可以根据区域来切换显示汇总结果

## 20180325 完成内容
- models 表还需要做进一步细化
- views 中 caculate_by_district.py 通过现有表的 for 循环迭代来生成 production_distictrecord 操作太繁琐，应该通过ORM的高级过滤操作结合queryset内置操作函数来进行数据汇总。https://code.ziqiangxuetang.com/django/django-queryset-advance.html

## 20180327
- 完善了按照区域汇总的部分，由于production_record中新增bigtype字段，通过ORM的select_related机制完成对bigtype的过滤
- 调整了按区域汇总的需求按钮，放到对应的template下，由用户来触发。

## TODO
完成按照district_detail的报表汇总
