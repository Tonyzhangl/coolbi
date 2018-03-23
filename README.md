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

## TODO
完成按照区域性的报表汇总
