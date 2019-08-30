# coding: utf-8

import pandas as pd 
import numpy as np

import folium


def num_position(col):
    """
    effects：针对列表中['(1,2)','(10,3)']的转换为:[[1,2],[10,3]...]
    col:[[1,2],[10,3]...] or pd.series
    """
    f = lambda x:list(map(float, x[1:-1].split(",")))    
    return (list(map(f, col)))


def df_pos(data,col_name):
    """
    effects:针对数据框中某列地理位置(str)转换为数字型(list)列
    data:DataFrame文件
    col_name:位置列名
    """
    data[col_name] = data.apply(lambda x:list(map(float, x[col_name][1:-1].split(","))), axis=1)
    print("数据框位置列已转换")
    return data[col_name]


def position_lng_lat(col):
    """
    effects:将文本型数据['(lat,lng)'...]拆分成数值型lat,lng
    col:[[1,2],[10,3]...] or pd.series
    """
    position = num_position(col)
    return list(np.array(position)[:,0]), list(np.array(position)[:, 1])
    


# 将经度，纬度数据整合变为新的一列[lat,lng]
def lng_lat(data, lng='longitude', lat='latitude'):
    """
    data:DataFrame---带有经纬度列的数据
    lng,lat:str
    """
    f = data.apply(lambda x:[x[lat], x[lng]], axis=1)
    #data['position'] = data.apply(lambda x:[x[lat], x[lng]], axis=1)
    return(f)



def geodistance(lng1, lat1, lng2, lat2,R=6371.393):
    from math import radians, cos, sin, asin, sqrt
    # 经纬度转换成弧度
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a=sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2 
    # 地球平均半径6371.393km
    distance=2*asin(sqrt(a))*R*1000 
    distance=round(distance/1000, 5)
    # 返回结果单位是千米
    return distance
    


def geodistance1(p1, p2, R=6371.393):
    """
    point p1(latA,lonA)
    point p2(latB,lonB)
    """
    from math import radians, cos, sin, asin, sqrt
    # 经纬度转换成弧度
    lng1, lat1, lng2, lat2 = map(radians, [float(p1[1]), float(p1[0]), float(p2[1]), float(p2[0])])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2 
    distance = 2*asin(sqrt(a))*R*1000 
    distance = round(distance/1000, 5)
    # 返回结果单位是千米
    return distance


def getDegree(lonA,latA,lonB,latB):
    """
    Args:
        point p1(lonA,latA)
        point p2(lonB,latB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    from math import radians, cos, sin, sqrt,degrees, atan2
    radLatA, radLonA, radLatB, radLonB= map(radians, [float(latA), float(lonA), float(latB), float(lonB)])
    dLon = radLonB - radLonA
    y = sin(dLon)*cos(radLatB)
    x = cos(radLatA)*sin(radLatB) - sin(radLatA)*cos(radLatB)*cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
	#返回的是度数
    return brng

	
# 计算单点到多点的距离[纬度，经度]
def dist_list(pos,list_pos):
    """
    pos：单个位置点eg:[latA,lonA]
    list_pos：[[latA,lonA],[latB,lonB]...] OR pd.series
    """
    f = lambda x: geodistance1(x, pos)
    return list(map(f, list_pos))



	
# 计算一组经纬度数据的距离矩阵
def dist_matrix(n_position):
    """n_position:[[lat,lng],[]...] or pd.series """
    d_ma = []
    for i in n_position:
        d_ma.append(dist_list(i, n_position))
    d_ma = pd.DataFrame(d_ma)
    # 返回数据框型距离矩阵
    return(d_ma)
        

		

# 要已知距离矩阵dmatrix,来统计小于s千米内的点的个数及平均距离
def count_dist(dmatrix, s=100):
    s_count = ((dmatrix < s) & (dmatrix != 0)).sum(axis=1)
    s_aver = dmatrix[(dmatrix < s) & (dmatrix != 0)].mean(axis=1)
    #s_min = dmatrix[(dmatrix < s) & (dmatrix != 0)].min(axis=1)
    return s_count, s_aver


	
data = pd.read_csv('C:\\Users\\z50004593\\Desktop\\python_ceshi\\position.csv')


# ####画图类####




#在地图上依据经纬度描多个点
def map_pict(pos_list, filename, r=100):
    m = folium.Map(location=pos_list[0], zoom_start=10, control_scale=True)
    for i in pos_list:
        folium.Circle(radius=100, location=i, color='#3388ff', fill=True, fill_opacity=0.7).add_to(m)
    m.save(filename)
    print('the map exsits in:' + filename)
# 示例：map_pict([[35.002,118.204],[35.0012,118.2041],[35.0052,118.24],[35.0122,118.104],[35.00012,118.0204]],'C:\\Users\\z50004593\\Desktop\\ceshi.html')   
    



# 在地图上依据经纬度描多个点，folium学习可参考：https://www.cnblogs.com/feffery/p/9282808.html
# color的可选项包括：['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
def map_pict(pos_list,filename, r=100):
    m = folium.Map(location=pos_list[0], zoom_start=10, control_scale=True)
    for i in pos_list:
        folium.Circle(radius=100, location=i, color='#3388ff', fill=True, fill_opacity=0.7).add_to(m)
    '''为地图对象添加点击显示经纬度的子功能'''
    # m.add_child(folium.LatLngPopup())
    """实现点击地图任意位置产生一个新的图标,双击可取消标记"""
    # m.add_child(folium.ClickForMarker())    
    m.save(filename)
    print('the map exsits in:' + filename)


# 多点连线
def pos_line(pos_list,filename):
    m = folium.Map(location=pos_list[0],
              zoom_start=10,
              control_scale=True)
    ls = folium.PolyLine(locations=pos_list,
                    color='blue')
    ls.add_to(m)
    m.save(filename)
    print('the map_PolyLine exsits in:'+filename)

