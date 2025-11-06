from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import os
import browser_sql
import time
import export_excel

p_log = False
tab_dict = {"Tab1":"Tab1"}
con_dict = {"Tab1":{"query":'test query',"table":'','time':'',"instance":'','username':'','password':''}}
active_tab = "Tab1"
tab_count=1
p_o_log = 'T'
p_instance={}
def refresh_instance():
    global p_instance
    p_instance = browser_sql.read_config()[2]
def get_table(p_xml):
    root= ET.fromstring(p_xml)
    table_html = """ <table class = "style1" border="1">
"""
    t_flag = True
    for type_tag in root.findall('ROW'):
        if t_flag:
            table_html = table_html + """<tr>
"""
            for i in type_tag.iter():
                 table_html = table_html+"""
<th >"""+i.tag+"""
</th>
"""
            table_html = table_html+ """
</tr>"""
            t_flag=False
        table_html = table_html + """
<tr>
"""
        for i in type_tag.iter():
            if i.text !=None:
                table_html = table_html+"""
<td>"""+i.text+"""
</td>
"""
            else:
                table_html = table_html+"""
<td>null
</td>
"""
        table_html = table_html + """
</tr>
"""
    table_html = table_html+"""
</table>"""
    #print(table_html)
    return table_html
    #print(os.getcwd())
    


app = Flask(__name__,template_folder = os.getcwd(),static_url_path='/static')

@app.route("/")
def home():
    global p_instance
    global con_dict
    refresh_instance()
    #print(p_instance)
    if p_log:
        print('rendering')
    return render_template('json.html',tab_dict = tab_dict,con_dict =con_dict, active_tab = active_tab,p_instance = p_instance )


@app.route("/tabadd",methods=['GET','POST'])
def tabadd():
    global p_instance
    #print('Add')
    global tab_dict
    global con_dict
    global tab_count
    global active_tab
    refresh_instance()
    if p_log:
        print('Add1')
    tab_count = tab_count+1
    if p_log:
        print('Add2')
    tab_dict["Tab"+str(tab_count)] = "Tab"+str(tab_count)
    if p_log:
        print('Add3')
    con_dict["Tab"+str(tab_count)] = {"query":'<test query>',"table":'','time':'','instance':'','username':'','password':''}
    if p_log:
        print('Add4')
    active_tab = "Tab"+str(tab_count)
    if p_log:
        print('Add5')
    return render_template('json.html',tab_dict = tab_dict,con_dict =con_dict, active_tab = active_tab,p_instance = p_instance )

@app.route("/tabsub/<tabname>",methods=['GET','POST'])
def tabsub(tabname):
    global p_instance
    global tab_dict
    global con_dict
    global active_tab
    refresh_instance()
    active_tab = tabname
    tab_dict.pop(tabname)
    con_dict.pop(tabname)
    return render_template('json.html',tab_dict = tab_dict,con_dict =con_dict, active_tab = active_tab,p_instance = p_instance )


@app.route('/qExec/<tabname>',methods=['GET','POST'])
def qExec(tabname):
    #print('Start')
    global con_dict
    global p_instance
    global p_log
    global active_tab
    refresh_instance()
    active_tab = tabname
    if p_log:
        print('Work')
        print(tabname)
    t1 = time.time()
    s_query = request.form[tabname+'_gunText']
    s_instance = request.form[tabname+'_instance']
    s_username = request.form[tabname+'_userName']
    s_password = request.form[tabname+'_password']
    s_name = request.form[tabname+'_fileName']
    #print(s_instance,s_username,s_password)
    if p_log:
        print('query')
    p_count = request.form[tabname+'_gunCount']
    if p_log:
        print('count')
    if p_count is None or p_count =='':
        p_count='50'
    try:
        lcheck = request.form[tabname+'_gunLog']
        #print(lcheck)
        if p_log:
            print('check')
    except:
        lcheck = 'F'
    if lcheck is None or lcheck =="":
        lcheck='F'
    if p_log:
        print(lcheck)
    #ax = open("abc.xml",'r')
    #h_table=get_table(str(ax.read()))
    #ax.close()
    if s_query.strip() is not None and  s_query.strip() !="":
        #print('1')
        #export_excel.backup_query(s_query.strip(),s_instance)
        b_res = browser_sql.b_main(s_query,p_log,lcheck,p_count,p_instance[s_instance],s_username,s_password)
    else:
        con_dict[tabname]["query"] =  s_query.strip()
        con_dict[tabname]["table"] =  "<font color=red><b> Error:<br>Query is empty</b></font>"
        con_dict[tabname]["time"] =  ""
        con_dict[tabname]["instance"] =  s_instance
        con_dict[tabname]["username"] =  s_username
        con_dict[tabname]["password"] =  s_password
        return render_template('json.html',con_dict = con_dict, tab_dict = tab_dict, active_tab = active_tab,p_instance = p_instance)
    t2 = time.time()
    if p_log:
        print('Got XML')
    if b_res[0]:
        if p_log:
            print("Error")
            print(b_res[1])
        con_dict[tabname]["query"] =  s_query.strip()
        con_dict[tabname]["table"] =  "<font color=red><b> Error:<br>"+b_res[1]+"</b></font>"
        con_dict[tabname]["time"] =  ""
        con_dict[tabname]["instance"] =  s_instance
        con_dict[tabname]["username"] =  s_username
        con_dict[tabname]["password"] =  s_password
        return render_template('json.html',con_dict = con_dict, tab_dict = tab_dict, active_tab = active_tab,p_instance = p_instance)
    else:
        if lcheck =='F':
            #print('1')
            export_excel.backup_query(s_query.strip(),s_instance)
            con_dict[tabname]["query"] =  s_query.strip()
            con_dict[tabname]["table"] =  get_table(b_res[2])
            con_dict[tabname]["time"] =  "Query Execution Time: "+str(round(t2-t1,2))
            con_dict[tabname]["instance"] =  s_instance
            con_dict[tabname]["username"] =  s_username
            con_dict[tabname]["password"] =  s_password
            return render_template('json.html',con_dict = con_dict, tab_dict = tab_dict, active_tab = active_tab, p_instance = p_instance)
        else:
            
            t_err=export_excel.main(b_res[2],s_name.strip())
            #print('1')
            export_excel.backup_query(s_query.strip(),s_instance)
            con_dict[tabname]["query"] =  s_query.strip()
            #con_dict[tabname]["table"] =  get_table(b_res[2])
            if t_err:
                con_dict[tabname]["time"] =  "File saved Successfuly. Query Execution Time: "+str(round(t2-t1,2))
            else:
                con_dict[tabname]["table"] =  "Employee_Create.py</b></font>"
            con_dict[tabname]["instance"] =  s_instance
            con_dict[tabname]["username"] =  s_username
            con_dict[tabname]["password"] =  s_password
            return render_template('json.html',con_dict = con_dict, tab_dict = tab_dict, active_tab = active_tab, p_instance = p_instance)
    #print('Working')
    
    
if __name__ == "__main__":
    if p_log:
        print('Start')
    app.run()
    #aa = open('abc.xml','r')
    #ac=aa.read()
    #aa.close()
    #root = ET.parse('abc.xml').getroot()



