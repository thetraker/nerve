from core.redis  import rds
from core.triage import Triage
from core.parser import ScanParser, ConfParser
from core.logging import logger
class Rule:
  def __init__(self):
    self.rule = 'SVC_21BV'
    self.rule_severity = 1
    self.rule_description = 'Checks for Obfuscated SSH Ports'
    self.rule_mitigation = '''SSH Running on non-standard ports is easy for attackers to find.
While it doesn't do harm changing the standard port from (default) 22, ensure the server only accepts keys, and only allows SSH access from trusted IP sources.
'''
    self.rule_confirm = 'Remote Server Obfuscates SSH ports'
    self.rule_details = ''
    self.intensity = 0
    
  def check_rule(self, ip, port, values, conf):
    c = ConfParser(conf)
    t = Triage()
    p = ScanParser(port, values)
    
    module = p.get_module()
    domain = p.get_domain()
    product = p.get_product()
    
    if 'ssh' in module or 'ssh' in product.lower():
      if port != 22:
        self.rule_details = 'SSH is hidden behind port {}'.format(port)
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
