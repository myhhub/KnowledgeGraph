#!/usr/bin/env python
# coding=utf-8

import requests
import commands
import math
from tqdm import tqdm
from xml.etree import ElementTree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--fuseki', type=str, 
                    default='/home1/peng/project/apache-jena-fuseki-3.7.0/', help='Path to fuseki-server')
parser.add_argument('--baiduNt', type=str ,
                  default="/home1/peng/project/d2rq-0.8.1/full_nt/baidu_baike.nt" , help='Path to baidu N-triples ')
parser.add_argument('--hudongNt', type=str ,
                  default="/home1/peng/project/d2rq-0.8.1/full_nt/hudong_baike.nt" , help='Path to hudong N-triples')
parser.add_argument('--maxNtLength', type=float ,
                  default=5000000.0 , help='Max N-triples in each nt file')
parser.add_argument('--ip', type=str ,
                  default='localhost' , help='Ip for Fuseki and Silk server')
parser.add_argument('--projectName', type=str ,
                  default='baike' , help='Silk project name')
args = parser.parse_args()

class SilkCmd(object):
    def __init__(self):
        self.header_dict = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
                   'Accept': '*/*',
                   'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'X-Requested-With': 'XMLHttpRequest',
                   'DNT': '1',
                   'Connection': 'keep-alive',
                   'Pragma': 'no-cache',
                   'Cache-Control': 'no-cache',
                  }
    def control_linking(self, ip=args.ip, project_name=args.projectName,
                        task_name="baike_test", action="start"):
        '''
        Control linking task
        :ip IP for sile server type: string
        :project_name type: string disc: the project name in silk
        :task_name linking task name type: string
        :return execute result
        '''
        url = "http://{}:9000/workspace/projects/{}/tasks/{}/activities/ExecuteLinking/{}".format(ip, project_name, task_name, action)
        res = requests.post(url, json = {}, headers=self.header_dict)
        return res.text
    
    def build_task(self, ip=args.ip, project_name=args.projectName,
                   task_name="baike_test", source_data="baidu_50",
                   target_data="hudong_50", output_data="output"):
        url = "http://{}:9000/workspace/projects/{}/tasks".format(ip, project_name)
        data_dict = {"id":task_name,
                     "data":{"taskType":"Linking",
                             "source":{"inputId":source_data,"typeUri":"","restriction":""},
                             "target":{"inputId":target_data,"typeUri":"","restriction":""},
                             "outputs":[output_data]}}
        res = requests.post(url, json = data_dict, headers=self.header_dict)
        return res.text

    def build_endPoint(self, data_name, endpointURI, pageSize, ip=args.ip, project_name=args.projectName):
        url = "http://{}:9000/workspace/projects/{}/tasks".format(ip, project_name)
        data_dict = {"id":data_name,
                     "data":{"taskType":"Dataset","type":"sparqlEndpoint",
                             "uriProperty":"",
                             "parameters":{"endpointURI":str(endpointURI),
                                           "login":"","password":"","graph":"","pageSize":pageSize,
                                           "entityList":"","pauseTime":"0","retryCount":"3",
                                           "retryPause":"1000","queryParameters":"","strategy":"parallel",
                                           "useOrderBy":"true","clearGraphBeforeExecution":"true"}}}
        res = requests.post(url, json = data_dict, headers=self.header_dict)
        return res.text

    def build_rdf(self, data_name, input_data, maxReadSize = "100000", ip=args.ip, project_name=args.projectName):
        url = "http://{}:9000/workspace/projects/{}/tasks".format(ip, project_name)
        data_dict = {"id":data_name,
                     "data":{"taskType":"Dataset","type":"file",
                             "uriProperty":"",
                             "parameters":{"file":input_data,"format":"N-Triples",
                                           "graph":"","maxReadSize":maxReadSize,"entityList":""}}}
        res = requests.post(url, json = data_dict, headers=self.header_dict)
        return res.text
    
    def build_output(self, data_name, ip=args.ip, project_name=args.projectName):
        url = "http://{}:9000/workspace/projects/{}/resources/{}".format(ip, project_name, data_name)
        res = requests.put(url, data = {}, headers=self.header_dict)
        return res.text

    def add_prefix(self, prefixes, project_name="baike", ip="10.3.10.194"):
        url = "http://{}:9000/workspace/projects/{}/prefixes".format(ip, project_name)
        data_dict = {"owl": "http://www.w3.org/2002/07/owl#",
                    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                     "rdfs": "http://www.w3.org/2000/01/rdf-schema#"}
        for prefix in prefixes:
            print("prefix: ", prefix)
            data_dict[prefix] = prefixes[prefix]
        res = requests.put(url, data = data_dict, headers=self.header_dict)
        return res.text

    def add_rule(self, rule, project_name="baike", task_name="baike_test", ip="10.3.10.194"):
        url = "http://{}:9000/linking/tasks/{}/{}/rule".format(ip, project_name, task_name)
        header_dict = self.header_dict
        header_dict["Content-Type"] = " text/xml;charset=UTF-8"
#        data = '<LinkageRule linkType="owl:sameAs"><Compare metric="levenshteinDistance" id="levenshteinDistance1" required="false" threshold="0.0" weight="1"><TransformInput function="lowerCase" id="lowerCase1"><Input path="baidu:lemmas_disambi" id="sourcePath1"/></TransformInput><TransformInput function="lowerCase" id="lowerCase2"><Input path="hudong:lemmas_disambi" id="targetPath1"/></TransformInput><Param name="minChar" value="0"/><Param name="maxChar" value="z"/></Compare><Filter/></LinkageRule>'
        res = requests.put(url, data = rule, headers=header_dict)
        return res.text

    def control_project(self, project_name="baike", ip="10.3.10.194", action="PUT"):
        url = "http://{}:9000/workspace/projects/{}".format(ip, project_name)
        if action == "PUT":
            res = requests.put(url, data = {}, headers=self.header_dict)
        elif action == "DELETE":
            res = requests.delete(url, data = {}, headers=self.header_dict)
        return res.text


class JenaCmd(object):
    def __init__(self):
        self.header_dict = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
                   'Accept': '*/*',
                   'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'X-Requested-With': 'XMLHttpRequest',
                   'DNT': '1',
                   'Connection': 'keep-alive',
                   'Pragma': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cache-Control': 'no-cache',
                  }
    def add_tdb(self, ip="10.3.10.194", dbName="kg_test"):
        url = "http://{}:3030/$/datasets".format(ip)
        data_dict = {'dbName': dbName,
                     'dbType': 'tdb'}
        res = requests.post(url, data = data_dict, headers=self.header_dict)
        return res.text

    def delete_tdb(self, ip="10.3.10.194", dbName="kg_test"):
        url = "http://{}:3030/$/datasets/{}".format(ip, dbName)
        res = requests.delete(url, data = {}, headers=self.header_dict)
        return res.text

    @staticmethod
    def load_nt(tdb_path, nt_path, jena_path="/home1/peng/project/apache-jena-3.7.0/bin"):
        status, out = commands.getstatusoutput('sh {}/tdbloader --loc="{}" "{}"'.format(jena_path, tdb_path, nt_path))
        print(out)
        return status

def seg_nt(source_nt, max_len=5000000.0):
    out_file_list = []
    _, total_line = commands.getstatusoutput("wc -l {}".format(source_nt))
    total_line = total_line.split()[0]
    seg_file_name = source_nt.strip(".nt")
    print("total_line: ", type(total_line), total_line, math.ceil(float(total_line) / max_len))
    for i in tqdm(range(int(math.ceil(float(total_line)/max_len)))):
        ith_file_name = seg_file_name + "_" + str(i) + ".nt"
        status, _ = commands.getstatusoutput("sed -n '{},{}p' {} > {}".format(int(max_len*(i)+1), int(max_len*(i+1)), source_nt, ith_file_name))
        if status == 1:
            raise Exception("Error when segment file {}".format(ith_file_name))
        out_file_list.append(ith_file_name)
    return out_file_list



if __name__ == "__main__":
    sm = SilkCmd()
    dname = "baidu_11_0"
#    prefixes = {"baidu": "http://www.kgbaidu.com#",
#                "hudong": "http://www.kghudong.com#"}
#    print sm.add_prefix(prefixes)
#    print sm.add_rule()
#    print sm.build_endPoint("baike", dname, "http://10.3.10.194:3030/{}/query".format(dname), "500000")
#    print sm.build_output("baike", "safaasfsasfaf.nt")
#    print sm.control_linking(project_name="baike", task_name="t_hudong_11_0baidu_11_0")
#    print sm.control_project(project_name="baike")
#    print sm.control_project(project_name="baike", action="DELETE")
#    jm = JenaCmd()
#    jm.delete_tdb(dbName="hudong_11_2")

