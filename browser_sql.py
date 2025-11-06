import requests
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import base64
import csv
#p_user = 'sysadmin'
#p_pass = 'Welcome1'
#p_instance = {}
p_log = False
q_thres = 3000
tag = '<ns2:reportBytes>'
tage = '</ns2:reportBytes>'
tagerr = '<env:Text xml:lang="en-US">'
tagerre = '</env:Text>'
tagte = 'failed: '
api = 'xmlpserver/services/ExternalReportWSSService'
#url = "https://fa-emvb-saasfaprod1.fa.ocs.oraclecloud.com:443/xmlpserver/services/ExternalReportWSSService"
#p_query="select%20*%20from%20poz_suppliers%20where%20rownum%232"
p_tab = [['\r\n','%0D'],['\n','%0D'],['>','%3E'],['<','%3C'],[' ','%20']]

def read_config():
    #global p_instance
    p_instance= ''
    l_err=False
    l_msg = ''
    try:
        aa = open('instance.config','r')
    except:
        l_msg='No config file present'
        l_err = True
    if not l_err:
        try:
            ac=csv.reader(aa)
            p_instance = {rows[0]:rows[1] for rows in ac}
        except:
            l_msg='Invalid config file'
            l_err = True
    return [l_err,l_msg,p_instance]
        
def get_payload(p_query,p_o_log,p_count):
    temp_query=""
    q_len = len(p_query)
    q_count = (q_len//q_thres)+1
    #print(p_o_log)
    for i in range(0,q_count):
        temp_query = temp_query +  """<pub:item>
                  <pub:label>p_query"""+str(i)+"""</pub:label>
                  <pub:name>p_query"""+str(i)+"""</pub:name>
                  <pub:values>
                     <!--Zero or more repetitions:-->
                     <pub:item>"""+p_query[q_thres*i:q_thres*(i+1)]+"""</pub:item>
                  </pub:values>
               </pub:item>"""
    return """
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:pub="http://xmlns.oracle.com/oxp/service/PublicReportService">
   <soap:Header/>
   <soap:Body>
      <pub:runReport>
         <pub:reportRequest>
            <pub:attributeFormat>xml</pub:attributeFormat>
            <pub:flattenXML>true</pub:flattenXML>
            <pub:parameterNameValues>
               <!--Zero or more repetitions:-->
               """+temp_query+"""
               <pub:item>
                  <pub:label>p_log</pub:label>
                  <pub:name>p_log</pub:name>
                  <pub:values>
                     <!--Zero or more repetitions:-->
                     <pub:item>"""+p_o_log+"""</pub:item>
                  </pub:values>
               </pub:item>
               <pub:item>
                  <pub:label>p_count</pub:label>
                  <pub:name>p_count</pub:name>
                  <pub:values>
                     <!--Zero or more repetitions:-->
                     <pub:item>"""+p_count+"""</pub:item>
                  </pub:values>
               </pub:item>
            </pub:parameterNameValues>
            <pub:reportAbsolutePath>/Custom/Gunjan/GUN_OUT_RPT.xdo</pub:reportAbsolutePath>
         </pub:reportRequest>
      </pub:runReport>
   </soap:Body>
</soap:Envelope>
"""

def validate_query(p_query):
    global p_log
    if p_log:
        print('Inside validate')
    err_f = False
    err_msg = ''
    aa_query = str(p_query.strip())
    if (aa_query[len(aa_query)-1:len(aa_query)] == ';'):
        if p_log:
            print('Query Error: Query has ; at the end.')
        err_f = True
        err_msg = "Query cannot end with ;"
    if not err_f:
        for i in p_tab:
            aa_query = aa_query.replace(i[0],i[1])
        if p_log:
            print('Query: Filtered caharacters')
    return [err_f,err_msg,aa_query]

def get_headers(p_user,p_pass,p_payload,p_host):
    return {
        "Content-Type": "application/soap+xml;charset=UTF-8",
           "Content-Length":str(len(p_payload)),
           "Host":p_host+":443",
           "Connection":"Keep-Alive",
           "User-Agent":"Apache-HttpClient/4.1.1 (java 1.5)",
           "Authorization":"Basic "+base64.b64encode((p_user+":"+p_pass).encode('utf-8')).decode('utf-8')
        }

def run_report(p_payload,p_headers,p_url):
    global p_log
    global api
    err_f = False
    #print(p_payload)
    err_msg = ""
    l_url=''
    if (p_url[-1:]=='/'):
        l_url = p_url+api
    else:
        l_url = p_url+'/'+api
    try:
        r = requests.post(l_url,data=p_payload, headers=p_headers)
        if p_log:
            print('Report: Request executed wit status: '+ str(r.status_code))
        s_code = r.status_code
        aa=str(r.content.decode('utf-8'))
        #print(p_payload)
        #print(l_url)
        #print(aa)
        r.close()
    except Exception as e:
        if p_log:
            print('Report: Request Error: '+str(e))
        err_f = True
        err_msg = "Fusion Server Error with code: "+str(e)
    #tree=ET.ElementTree(ET.fromstring(str(aa)))
    #root = tree.getroot()
    #print(str(aa))
    #print(tree.text)
    #for i in root.findall('{http://www.w3.org/2003/05/soap-envelope}Body'):
        #'ns2:reportBytes'):
     #   print(i.)
    if r.status_code == 200:
        if p_log:
            print(aa)
        r_bytes = aa[aa.find(tag)+len(tag):aa.find(tage)]
        try:
            report_xml=base64.b64decode(r_bytes).decode('utf-8')
            if p_log:
                print('Report: Bytes read.')
        except Exception as e:
            if p_log:
                print('Report: Report Call failurre: '+str(r_bytes))
            err_f = True
            err_msg = "Error getting report data. {Invalid retportBytes}"
        return [err_f,err_msg,report_xml]
    else:
        err_f = True
        err_msg = "Query Execution Failed: "
        r_bytes = aa[aa.find(tagerr)+len(tagerr):aa.find(tagerre)]
        if r_bytes.find(tagte)>-1:
            r_bytes = r_bytes[r_bytes.find(tagte)+len(tagte):len(r_bytes)]
        return [err_f,r_bytes,None]
    #print(aa.find('reportBytes'))
    #print(aa.find('reportBytes',aa.find('reportBytes')+1))


def b_main(p_query,l_log,p_o_log,p_count,p_url,p_user,p_password):
    global p_log
    p_log=l_log
    err_msg = ""
    err_f = False
    f_payload=''
    if p_url == '' or p_url == None or p_user == '' or p_user == None or p_password == '' or p_password == None:
        err_f= True
        err_msg = "Please select correct instance or Please enter username or password."
        return [err_f,err_msg,None]
    val = validate_query(p_query)
    if val[0]:
        if p_log:
            print('Main: Validate error: '+val[1])
        err_f = True
        err_msg = "Main: Query Validation failed with error: "+val[1]
        return [err_f,err_msg,None]
    else:
        if p_log:
            print('Main: Validated.')
        f_payload = get_payload(val[2],p_o_log,p_count)
        if p_log:
            print(f_payload)
        if p_log:
            print('Main: got payload')
        f_headers = get_headers(p_user,p_password,f_payload,'{uri.netloc}'.format(uri=urlparse(p_url)))
        if p_log:
            print('Main: Got headers')
        runr = run_report(f_payload,f_headers,p_url)
        #print(f_headers,p_url)
        if p_log:
            print(runr[2])
        if runr[0]:
            if p_log:
                print('Main: Validate error: '+val[1])
            err_f = True
            err_msg = "Main: Report Execution Failed: "+runr[1]
            return [err_f,err_msg,None]
        else:
            return [err_f,err_msg,runr[2]]
