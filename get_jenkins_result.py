TEST_DOMAIN = {



	# idcevo_sop26v2_evt2
    'IDCEVO_SOP26_EVT2_Misc': ['idcevo_sop26v2_la_evt2_linux', 'idcevo_sop26v2_la_evt2_android', 'idcevo_sop26v2_la_evt2_python'],
    
}

import sys
import os
import re
import jenkins
from datetime import datetime


class CITestManager:
    def __init__(self, url, username, password, jobname, buildnum):
        self.url = url
        self.jobname = jobname.  #'CI_TEST'
        self.buildnum = buildnum #'516362'
        tfs_jenkins = jenkins.Jenkins(self.url, username=username, password=password)
        self.build_info = tfs_jenkins.get_build_info(jobname, buildnum, depth='2')
        self.jenkins_param = {}
        self.result_dict = {}
        self.suite_result_dict = {}
        self.suite = ''
        print("end of CITestManager_init")
       
    def get_test_info(self):
        # get jenkins parameter
        print("-exe get_test_info")
        build_info_action = [item for item in self.build_info['actions'] if item]
        action_parameters = next((item['parameters'] for item in build_info_action
                                if item.get('_class') == 'hudson.model.ParametersAction'), None)
        for param in action_parameters:
            self.jenkins_param[param['name']] = param['value']
            
        # test result
        detail_result = re.split(r'- UW.+ <br>\n', self.build_info['description'].strip())[1].split('<br>\n')
        for line in detail_result:
            each = re.split(r'(\w+)\/(.+) : (PASS|FAIL|Disable|NotTested)', line)
            try:
                sitl_number = re.search(r'.*[_-](\d+)\.', each[2])
                sitl_number = sitl_number.group(1)
            except AttributeError:
                sitl_number = ""
                    
            suite, tc, result = each[0] + each[1], f'SITL-{sitl_number}', each[3]
            if suite not in self.result_dict:
                self.result_dict[suite] = {}
            self.suite_result_dict[tc] = result
            self.result_dict[suite] = self.suite_result_dict
                
    def get_local_project_name(self):
        print("-exe get_local_project_name")
        build_project = []
        for local_project, jenkins_suites in TEST_DOMAIN.items():
            for suite in jenkins_suites:
                if self.jenkins_param['TARGET_PROJECT'] in suite:
                    build_project.append(local_project)
        return list(set(build_project))
    
    def create_csv_directory(self, ir_version, build_number):
        root_dir = 'E:/03.project/tc_manager/RegressionTest_LOG'
        try:
            csv_dir = os.path.join(root_dir, ir_version, build_number)
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)
            else:
                for file in os.listdir(csv_dir):
                    if file.endswith('.CSV'):
                        os.remove(os.path.join(csv_dir, file))
        except Exception as e:
            print(e)
            csv_dir = ''
        return csv_dir
        
    def create_auto_pass_directory(self, csv_dir, project):
        print("-exe create_auto_pass_directory")
        try:
            auto_pass_dir = os.path.join(csv_dir, project)
            if not os.path.exists(auto_pass_dir):
                os.makedirs(auto_pass_dir)
            else:
                for file in os.listdir(auto_pass_dir):
                    if file.endswith('.txt'):
                        os.remove(os.path.join(auto_pass_dir, file))
        except Exception as e:
            print(e)
            auto_pass_dir = ''
        return auto_pass_dir
        
    def make_auto_result_file(self, csv_dir):
        print("-exe make_auto_result_file")
        project_domain = self.get_local_project_name()
        for project in project_domain:
            result_csv = os.path.join(csv_dir, f'{project}_RESULT_LOG.CSV')
            auto_pass_dir = self.create_auto_pass_directory(csv_dir, project)
            
            cur_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
            for jenkins_suite in TEST_DOMAIN[project]:
                jsuite = jenkins_suite.split('_')[-1]
                for suite, tc_result in self.result_dict.items():
                    if jsuite == suite:
                        for tc, result in tc_result.items():
                            with open(result_csv, 'a', encoding='utf-8') as f:get_
                                f.writelines(f"{tc}.{result.capitalize()}.{cur_datetime}.{'0'}.{'0'}.{'autotest'}\n")
                            if result == 'PASS':
                                auto_log_txt = os.path.join(auto_pass_dir, f"{project}.{tc}.{result}.{cur_datetime}.{'0'}.{'autotest'}.Commlog.txt")
                                with open(auto_log_txt, 'w', encoding='utf-8') as txtfile:
                                    txtfile.write(f'{self.url}/job/{self.jobname}/{self.buildnum}/\n')
                                    
                                                                     
if __name__ == '__main__':
    print("—————————————— START ————————————-")
    url = 'http://12.81.225.104:8100'
    username = 'testworks'
    password = 'test2015!'
    jobname = 'CI_TEST'
    
    ir_buildnum = re.search(r'(\w+)#(\d+)', sys.argv[1])  # ex) IR260707#123456
    ir_version, build_number = ir_buildnum.group(1), ir_buildnum.group(2)
    ci_test = CITestManager(url, username, password, jobname, build_number)
    ci_test.get_test_info()
    
    csv_dir = ci_test.create_csv_directory(ir_version, build_number)
    ci_test.make_auto_result_file(csv_dir)
    print("—————————————— END ————————————-")