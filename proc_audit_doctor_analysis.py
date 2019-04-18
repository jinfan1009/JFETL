import os,sys
from ETL import ETL
etl1 = ETL({"pmonth":"2018-12"})
etl1.run("proc_audit_doctor_analysis")

etl2 = ETL({"pmonth":"2018-12"})
etl2.run("proc_audit_doctor_violation_detail")