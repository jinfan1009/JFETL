
import os,sys

##### 将结果全部转换成为字符串，以方便后期的输入加载
class  Value2String:
    def __init__(self):
        pass
    def proc(self,inputblock):
        for  obj in inputblock.inputdata:
            for  key in  inputblock.mappingconfig.values():
                s = str ( getattr(obj,key))
                setattr(obj , key , s)
