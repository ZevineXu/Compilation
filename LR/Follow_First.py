from .product import *
from .project import *
from .util import *
from .pattern import *
from LL.products import Product as LLProduct
from LL.util import getFirst as Lgenerate_First
import re
from typing import List

def get_products_non_ter_list()->(List[Product],List[str]):
    f = open("LR/test.txt", "r")
    num = int(f.readline())
    products = [Product("E'->E")]
    for i in range(num):
        p = Product(f.readline())
        products.append(p)
    
    non_ter_list = []
    for p in products:
        if p.left not in non_ter_list:
            non_ter_list.append(p.left)

    return products,non_ter_list

class First:

    fs = None
    def __init__(self):
        self.first = {}
        self.products,self.non_ter_list = get_products_non_ter_list()
        for nt in self.non_ter_list:
            self.first[nt] = []
        
    # 生成First集
    def generate_First(self):
        for p in self.products:
            self._first1(p)
        
        for nt in self.non_ter_list:
            self._first2(nt)

        

    def _first1(self,p:Product):
        if re.match(pattern_ter,p.right[0]): # 这里默认产生式的右部如果有空串那么一定是右部只有一个元素即空串，即A->A'的形式
            self.first[p.left].append(p.right[0])
        else:
            self.first[p.left].append(p.right)

    def _first2(self,nt):
        if re.match(pattern_ter,nt):
            return [nt]
        posis = []
        for posi in range(len(self.first[nt])):
            ele = self.first[nt][posi]
            if type(ele) is list:
                i = 0
                l = []
                while i < len(ele):
                    if ele[i] == nt:
                        i+=1
                        continue
                    l1 = self._first2(ele[i])
                    if '~' in l1:
                        l1.remove('~')
                        l += l1
                        i += 1
                        if i==len(ele):
                            l.append('~')
                    else:
                        l += l1
                        break
                
                for e in l:
                    if e not in self.first[nt]:
                        self.first[nt].append(e)

                posis.append(posi)

        
        for i in range(len(posis)):
            posis[i] -= i
            del self.first[nt][posis[i]]
        return self.first[nt]

    @staticmethod
    def getInstance():
        if First.fs is None:
            fi = First()
            fi.generate_First()
            First.fs = fi.first
            return First.fs
        else:
            return First.fs



def generate_Follow():
    # f = open("LR/test.txt", "r")
    # num = int(f.readline())
    # products = [Product("E'->E")]
    # for i in range(num):
    #     p = Product(f.readline())
    #     products.append(p)

    products,non_ter_list = get_products_non_ter_list()

    


    f ={} # Follo集存放位置
    add = {} # 需要添加Follow集的
    fi = {} # 需要添加First集的


    for non_ter in non_ter_list:
        f[non_ter] = []
        add[non_ter] = []
        fi[non_ter]=[]
    f["E'"] = ['$']


    for p in products:
        for alpha in range(len(p.right)):
            # 终结符直接加入Follow集
            if alpha + 1 < len(p.right) and re.match(pattern_ter ,p.right[alpha+1]) and re.match("[A-Z]",p.right[alpha]):
                f[p.right[alpha]].append(p.right[alpha+1])
            # 假如说右端是非终结符，那么将右端符号添加进入fi中
            elif alpha + 1 < len(p.right) and re.match("[A-Z]",p.right[alpha]) and re.match("[A-Z]",p.right[alpha+1]):
                fi[p.right[alpha]].append(p.right[alpha+1])
            # 假如符号是本产生式最后一个需要将产生式的左端添加到add中
            elif alpha == len(p.right)-1 and re.match("[A-Z]",p.right[alpha]):
                add[p.right[alpha]].append(p.left)







    for __ in range(2):
        for _ in range(len(non_ter_list)*2):
            for non_ter in non_ter_list:
                for add_non_ter in add[non_ter]:
                    f[non_ter]+=f[add_non_ter]

        for _ in range(len(non_ter_list)*2):
            for non_ter in non_ter_list:
                for add_non_ter in fi[non_ter]:
                    f[non_ter] += firstSingleton(add_non_ter)

    for i in f.keys():
        f[i] = list(set(f[i]))
    return f

def getFollow(ter):
    return generate_Follow()[ter]

def generate_First():
    f = open("LR/test.txt", "r")
    num = int(f.readline())
    products = [LLProduct("E'->E")]
    for i in range(num):
        p = LLProduct(f.readline())
        products.append(p)

    sources = Lgenerate_First(products)
    for k in sources.keys():
        sources[k] = list(sources[k].first)
    return sources

def get_First(ter):
    f = generate_First()
    return f[ter]


