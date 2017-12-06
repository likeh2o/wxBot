import json
 
#obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]
obj = '{"remark": "", "subject_type": 0, "description": "\u7a33\u4f4f\uff0c\u6211\u4eec\u80fd\u8d62", "title": "", "start_time": 0, "avatar": "/static/upload/photo/2017-11-29/cdc4d73404b6fa16e34fc99497f594e3e4b71676.jpg", "job_number": "", "origin_photo_id": 62, "birthday": null, "entry_date": null, "department": "", "end_time": 0, "id": 59, "name": "\u54f2\u54f2"}'
a = json.loads(obj)
print a['name']+a['description']

