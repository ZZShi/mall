import random

import requests
from faker import Faker
from loguru import logger


fake = Faker(locale='zh_CN')


def get_hero() -> dict:
    """获取英雄信息"""
    hero_list = requests.get("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()["hero"]
    hero = random.choice(hero_list)
    info = {
        "nickname": hero["name"],
        "name": hero["title"],
        "avatar": f"https://game.gtimg.cn/images/lol/act/img/champion/{hero['alias']}.png",
        "phone": fake.phone_number(),
        "email": fake.email(),
        "remark": hero["keywords"]
    }
    logger.debug(f"英雄信息: {info}")
    return info


def get_ip_addr(ip: str) -> str:
    addr = "未知"
    url = f"http://ip-api.com/json/{ip}"
    try:
        data = requests.get(url).json()
        if data['status'] == 'success':
            region = data['regionName']
            city = data['city']
            addr = f"{region}, {city}"
    finally:
        logger.debug(f"{ip = } 的归属地为 {addr}")
        return addr


if __name__ == '__main__':
    # get_ip_addr("125.119.235.142")
    get_hero()