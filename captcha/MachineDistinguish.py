"""
机器验证识别模块
"""
import requests
import base64
import json
import re
import random
from captcha.captcha_validator import CaptchaValidatorImpl
from copy import deepcopy


class MachineDistinguish(CaptchaValidatorImpl):

    def __init__(self,text_list):
        """
        构造
        :param url: 图片url
        """
        self.text_list = text_list
        self.interface_url = "http://62.234.160.132/upload_b64"

    async def post_pic(self, im, codetype):
        # 处理图片
        json_image = self.deal_image(im)
        result_bool, json_data = self.get_interface(data=json_image)
        return (result_bool, json_data)

    def result_handler(self, data):
        result_bool, json_data = data
        if result_bool is False:
            message = json_data
            return False, message
        final_result = self.deal_data(data[1])
        print(final_result)
        # 选取三个汉字
        result_text = self.select_text(data=final_result)
        if result_text is False:
            return False, '汉字匹配不全'
        # 处理汉字
        result_data = self.deal_text(data=final_result)
        return True, result_data

    def deal_image(self, image: bytes):
        """
        加密图片
        :return:
        """
        # 判断图片文件是否存在
        pass

        base64_data = base64.b64encode(image)
        string_start = 'data:image/jpg;base64,'
        result = string_start + str(base64_data)[2:-1]
        # 新建字典
        temp = {}
        temp.update({'imgString': result})
        temp_result = json.dumps(temp)
        return temp_result

    def get_interface(self, data):
        """
        请求接口
        get_interface
        :param data:
        :return:
        """
        try:
            response = requests.post(url=self.interface_url, data=data)

        except Exception as e:
            message = '请求发生异常' + str(e)
            return False, message
        else:
            result = response.json()
            return True, result

    def deal_coordinate(self, point_set):
        """
        处理坐标，取中间值
        :return:
        """
        point_list = re.split(r',', point_set)
        point_list = [float(i) for i in point_list]
        # print(point_list)
        x1, y1, x2, y2, x3, y3, x4, y4 = point_list[0], point_list[1], point_list[2], point_list[3], point_list[4], \
                                         point_list[5], point_list[6], point_list[7],
        # 取对角线上的中间坐标
        one_point = ((x1 + x3) / 2, (y1 + y3) / 2)
        # 取对角线上的中间坐标
        two_point = ((x2 + x4) / 2, (y2 + y4) / 2)
        # 取中点坐标的中点
        point_result = (one_point[0] + two_point[0]) / 2, (one_point[1] + two_point[1]) / 2
        # print(one_point, two_point, point_result)
        return point_result

    def deal_data(self, result):
        """
        处理坐标
        :param result:
        :return:
        """
        # json数据解析
        coordinate_list = result['res']
        new_dict = {}
        for temp in coordinate_list:
            # 坐标
            point_set = temp['box']
            # print(point_set)
            # 处理坐标
            point_result = self.deal_coordinate(point_set)

            new_dict.update({temp['text']: point_result})

        return new_dict

    def select_text(self, data):
        """
        查找汉字，完全匹配就匹配，有一个汉字找不到，就随机选择
        俩个或者俩个以上找不到，求重新请求
        :param data: 接口数据
        :return:
        """
        new_data = deepcopy(data)
        temp_mark = []
        for num, text in enumerate(self.text_list):
            info = new_data.get(text, None)
            if info is None:
                temp_mark.append(num)

        if len(temp_mark) == 0:
            # 表示 汉字完全识别
            return True

        # 有一个汉字没有识别出来，进行随机选择
        elif len(temp_mark) == 1:

            # 先删除字典中已经有的汉字
            self.text_list.pop(temp_mark[0])
            for j in self.text_list:
                new_data.pop(j)

            # 随机选择
            temp_text = random.choice(list(new_data.keys()))
            # 插入
            self.text_list.insert(temp_mark[0], temp_text)

            return True

        else:
            # 有多个汉字没有识别出来
            return False

    def deal_text(self, data):
        """
        处理汉字文本
        :return:
        """
        new_list = []
        for text in self.text_list:
            local_info = data.get(text, None)
            # 可以匹配到汉字时候
            if local_info is not None:
                temp = str(int(local_info[0])) + '|' + str(int(local_info[1])) + "|" + str(
                    random.randint(10, 30)) + '|click'
                new_list.append(temp)
        return new_list



