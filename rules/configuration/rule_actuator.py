from core.redis  import rds
from core.triage import Triage
from core.parser import ScanParser, ConfParser

class Rule:
  def __init__(self):
    self.rule = 'CFG_9B88'
    self.rule_severity = 3
    self.rule_description = 'Actuator Misconfiguration'
    self.rule_confirm = 'Remote Server Actuator is misconfigured'
    self.rule_details = ''
    self.rule_mitigation = '''Server has a misconfigured Actuator, which is potentially leaking out sensitive data.
Restrict access to the endpoint to trusted sources only.'''
    self.rule_match_string = {
                              '/admin/dump':{
                                'app':'SPRING_BOOT_ACTUATOR_DUMP',
                                'match':['lineNumber','threadState','blockedTime','threadName'],
                                'title':'Spring Boot Actuator'
                              },
                               '/dump':{
                                'app':'SPRING_BOOT_ACTUATOR_DUMP',
                                'match':['lineNumber','threadState','blockedTime','threadName'],
                                'title':'Spring Boot Actuator'
                              },
                              '/admin/env.json':{
                                'app':'SPRING_BOOT_ACTUATOR_ENV',
                                'match':['os.arch','java.vm.vendor','java.runtime.name','java.library.path'],
                                'title':'Spring Boot Actuator'
                              },
                              '/actuator/env':{
                                'app':'SPRING_BOOT_ACTUATOR_ENV',
                                'match':['os.arch','java.vm.vendor','java.runtime.name','java.library.path'],
                                'title':'Spring Boot Actuator'
                              },
                              '/env.json':{
                                'app':'SPRING_BOOT_ACTUATOR_ENV',
                                'match':['os.arch','java.vm.vendor','java.runtime.name','java.library.path'],
                                'title':'Spring Boot Actuator'
                              },
                              '/env':{
                                'app':'SPRING_BOOT_ACTUATOR_ENV',
                                'match':['os.arch','java.vm.vendor','java.runtime.name','java.library.path'],
                                'title':'Spring Boot Actuator'
                              },
                              '/actuator/health':{
                                'app':'ACTUATOR_HEALTH',
                                'match':['"diskSpace":'],
                                'title':'Actuator Health'
                              },   
                              '/health':{
                                'app':'ACTUATOR_HEALTH',
                                'match':['"diskSpace":'],
                                'title':'Actuator Health'
                              },
                           }
    self.intensity = 3


  def check_rule(self, ip, port, values, conf):
    c = ConfParser(conf)
    t = Triage()
    p = ScanParser(port, values)
    
    domain = p.get_domain()
    module   = p.get_module()

    if 'http' not in module:
      return
    
    for uri, values in self.rule_match_string.items():
      app_name = values['app']
      app_title = values['title']

      resp = t.http_request(ip, port, uri=uri)
                    
      if resp is not None:
        for match in values['match']:
          if match in resp.text:
            self.rule_details = 'Exposed {} at {}'.format(app_title, uri)
            
            js_data = {
              'ip':ip,
              'port':port,
              'domain':domain,
              'rule_id':self.rule,
              'rule_sev':self.rule_severity,
              'rule_desc':self.rule_description,
              'rule_confirm':self.rule_confirm,
              'rule_details':self.rule_details,
              'rule_mitigation':self.rule_mitigation
            }
            
            rds.store_vuln(js_data)   
  
    return
