# -*- coding: utf-8 -*-
##  ETL frameworks
import os,sys
import json
import plistlib
from DBtools import  DB

####创建实例
def createInstance(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj
####实体类
class Model:
	def __init__(self):
		pass

class INPUTBLOCK:
	def __init__(self,inputsql,inputmappingconfig,input_paras,preparesqllist):
		self.inputsql = inputsql
		self.inputdata =None
		self.mappingconfig = inputmappingconfig
		self.input_paras = input_paras
		self.proceedInputSql = None
		self.preparesqllist = preparesqllist

	#####更新输入参数到系统中
	def  updateInputParas(self,updatedParasdt):
		for key in self.input_paras.keys():
			if  key in  updatedParasdt:
				self.input_paras[key] = updatedParasdt[key]

	#####替换配置文件里面的参数
	def makeProceedInputSql(self):
		self.proceedInputSql = self.inputsql
		for key in self.input_paras.keys():
			self.proceedInputSql = self.proceedInputSql.replace("{%s}"%(key),self.input_paras[key])
	##### 替换预处理SQL里面的参数
	def makePrepareSqllist(self):
		li = []
		for preparesql in self.preparesqllist:
			sql = preparesql
			for key in self.input_paras.keys():
				sql = sql.replace("{%s}"%(key),self.input_paras[key])
			li.append(sql)
		self.preparesqllist = li
	##### 预处理 sql并执行
	def makePrepareSqllistAndExe(self):
		self.makePrepareSqllist()
		db = DB()
		for preparesql  in self.preparesqllist:
			db.update_trans(preparesql)
		db.commit()
		db.close()




	def getInputData(self):
		self.makeProceedInputSql()

		db = DB()
		r = db.query(self.proceedInputSql)
		self.inputdata = r
		db.close()
	#####设置结果对象的属性和值
	def setAttr(self,row):
		obj = Model()
		for key in self.mappingconfig.keys():
			t_key = key
			if  t_key.isdigit()== True:t_key = int(key)
			obj.__setattr__( self.mappingconfig[key],row[ t_key ] )
		m=''
		return obj
	def mapping(self):
		li = []
		for row in self.inputdata:
			obj = self.setAttr(row)
			li.append(obj)
		self.inputdata = li
		s =""


		
class OUTPUTBLOCK:
	def __init__(self,outputconfig):
		self.outputconfig = outputconfig
		self.outputsql = self.outputconfig["outputsql"]
		self.mappingconfig = self.outputconfig["output_field_mapping"]
		self.outputdata = []

	def makeOutputSql(self,obj):
		proceedOutputSql = self.outputsql
		for  key in self.mappingconfig.keys():
			value = self.mappingconfig[key]
			proceedOutputSql = proceedOutputSql.replace('{%s}'%(key),getattr(obj,value))
		self.outputdata.append(proceedOutputSql)



	def getOutputData(self,inputdata):
		for obj in inputdata:
			self.makeOutputSql(obj)
			m = ''



	def loadOutputData(self):
		db = DB()
		for sql in self.outputdata:
			db.update_trans(sql)
		db.commit()
		db.close()
		

class PROCESS:
	def __init__(self,actionname):
		self.processname = actionname
		#module = __import__('process_scripts.%s'%(actionname))
		proc_class = createInstance('process_scripts.%s'%(actionname),actionname)
		self.procobj = proc_class

		
class ETL:
	def  __init__(self,paras_dt):
		self.setting = None
		self.inputblock = None
		self.outputblock = None
		####入参
		self.paras_dt = paras_dt
		self.processlist =[]
	def makeINPUTBLOCK(self):
		self.inputblock = INPUTBLOCK(
			self.setting["input"]["inputsql"],
			self.setting["input"]["input_field_mapping"],
			self.setting["input"]["input_paras"],
			self.setting["input"]["preparesqllist"],
		)
		####更新输入参数到系统
		self.inputblock.updateInputParas(self.paras_dt)
		####预处理sql参数替换，并执行替换后的sql语句
		self.inputblock.makePrepareSqllistAndExe()
		self.inputblock.getInputData()
		self.inputblock.mapping()
	def makePROCESSLIST(self):
		procli = self.setting["process"]["processlist"]
		for actionname in procli:
			proc = PROCESS(actionname)
			self.processlist.append(proc)

	def makeOUTPUTBLOCK(self):
		self.outputblock = OUTPUTBLOCK(self.setting["output"])
		self.outputblock.getOutputData(self.inputblock.inputdata)
		self.outputblock.loadOutputData()

	#######执行正常的E T L 流程（提取，转换，加载）
	def run(self,settingfilename):
		#f = open("settings/%s.json"%(settingfilename),"rb")
		#fb = f.read()
		#s = fb.decode( encoding="utf8")
		#settingdt =  json.loads(s)
		settingdt ={}
		with open("settings/%s.plist" % (settingfilename), 'rb') as fp:
			settingdt = plistlib.load(fp)
		self.setting = settingdt
		self.makeINPUTBLOCK()
		self.makePROCESSLIST()
		for proc in self.processlist:
			proc.procobj.proc(self.inputblock)
		self.makeOUTPUTBLOCK()

	#######执行ET 流程（提取，转换）
	def runET(self,settingfilename):
		with open("settings/%s.plist" % (settingfilename), 'rb') as fp:
			settingdt = plistlib.load(fp)
		self.setting = settingdt
		self.makeINPUTBLOCK()
		self.makePROCESSLIST()
		for proc in self.processlist:
			proc.procobj.proc(self.inputblock)


	#######执行TL 流程（转换，加载）
	def  runTL(self,settingfilename,inputdata):
		with open("settings/%s.plist" % (settingfilename), 'rb') as fp:
			settingdt = plistlib.load(fp)
		self.setting = settingdt
		self.makeINPUTBLOCK()
		self.makePROCESSLIST()
		for proc in self.processlist:
			proc.procobj.proc(inputdata)
		self.makeOUTPUTBLOCK()


	def  makeInitConfig(etlname):
		configdt ={
			'input':{
				'inputsql':'',
				'preparesqllist':[''],
				'input_field_mapping':{'0':''},
				'input_paras':{'pmonth':'2018-12'}
			},
			'output':{
				'outputsql':'',
				'output_field_mapping':{'0':''},
				'output_paras':{}
			},
			'process':{
				'processlist':['Value2String']
			}
		}
		####write to plist file
		with open("settings/%s.plist"%(etlname), 'wb') as fp:
			plistlib.dump(configdt,fp)




