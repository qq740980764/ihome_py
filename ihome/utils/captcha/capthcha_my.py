import random
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
# from ttt import settings
import os
import base64
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
PATH = os.path.join(BASE_DIR, 'captcha/fonts/Arial.ttf')  # 字体
print(PATH)
LEN_VERIFY = 4


def get_verify():
     verify_len =LEN_VERIFY
     weight = 108
     hight = 41
       # 大写字母，小写字母，数字
     txt_list = [48, 49, 50, 51, 52, 53, 54, 55, 56, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
     81,
     82, 83, 84, 85, 86, 87, 88, 89, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
     111,
     112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
     image = Image.new('RGBA', (weight, hight), (255, 255, 255))
     font = ImageFont.truetype(PATH, 20)
     draw = ImageDraw.Draw(image)
       # 填充背景
     for x in range(weight):
         for y in range(hight):
             draw.point((x, y), fill=(200, 200, 200))
       # 生成随机验证码
     verify = ''
     for t in range(verify_len):
         text = chr(txt_list[random.randint(0, len(txt_list) - 1)])
     verify += text
     draw.text(((weight // verify_len) * t + 7, 10), text, font=font,
     fill = (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)))
     img_buffer = BytesIO()
     image.save(img_buffer, 'PNG')
     base = base64.b64encode(img_buffer.getvalue())
     return base, verify
