import os,sys
from ETL import ETL

etl1 = ETL({"pmonth":"2018-12"})
etl1.run("proc_statis_section_work")