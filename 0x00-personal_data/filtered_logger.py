import logging
import bcrypt

logging.basicConfig(filename="basic.log", level=logging.INFO, format='%(asctime)s:%(filename)s:%(levelname)s:%(funcName)s:%(message)s')


def squares(lst: list[int]):
    return [i**2 for i in lst]

ans = squares([4,5,6,2,6,8])
logging.info(ans)

# my password
password = "Bruuh@2020"
