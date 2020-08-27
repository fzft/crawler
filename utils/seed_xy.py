import random


def px_seed(xy_click_2: list, xy_click_1: list, options: str) -> list:
    # 8种情况生成move xy
    locus_xy_list = []

    if options == "RU":  # 右上 eg:2 (250,50) 1(150,100)
        x_pxs = int(xy_click_2[0]) - int(xy_click_1[0])
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) + i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) - i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list):  # y 差值补位
            y = y_pxs_list[-1]
            for i in range(len(x_pxs_list) - len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list):  # x 差值补位
            x = x_pxs_list[-1]
            for i in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(10, 30)}|move")
        return locus_xy_list

    if options == "RD":  # 右下 eg:2 (250,150) 1(150,100)
        x_pxs = int(xy_click_2[0]) - int(xy_click_1[0])
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) + i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) + i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list):  # y 差值补位
            y = y_pxs_list[-1]
            for _ in range(len(x_pxs_list) - len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list):  # x 差值补位
            x = x_pxs_list[-1]
            for _ in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(10, 30)}|move")
        return locus_xy_list

    if options == "LU":  # 左上 eg:2 (80,50) 1(150,100)
        x_pxs = abs(int(xy_click_2[0]) - int(xy_click_1[0]))
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) - i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) - i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list):  # y 差值补位
            y = y_pxs_list[-1]
            for _ in range(len(x_pxs_list) - len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list):  # x 差值补位
            x = x_pxs_list[-1]
            for _ in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(10, 30)}|move")
        return locus_xy_list

    if options == "LD":  # 左下 eg:2 (80,150) 1(150,100)
        x_pxs = abs(int(xy_click_2[0]) - int(xy_click_1[0]))
        y_pxs = abs(int(xy_click_2[1]) - int(xy_click_1[1]))

        x_pxs_list = [int(xy_click_1[0]) - i for i in range(x_pxs)]
        y_pxs_list = [int(xy_click_1[1]) + i for i in range(y_pxs)]

        if len(x_pxs_list) >= len(y_pxs_list):  # y 差值补位
            y = y_pxs_list[-1]
            for _ in range(len(x_pxs_list) - len(y_pxs_list)):
                y_pxs_list.append(y)
            assert len(x_pxs_list) == len(y_pxs_list)
        if len(x_pxs_list) < len(y_pxs_list):  # x 差值补位
            x = x_pxs_list[-1]
            for _ in range(len(y_pxs_list) - len(x_pxs_list)):
                x_pxs_list.append(x)
            assert len(x_pxs_list) == len(y_pxs_list)
        # x y 合并
        for index in range(len(x_pxs_list)):
            locus_xy_list.append(f"{x_pxs_list[index]}|{y_pxs_list[index]}|{random.randint(10, 30)}|move")
        return locus_xy_list


def xy_seed(point_xy_list: list) -> list:
    """ click坐标点 生成移动轨迹 """

    if len(point_xy_list) != 3:
        return ["入参错误"]
    xy_click_1 = point_xy_list[0].split("|")
    xy_click_2 = point_xy_list[1].split("|")
    xy_click_3 = point_xy_list[2].split("|")
    if len(xy_click_1) + len(xy_click_2) + len(xy_click_3) != 12:
        return ["入参错误"]
    step_1_xy = xy_handle(xy_click_1, xy_click_2)
    step_2_xy = xy_handle(xy_click_2, xy_click_3)
    return step_1_xy + step_2_xy + [point_xy_list[2]]


def xy_handle(xy_click_1, xy_click_2):
    # 点击1 -> 点击2 轨迹
    # 右上 右下 左上 左下 四种情况
    if int(xy_click_2[0]) >= int(xy_click_1[0]) and int(xy_click_2[1]) < int(xy_click_1[1]):  # 2号点击 在 1号 右上 上
        locus_xy_list = px_seed(xy_click_2, xy_click_1, "RU")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list
    if int(xy_click_2[0]) > int(xy_click_1[0]) and int(xy_click_2[1]) >= int(xy_click_1[1]):  # 2号点击 在 1号 右下 右
        locus_xy_list = px_seed(xy_click_2, xy_click_1, "RD")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list
    if int(xy_click_2[0]) < int(xy_click_1[0]) and int(xy_click_2[1]) <= int(xy_click_1[1]):  # 2号点击 在 1号 左上 左
        locus_xy_list = px_seed(xy_click_2, xy_click_1, "LU")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list
    if int(xy_click_2[0]) <= int(xy_click_1[0]) and int(xy_click_2[1]) > int(xy_click_1[1]):  # 2号点击 在 1号 左下 下
        locus_xy_list = px_seed(xy_click_2, xy_click_1, "LD")
        all_xy_list = ["|".join(xy_click_1)] + locus_xy_list
        return all_xy_list


if __name__ == '__main__':
    print(xy_seed(['250|76|22|click', '191|52|24|click', '84|51|20|click']))