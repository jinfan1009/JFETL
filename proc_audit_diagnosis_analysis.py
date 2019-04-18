import os,sys
from ETL import ETL
etl1 = ETL({"pmonth":"2018-11"})
etl1.run("proc_audit_diagnosis_analysis")

etl2 = ETL({"pmonth":"2018-11"})
etl2.run("proc_audit_diagnosis_violation_detail")


