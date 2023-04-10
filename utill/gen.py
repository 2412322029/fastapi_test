import base64
import io
import math
import os
import random
import string
import time
import uuid
import aiofiles

from utill.captcha import ImageCaptcha

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp.txt')
with open(path, "w") as f:
    pass


async def verifyCode(uu: str, cc: str) -> (bool, str):
    async with aiofiles.open(path, "r") as f:
        code_list = [tuple(i.replace('\n', '').split(',')) for i in await f.readlines()]
    try:
        for code in code_list:
            u, c, t = code
            if uu == u:
                if cc == c:
                    if math.floor(time.time()) - int(t) > 300:
                        return False, '过期验证码'
                    else:
                        return True, '验证成功'
                else:
                    return False, '验证码错误'
    finally:
        await delcode()


async def delcode():  # 删除过期code
    async with aiofiles.open(path, "r") as f:
        code_list = [tuple(i.replace('\n', '').split(',')) for i in await f.readlines()]
    for code in code_list:
        u, c, t = code

        if math.floor(time.time()) - int(t) > 300:
            code_list.remove(code)
    async with aiofiles.open(path, "w") as f:
        for live_code in code_list:
            await f.write(f'{live_code[0]},{live_code[1]},{live_code[2]}\n')


async def generateCode() -> (str, str):
    await delcode()
    code = ''
    for i in range(5):
        code += random.choice(string.ascii_uppercase)
    u = uuid.uuid4().__str__()
    t = math.floor(time.time())
    async with aiofiles.open(path, "a+") as f:
        await f.write(f'{u},{code},{t}\n')
    image = ImageCaptcha()
    img = image.generate_image(code)
    # 将图像转换为base64编码的字符串
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str, u


if __name__ == '__main__':
    # base64_img, u = generateCode()
    # print(base64_img)
    print(verifyCode('8f3b488b-9def-4323-a884-144413d716fd', 'pzxrd'))
