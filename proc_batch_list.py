import os,sys
from ETL import ETL

def single_proc(actionName,month):
    etl1 = ETL({"pmonth": month})
    etl1.run(actionName)
    print("%s  %s  process completed!"%(month,actionName))

def  run():
    monthli = [ '2018-01','2018-02','2018-03', '2018-04','2018-05','2018-06','2018-07','2018-08', '2018-09','2018-10','2018-11','2018-12']
    for  i in range(0,len(monthli)):
        month = monthli[i]

        #single_proc("proc_audit_dept_analysis",month)
        #single_proc("proc_audit_dept_violation_detail", month)
        #single_proc("proc_audit_diagnosis_analysis", month)
        #single_proc("proc_audit_diagnosis_violation_detail", month)
        #single_proc("proc_audit_doctor_analysis", month)
        #single_proc("proc_audit_doctor_violation_detail", month)
        #single_proc("proc_audit_item_analysis", month)
        #single_proc("proc_audit_rule_analysis", month)
        #single_proc("proc_audit_rule_violation_detail", month)
        #single_proc("proc_statis_month_inoutpatient_charge_avg", month)
        #single_proc("proc_statis_month_order_count_amount", month)
        #single_proc("proc_statis_month_violation_detail", month)
        #single_proc("proc_statis_project_development_violation", month)
        #single_proc("proc_statis_rules_violation_amount", month)
        #single_proc("proc_statis_rules_violation_count", month)
        #single_proc("proc_statis_section_work", month)
        #single_proc("proc_statis_service_project_frequency", month)

        #single_proc("proc_audit_all_analysis", month)
        #single_proc("proc_audit_service_record", month)
        single_proc("proc_statis_project_development_item", month)

        #single_proc("proc_statis_service_project_violation", month)
        #single_proc("", month)
        #single_proc("", month)




run()