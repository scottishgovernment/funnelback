from .environment import Environment

DEV = Environment("dev", "scotgov", "dev")
UAT = Environment("uat", "scotgov", "uat")
PRD = Environment("prd", "scotgov")
ENVS = {e.name: e for e in [DEV, UAT, PRD]}
