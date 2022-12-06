import json
from os import path

GDkey = 'enter your key here'
tar_loc = r'your aiskLevelApi api branch location here'

def get_total():
    # 从info.json中获取文件列表
    info = path.join(tar_loc, 'info.json')
    file_list = json.load(open(info, encoding='utf-8'))["file_list"]

    # 将所有json整合进records
    records = []
    for f in file_list:
        with open(path.join(tar_loc, f['file_name']), encoding='utf-8') as file:
            records.append(json.loads(file.read()))
    return records

def get_latest():
    info = path.join(tar_loc, 'latest.json')
    data = json.load(open(info, encoding='utf-8'))
    return [data]


records = get_latest()


# 对records中不和shp符合的部分进行记录
def modify(l):
    if l[0] == '北京市':
        return [l[0], l[0], l[1]]
    elif l[1] in ['东莞市', '中山市']:
        return [l[0], l[1], l[1]]
    elif l[1] == '省直辖县级行政单位':
        return [l[0], '乐东黎族自治县', l[2]]  # 不符合实际，结合shp文件将就用
    else:
        return l


# 提取records里的所有地点三元组
locations = []
for i in records:
    for j in i['data']['highlist'] + i['data']['middlelist']:
        if j['province']:  # 有空值
            locations.append(modify([j['province'], j['city'], j['county']]))

# 地点locations去重 获得individual
temp = [','.join(i) for i in locations]
temp_set = set(temp)
individual = [i.split(',') for i in list(temp_set)]

# 存储individual
# with open('history1.csv','w+',encoding='ANSI') as f:
#     f.write('\n'.join([','.join(i) for i in individual if i[0]]))

# 读取shp文件
with open('shpData.csv', encoding='ANSI') as f:
    total_raw = [row.split(',') for row in f.readlines()]

# 补充shp数据中直辖市部分city数据的缺失
total = []
for t in total_raw[1:]:
    if not t[3].strip():
        t[3] = t[1]
        t[4] = t[2] # 直辖市在市.shp也是这个
    total.append(t)

# 获得以三元组字符串为索引，代码为值的字典
total_dict = {}
for t in total:
    total_dict[t[1] + t[3] + t[5]] = t[6]

# 读取不在shp中，但之前通过高德查询过，并因此获得了匹配的code的地址字典
try:
    complete_missed = json.load(open('complete_missed.json', 'r+'))
except FileNotFoundError:
    complete_missed = {}

total_dict.update(complete_missed)

# 利用字典匹配
codes = []
missed = []
for i in individual:
    code = total_dict.get(''.join(i))
    if code:
        if code != '999999':
            codes.append(code)
    else:
        missed.append(i)

# 利用高德api补全missed
import requests


def gaode(city, text):
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'key': GDkey,
        'address': text,
        'city': city
    }
    r = requests.get(url, params)
    print('GD:', text)
    return r


for m in missed:
    r = gaode('', ' '.join(m))
    rt = json.loads(r.text)
    if rt.get('geocodes'):
        gc = rt['geocodes'][0]
        if gc.get('adcode'):
            mcode = gc.get('adcode')
        else:
            mcode = '999999'  # 在验证时，为999999则不会被记录到code中，即放弃将该地址绘入图中
    else:
        mcode = '999999'
    complete_missed[''.join(m)] = mcode

# 如果当日出现了新的不在shp文件中的情况，则在高德获取后更新到json中
if missed:
    json.dump(complete_missed, open('complete_missed.json', 'w+'))

json.dump(codes,open('latest_code.json','w+'))
