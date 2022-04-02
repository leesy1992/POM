# from importlib.abc import Loader
# import random,json,hashlib
# # 来迟
# import faker

# def faker_word(location='zh_CN'):
#     sentence=faker.Faker(locale=location).phone_number()
#     lon=sentence[:-1]
#     lens=sentence[::-1]
#     print(sentence,lon,lens)

# a=2.0
# b=2.0
# c=2223222
# d=2223222

# print(a is b)
# print(c is d)
# print(hash('123'))
# print(hash("123456"))
# ss=hashlib.md5('eeee'.encode('utf-8')).hexdigest()
# print(ss)

# def get_full_name(first_name:str, last_name:str):
#     full_name=first_name.title()+" "+last_name.title()
#     return full_name

# print(get_full_name("jos",333))

# class Person:
#     def __init__(self) -> None:
#         pass

#     def getAge(self):
#         print(__name__)

# p=Person().getAge()        


# def slicing(value, index=1, size=1000):
#     if not (str(index).isdigit() and int(index) > 0):
#         index = 1
#     if not (str(size).isdigit() and int(size) > 0):
#         size = 1000
#     if value:
#         index = int(index)
#         size = int(size)
#         try:
#             return value[(index - 1) * size:index * size]
#         except Exception:
#             raise TypeError("unable to slice:" + str(type(value)))
#     else:
#         return []


# ls=[1,5,6,58,8,5,8,5]
# print(slicing(ls,index=5,size=5))

from calendar import WEDNESDAY
import imp
from lib2to3.pgen2 import driver
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

		
    # 全局分页器对象
# def paginator():

#     return paginators=Paginator([1,2,3,4,5,6,7,8,9,10],3)

# print(Paginator.count) # 10  数据总数
# print(paginator.num_pages)  # 4  总页数
# print(paginator.page_range) # range(1, 5)  页码的列表

    # 单页对象
    # print(paginators.object_list)
    # page = paginators.page(1)
    # print(page.object_list)
# paginator()
# print(page.has_next())  # 是否有下一页
# print(page.next_page_number())  # 下一页的页码
# print(page.has_previous())  # 是否有上一页
# print(page.previous_page_number())  # 上一页的页码
#     # 取出单页对象的值
# print(page.object_list) # [4, 5, 6]
# for i in page:
# #     print(i)

# def paginator(value,index=1,page_size=5):
#     fenye=Paginator(value,page_size)
#     if index==0:
#         return fenye.object_list 
#     else:
#         page=fenye.page(index)
#         return page.object_list

ls=[1,2]
# print(paginator(ls,0))

ss=[x*x for x in range(1,11)]
# print(ss)

def multi():
    # print(lambda x : i*x for i in range(4))
    return [lambda x : i*x for i in range(4)]
# print([m(3) for m in multi()])
# for m in multi():
    # print(multi()[1](3))
    # print(m(3))
# print(multi(3))
# s=list(filter(lambda x: x % 2 == 0, range(10)))
# print(s)

# ss=reduce

# import math 
# print(math.ceil(3456/10))

def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))
 
def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))
 
def non_increasing(L):
    return all(x>=y for x, y in zip(L, L[1:]))
 
def non_decreasing(L):
    return all(x<=y for x, y in zip(L, L[1:]))
 
def monotonic(L):
    return non_increasing(L) or non_decreasing(L)

ls=[1,2,5,6,8]


def switch_case(value):
    switcher = {
        0: "zero",
        1: "one",
        2: "two",
    }
     
    return switcher.get(value, 'wrong value')


ss=switch_case(2)
ss=ss.upper()
print(ss)

class PAGE:
    def test_1(self,l1):
        print(l1)

    def test_2(self,l2):
        print(l2)


# PAGE().test_1(s)

def add(func):
    def fun(*args, **kwargs):
        print("装饰器的功能代码：登录")
        return func(*args,**kwargs)
    return fun


@add  # MyClass=add(MyClass)
class MyClass:
    def __init__(self,name,age):
      self.name=name
      self.age=age

m = MyClass("qinghan","18")
print("m的值：",m)