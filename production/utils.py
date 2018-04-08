# -*- coding:utf8 -*-
from django.db.models import Sum

def list2dict(districtrecord, phase, key_district, key_district_detail, sum_key):
    d = []
    list_ = districtrecord.objects.filter(phase=phase).values(key_district, key_district_detail).annotate(annotate_key=Sum(sum_key)).all()

    k = ''
    for _, item in enumerate(list_):
        if k != item.get(key_district):
            d.append({'district_id': item.get(key_district), 'details': [{key_district_detail: item.get(key_district_detail), sum_key: item.get('annotate_key')}]})
            k = item.get(key_district)
        else:
            d.get(item.get('details')).append({key_district_detail: item.get(key_district_detail), sum_key: item.get('annotate_key')})
    return d
