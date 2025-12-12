from .environment import Environment

DEV = Environment("dev", "govscot-dev")
UAT = Environment("uat", "govscot-uat")
PRD = Environment("prd", "govscot")
ENVS = {e.name: e for e in [DEV, UAT, PRD]}
