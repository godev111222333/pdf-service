import yaml


class Config:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            cfg = yaml.safe_load(f)

        self.customer_contract = cfg['customer_contract']
        self.partner_contract = cfg['partner_contract']
        self.aws = cfg['aws']
