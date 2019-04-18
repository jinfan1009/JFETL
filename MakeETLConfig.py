import os,sys
import ETL
def run():
    configname = input("input config name：")
    ETL.ETL.makeInitConfig(configname)
    print(configname+"  created completed!")
    input(">>>")
run()