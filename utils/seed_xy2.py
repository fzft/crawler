import random
from pprint import pprint


def random_point(xy_click_2:list,xy_click_1:list)->list:
    """ 两点间生成轨迹点个数及位置 """
    point_x_list = []
    point_y_list = []
    point_num = random.randint(1,3)  # 随机生成1-3个坐标点
    if int(xy_click_2[0]) >= int(xy_click_1[0]):  # x轴
        for _ in range(point_num):
            point_x_list.append(random.randint(int(xy_click_1[0]),int(xy_click_2[0])))
    else:
        for _ in range(point_num):
            point_x_list.append(random.randint(int(xy_click_2[0]), int(xy_click_1[0])))

    if int(xy_click_2[1]) >= int(xy_click_1[1]): # y轴
        for _ in range(point_num):
            point_y_list.append(random.randint(int(xy_click_1[1]),int(xy_click_2[1])))
    else:
        for _ in range(point_num):
            point_y_list.append(random.randint(int(xy_click_2[1]),int(xy_click_1[1])))
    random_point_xy_list = []
    for i in range(point_num):
        random_point_xy_list.append([f"{point_x_list[i]}",f"{point_y_list[i]}",f"{random.randint(5,20)}","move"])
    return random_point_xy_list



def px_seed(xy_click_2:list,xy_click_1:list,options:str)->list:
    # 8种情况生成move xy
    locus_xy_list = []

    if options == "RU": # 右上 eg:2 (250,50) 1(150,100)
        x_pxs = int(xy_click_2[0]) - int(xy_click_1[0])
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) + i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) - i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list): # y 差值补位
            y = y_pxs_list[-1]
            for i in range(len(x_pxs_list)-len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list): # x 差值补位
            x = x_pxs_list[-1]
            for i in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(5, 20)}|move")
        return locus_xy_list

    if options == "RD": # 右下 eg:2 (250,150) 1(150,100)
        x_pxs = int(xy_click_2[0]) - int(xy_click_1[0])
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) + i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) + i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list): # y 差值补位
            y = y_pxs_list[-1]
            for _ in range(len(x_pxs_list)-len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list): # x 差值补位
            x= x_pxs_list[-1]
            for _ in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(5, 20)}|move")
        return locus_xy_list

    if options == "LU": # 左上 eg:2 (80,50) 1(150,100)
        x_pxs = abs(int(xy_click_2[0]) - int(xy_click_1[0]))
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) - i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) - i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list): # y 差值补位
            y = y_pxs_list[-1]
            for _ in range(len(x_pxs_list)-len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list): # x 差值补位
            x= x_pxs_list[-1]
            for _ in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(5,20)}|move")
        return locus_xy_list



    if options == "LD": # 左下 eg:2 (80,150) 1(150,100)
        x_pxs = abs(int(xy_click_2[0]) - int(xy_click_1[0]))
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) - i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) + i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list): # y 差值补位
            y = y_pxs_list[-1]
            for _ in range(len(x_pxs_list)-len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list): # x 差值补位
            x= x_pxs_list[-1]
            for _ in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(5, 20)}|move")
        return locus_xy_list




def xy_seed(point_xy_list:list)->list:
    """ click坐标点 生成移动轨迹 """

    if len(point_xy_list) != 3:
        return ["入参错误"]
    xy_click_1 = point_xy_list[0].split("|")
    xy_click_2 = point_xy_list[1].split("|")
    xy_click_3 = point_xy_list[2].split("|")
    if len(xy_click_1)+len(xy_click_2)+len(xy_click_3) != 12:
        return ["入参错误"]

    # 添加point1 -> point2, point2 -> point3 中间随机点  结果[xy1,xyr...,xy2,xyr...,xy3]
    random_point_part1 = random_point(xy_click_1,xy_click_2)
    random_point_part2 = random_point(xy_click_2, xy_click_3)
    random_point_part1.insert(0,xy_click_1)
    random_point_part1.append(xy_click_2)
    random_point_part2.append(xy_click_3)
    all_point_xy_list = random_point_part1 + random_point_part2
    temp_xy_list = []
    for i in range(len(all_point_xy_list)-1):
        temp_xy_list += xy_handle(all_point_xy_list[i],all_point_xy_list[i+1])


    return temp_xy_list+[point_xy_list[2]]

def xy_handle(xy_click_1,xy_click_2):
    # 点击1 -> 点击2 轨迹
    # 右上 右下 左上 左下 八种情况


    if int(xy_click_2[0]) >= int(xy_click_1[0]) and int(xy_click_2[1]) < int(xy_click_1[1]): # 2号点击 在 1号 右上 上
        locus_xy_list = px_seed(xy_click_2,xy_click_1,"RU")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list
    if int(xy_click_2[0]) > int(xy_click_1[0]) and int(xy_click_2[1]) >= int(xy_click_1[1]): # 2号点击 在 1号 右下 右
        locus_xy_list = px_seed(xy_click_2, xy_click_1, "RD")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list
    if int(xy_click_2[0]) < int(xy_click_1[0]) and int(xy_click_2[1]) <= int(xy_click_1[1]): # 2号点击 在 1号 左上 左
        locus_xy_list = px_seed(xy_click_2, xy_click_1, "LU")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list
    if int(xy_click_2[0]) <= int(xy_click_1[0]) and int(xy_click_2[1]) > int(xy_click_1[1]): # 2号点击 在 1号 左下 下
        locus_xy_list = px_seed(xy_click_2, xy_click_1, "LD")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list



if __name__ == '__main__':
    pprint(xy_seed(['276|111|29|click', '151|93|21|click', '256|60|17|click']))