# encoding: utf-8
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import math
import random


def dcmp(x):
    if math.fabs(x) <= 1e-8:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def draw_skeleton(pxlist, pylist):
    """

    :rtype: void
    :param pxlist: x coordinates   
    :param pylist: y coordinates
    """
    plt.scatter(pxlist, pylist, alpha=0.5)  # 绘制出图形
    plt.show()


def getdist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def get_noise_effect(pxlist, pylist, noise_amount, noise_width):
    """
    
    :param pxlist: The x-coordinate of the set of points
    :param pylist: The y-coordinate of the set of points
    :param noise_amount: The number of the noise points
    :param noise_width: The width range in which noise occurs
    :return: The set of skeleton points after deformation
    """
    """
    The noise points are regarded as a magnet, the skeleton points are 
    fixed in the initial position by the rubber band, and finally the 
    skeleton points are in the state of force balance.
    """
    noise_x = []
    noise_y = []
    tot = len(pxlist)
    noise_sum_x = 0
    noise_sum_y = 0
    for i in range(noise_amount):
        pos = random.randint(0, tot)
        pos2 = (pos+1)%tot
        if pxlist[pos] == pxlist[pos2]:  #  斜率不存在
            dir = random.choice([-1, 1])
            delta = random.uniform(0, noise_width)
            noise_x.append(pxlist[pos]+dir*delta)
            noise_y.append(pylist[pos])
        else:  # 斜率存在，在法线方向
            norm_k = -1.0/((pylist[pos2]-pylist[pos])/(pxlist[pos2]-pxlist[pos]))
            norm_x = 1.0/math.sqrt(1.0+norm_k*norm_k)
            norm_y = norm_k/math.sqrt(1.0+norm_k*norm_k)
            dir = random.choice([-1, 1])
            delta = random.uniform(0, noise_width)
            noise_x.append(pxlist[pos]+dir*norm_x*delta)
            noise_y.append(pylist[pos]+dir*norm_y*delta)
        noise_sum_x += noise_x[i]
        noise_sum_y += noise_y[i]
    for i in range(tot):
        new_x = pxlist[i]
        new_y = pylist[i]
        delta_x = 0
        delta_y = 0
        for j in range(noise_amount):
            dis = getdist(noise_x[j], noise_y[j], pxlist[i], pylist[i])
            force = 1/(dis*dis)
            delta_x += force*math.fabs(math.cos((noise_y[j]-pylist[i])/(noise_x[j]-pxlist[i])))
            delta_y += force*math.fabs(math.sin((noise_y[j]-pylist[i])/(noise_x[j]-pxlist[i])))
        pxlist[i] += delta_x
        pylist[i] += delta_y


    # for i in range(tot):
    #     pxlist[i] = float((pxlist[i]+noise_sum_x))/(noise_amount+1)
    #     pylist[i] = float((pylist[i]+noise_sum_y))/(noise_amount+1)
    for i in range(noise_amount):
        pxlist.append(noise_x[i])
        pylist.append(noise_y[i])
    return pxlist, pylist

def draw_circle_skeleton(cluseter_angle, cluster_area, cluster_density,
                         cluster_distribution, noise_amount, noise_width, central_point):
    """

    :rtype: list point sets skeleton
    :param cluster_area: float
    :param cluseter_angle: float [-180,180]
    :param central_point: [float, float]
    """
    """
        (x-a)^2 + (y-b)^2 = r;
        pi*r*r = cluster_area --> r = sqrt(cluster_area/pi)
        x = a + r*sin(sita)
        y = b + r*cos(sita)
    """
    circle_sets = []
    pxlist = []
    pylist = []
    a = central_point[0]
    b = central_point[1]
    r = math.sqrt(cluster_area / math.pi)
    alpha = cluseter_angle / 180.0 * math.pi
    # print("r: ", r)
    # 0 2*pi* 1/200  2*pi*2/200 ...  2*pi*199/200
    for i in range(200):
        sita = 2 * math.pi * i / 200
        x = a + r * math.sin(sita)
        y = b + r * math.cos(sita)
        new_x = (x - a) * math.cos(alpha) - (y - b) * math.sin(alpha) + a
        new_y = (x - a) * math.sin(alpha) + (y - b) * math.cos(alpha) + b
        point = [new_x, new_y]
        pxlist.append(new_x)
        pylist.append(new_y)
        circle_sets.append(point)
    pxlist, pylist = get_noise_effect(pxlist, pylist, noise_amount, noise_width)
    draw_skeleton(pxlist, pylist)
    return circle_sets


def draw_oval_skeleton(cluster_area, cluster_angle, central_point):
    """

    :rtype: list point sets skeleton
    :param cluster_area: float
    :param cluster_angle: float [-180,180]
    :param central_point: [float, float]
    """

    """
    x^2/a^2 + y^2/b^2 = 1
    area = pi*a*b
    central_point: (m,n)
    x = m + a*cos(sita)
    y = n + b*sin(sita)
    """
    a = random.randint(2, 10)  # 半长轴 semi-major axis
    b = cluster_area / math.pi / a
    # 0 2*pi*1/200 2*pi*2/200 2*pi*3/200 ... 2*pi*199/200
    oval_sets = []
    pxlist = []
    pylist = []
    m = central_point[0]
    n = central_point[1]
    print(cluster_angle)
    alpha = cluster_angle / 180.0 * math.pi
    print("alpha: ", alpha)
    for i in range(200):
        sita = 2 * math.pi * i / 200
        x = m + a * math.cos(sita)
        y = n + b * math.sin(sita)
        new_x = (x - m) * math.cos(alpha) - (y - n) * math.sin(alpha) + m
        new_y = (x - m) * math.sin(alpha) + (y - n) * math.cos(alpha) + n
        point = [new_x, new_y]
        pxlist.append(new_x)
        pylist.append(new_y)
        oval_sets.append(point)
    draw_skeleton(pxlist, pylist)
    return oval_sets


def gettrianglearea(x1, y1, x2, y2, x3, y3):
    """

    :rtype: float
    :param x1: vertices1.x
    :param y1: vertices1.y
    :param x2: vertices2.x
    :param y2: vertices2.y
    :param x3: vertices3.x
    :param y3: vertices3.y
    :return: S the area of the triangle
    """
    S = 0.5 * (x1 * y2 + x2 * y3 + x3 * y1 - x1 * y3 - x2 * y1 - x3 * y2)
    S = math.fabs(S)
    return S


def gettriangleperimeter(x1, y1, x2, y2, x3, y3):
    return getdist(x1, y1, x2, y2) + \
           getdist(x2, y2, x3, y3) + \
           getdist(x3, y3, x1, y1)


def draw_triangle_skeleton(cluster_area, cluster_angle, central_point):
    """

    :rtype: list point sets skeleton
    :param cluster_area: float 缩放
    :param cluster_angle: float [-180,180]
    :param central_point: [float, float]
    """
    """
    Randomly generate 3 points and scale to the required area
    """
    vx = []
    vy = []
    cx = 0
    cy = 0
    a = central_point[0]
    b = central_point[1]
    while True:
        for i in range(3):
            vx.append(random.randint(0, 50))
            vy.append(random.randint(0, 50))
        # Sacle the triangle to required area
        old_S = gettrianglearea(vx[0], vy[0], vx[1], vy[1], vx[2], vy[2])
        if dcmp(old_S) != 0:
            break
    t = math.sqrt(float(cluster_area) / float(old_S))
    for i in range(3):
        vx[i] *= t
        vy[i] *= t
        cx += vx[i]
        cy += vy[i]
    cx /= 3.0
    cy /= 3.0
    for i in range(3):
        vx[i] -= (cx - a)
        vy[i] -= (cy - b)
    vx.append(vx[0])
    vy.append(vy[0])
    print("new_S: ", gettrianglearea(vx[0], vy[0], vx[1], vy[1], vx[2], vy[2]))
    C = gettriangleperimeter(vx[0], vy[0], vx[1], vy[1], vx[2], vy[2])
    triangle_sets = []
    pxlist = []
    pylist = []

    for j in range(3):
        step_num = int(float(getdist(vx[j], vy[j], vx[(j + 1) % 3], vy[(j + 1) % 3])) / float(C) * 200.0)
        for i in range(step_num):
            new_x = vx[j] + 1.0 * i / step_num * (vx[(j + 1) % 3] - vx[j])
            new_y = vy[j] + 1.0 * i / step_num * (vy[(j + 1) % 3] - vy[j])
            point = [new_x, new_y]
            pxlist.append(new_x)
            pylist.append(new_y)
            triangle_sets.append(point)
    print(len(pxlist), len(pylist))
    draw_skeleton(pxlist, pylist)
    return triangle_sets
    # plt.plot(vx, vy)
    # plt.show()


def getpolygonperimeter(vx, vy):
    totvex = len(vx)
    sumlen = 0
    for i in range(totvex):
        sumlen += getdist(vx[i], vy[i], vx[(i + 1) % totvex], vy[(i + 1) % totvex])
    return sumlen


def getpolygonarea(vx, vy):
    """
    多边形坐落于一个外接圆上，利用叉积求面积
    :param vx: 顶点横坐标
    :param vy: 顶点纵坐标
    :return: 多边形的面积
    """
    tot = len(vx)
    sum = 0
    for i in range(tot):
        sum += vx[i]*vy[(i+1)%tot] - vx[(i+1)%tot]*vy[i]
    return sum*0.5


def draw_polygon_skeleton(num_vertex, cluster_area, cluster_angle, central_point):
    """

    :rtype: list point sets skeleton
    :param num_vertex: the number of vertexes
    :param cluster_area: float 缩放
    :param cluster_angle: float [-180,180]
    :param central_point: [float, float]
    """
    """
    Determine an external circle, then determine the vertex on the circle,
    connect and scale to the specified area
    r = 20
    x = rcos(sita)
    y = rsin(sita)
    """
    r = 20
    vx = []
    vy = []
    totangle = 2 * math.pi
    minangle = 5.0 / 360.0 * totangle
    pre = 0
    for i in range(num_vertex - 1):
        sita = random.uniform(min(minangle, totangle / 2.0), totangle / 2.0)
        totangle -= sita
        vx.append(r * math.cos(pre + sita))
        vy.append(r * math.sin(pre + sita))
        pre += sita
    vx.append(r * math.cos(pre + totangle))
    vy.append(r * math.sin(pre + totangle))
    alpha = cluster_angle/180.0*math.pi
    for i in range(num_vertex):
        newx = vx[i]*math.cos(alpha) - vy[i]*math.sin(alpha)
        newy = vx[i]*math.sin(alpha) + vy[i]*math.cos(alpha)
        vx[i] = newx
        vy[i] = newy
    # vx.append(vx[0])
    # vy.append(vy[0])
    S = getpolygonarea(vx, vy)
    t = math.sqrt(float(cluster_area)/float(S))
    cx = 0
    cy = 0
    a = central_point[0]
    b = central_point[1]
    for i in range(num_vertex):
        vx[i] *= t
        vy[i] *= t
        cx += vx[i]
        cy += vy[i]
    cx /= num_vertex
    cy /= num_vertex
    for i in range(num_vertex):
        vx[i] -= (cx - a)
        vy[i] -= (cy - b)
    print("area: ", getpolygonarea(vx, vy))
    pxlist = []
    pylist = []
    polygon_sets = []
    C = getpolygonperimeter(vx, vy)
    for i in range(num_vertex):
        step_num = int(
            float(getdist(vx[i], vy[i], vx[(i + 1) % num_vertex], vy[(i + 1) % num_vertex])) / float(C) * 200)
        for j in range(step_num):
            new_x = vx[i] + 1.0 * j / step_num * (vx[(i + 1) % num_vertex] - vx[i])
            new_y = vy[i] + 1.0 * j / step_num * (vy[(i + 1) % num_vertex] - vy[i])
            point = [new_x, new_y]
            pxlist.append(new_x)
            pylist.append(new_y)
            polygon_sets.append(point)
    print(len(pxlist), len(pylist))
    draw_skeleton(pxlist, pylist)
    return polygon_sets
    # plt.plot(vx, vy)
    # plt.show()


def gen_region_cluster_skeleton(cluster_type, cluster_shape, cluster_angle,
                                cluster_area, cluster_density, cluster_distribution,
                                noise_amount, noise_width, central_point):
    """

    :rtype: point sets skeleton
    :param cluster_type: int  1: linear  2: regional
    :param cluster_shape: int 1:圆形、2:椭圆形、3:三角形、4:四边形、5:五边形、6:六边形、7:星形
    :param cluster_area: float 缩放
    :param cluster_angle: float [-180,180]
    :param cluster_density: float
    :param cluster_distribution: int {uniform, random, Gaussian} 以区域中心点为中心
    :param noise_amount: int
    :param noise_width: float
    :param central_point: [float, float]
    """
    points_sets = []
    if cluster_type == 1:
        return points_sets
    if cluster_shape == 1:
        points_sets = draw_circle_skeleton(cluster_angle, cluster_area, cluster_density,
                                           cluster_distribution, noise_amount, noise_width, central_point)
    elif cluster_shape == 2:
        points_sets = draw_oval_skeleton(cluster_area, cluster_angle, central_point)
    elif cluster_shape == 3:
        points_sets = draw_polygon_skeleton(3, cluster_area, cluster_angle, central_point)
        # points_sets = draw_triangle_skeleton(cluster_area, cluster_angle, central_point)
    elif cluster_shape == 4:
        points_sets = draw_polygon_skeleton(4, cluster_area, cluster_angle, central_point)
    elif cluster_shape == 5:
        points_sets = draw_polygon_skeleton(5, cluster_area, cluster_angle, central_point)
    elif cluster_shape == 6:
        points_sets = draw_polygon_skeleton(6, cluster_area, cluster_angle, central_point)
    return points_sets


if __name__ == '__main__':
    # cluster_type, cluster_shape, cluster_angle,
    # cluster_area, cluster_density, cluster_distribution,
    # noise_amount, noise_width, central_point
    for i in range(5):
        points_sets = gen_region_cluster_skeleton(2, 1, 10, 30, 10, 1, 1, 3, [0, 0])
    # points_sets = gen_region_cluster_skeleton(2, 2, 30, 45, 10, 1, 1, 5, [0, 0])
    # points_sets = gen_region_cluster_skeleton(2, 3, 20, 30, 10, 1, 1, 5, [5, 5])
    # points_sets = gen_region_cluster_skeleton(2, 4, 20, 50, 10, 1, 1, 5, [5, 6])
    pass