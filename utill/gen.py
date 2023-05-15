import base64
import io
import math
import os
import random
import string
import time
import uuid
import aiofiles
import asyncio
from utill.captcha import ImageCaptcha

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp.txt')
with open(path, "a+") as _:
    pass


async def verifyCode(uu: str, cc: str) -> (bool, str):
    async with aiofiles.open(path, "r") as f:
        code_list = [tuple(i.replace('\n', '').split(',')) for i in await f.readlines()]

    for code in code_list:
        u, c, t = code
        if uu == u:
            if cc == c:
                if math.floor(time.time()) - int(t) > 300:
                    await del_code(u)
                    return False, '过期验证码'
                else:
                    await del_code(u)
                    return True, '验证成功'
            else:
                return False, '验证码错误'
    return False, '未知uuid'


async def del_code(uuid_: str = ''):  # 删除过期code
    async with aiofiles.open(path, "r") as f:
        code_list = [tuple(i.replace('\n', '').split(',')) for i in await f.readlines()]
    for code in code_list:
        u, c, t = code

        if math.floor(time.time()) - int(t) > 300 or u == uuid_:
            code_list.remove(code)
    async with aiofiles.open(path, "w") as f:
        for live_code in code_list:
            await f.write(f'{live_code[0]},{live_code[1]},{live_code[2]}\n')


gen_times = 0


async def generateCode() -> (str, str):
    global gen_times
    gen_times += 1
    if gen_times == 100:
        await del_code()
    code = ''
    for i in range(5):
        code += random.choice(string.ascii_uppercase)
    u = str(uuid.uuid4())
    t = math.floor(time.time())
    async with aiofiles.open(path, "a+") as f:
        await f.write(f'{u},{code},{t}\n')
    image = ImageCaptcha()
    img = image.generate_image(code)
    # 将图像转换为base64编码的字符串
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return img_str, u


async def main():
    # print(await verifyCode('930236ac-876e-4f87-bf42-83e780fc7f7b', 'OARDL'))
    print(await generateCode())


if __name__ == '__main__':
    asyncio.run(main())
