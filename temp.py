import requests
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import base64
import csv

p_headers = {'Content-Type': 'application/soap+xml;charset=UTF-8',
             'Content-Length': '1595',
             'Host': 'eckvdev-test.fa.us2.oraclecloud.com:443',
             'Connection': 'Keep-Alive',
             'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
             'Authorization': 'Basic '}
l_url = 'http://eckvdev-test.fa.us2.oraclecloud.com/'
p_payload = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:pub="http://xmlns.oracle.com/oxp/service/PublicReportService">
   <soap:Header/>
   <soap:Body>
      <pub:runReport>
         <pub:reportRequest>
            <pub:attributeFormat>xml</pub:attributeFormat>
            <pub:flattenXML>true</pub:flattenXML>
            <pub:parameterNameValues>
               <!--Zero or more repetitions:-->
               <pub:item>
                  <pub:label>p_query0</pub:label>
                  <pub:name>p_query0</pub:name>
                  <pub:values>
                     <!--Zero or more repetitions:-->
                     <pub:item>select%20*%20from%20ar_collectors</pub:item>
                  </pub:values>
               </pub:item>
               <pub:item>
                  <pub:label>p_log</pub:label>
                  <pub:name>p_log</pub:name>
                  <pub:values>
                     <!--Zero or more repetitions:-->
                     <pub:item>F</pub:item>
                  </pub:values>
               </pub:item>
               <pub:item>
                  <pub:label>p_count</pub:label>
                  <pub:name>p_count</pub:name>
                  <pub:values>
                     <!--Zero or more repetitions:-->
                     <pub:item>50</pub:item>
                  </pub:values>
               </pub:item>
            </pub:parameterNameValues>
            <pub:reportAbsolutePath>/Custom/Gunjan/GUN_OUT_RPT.xdo</pub:reportAbsolutePath>
         </pub:reportRequest>
      </pub:runReport>
   </soap:Body>
</soap:Envelope>"""

r = requests.post(l_url,data=p_payload, headers=p_headers)
print(r.status_code)
