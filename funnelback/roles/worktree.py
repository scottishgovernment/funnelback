import json
import os
from .role import Role


class Worktree:
    def design_files(self, env):
        common = self.__list_dir(self.__source_dir())
        environment = self.__list_dir(self.__source_dir(env))
        common.update(environment)
        return common

    def __list_dir(self, dir):
        if not os.path.exists(dir):
            return {}
        files = sorted(os.listdir(dir))
        return {f: os.path.join(dir, f) for f in files}

    def has_design_file(self, env, id):
        filename = id.split("~")[1] + ".json"
        common_dir = self.__source_dir()
        env_dir = self.__source_dir(env)
        for d in [common_dir, env_dir]:
            path = os.path.join(d, filename)
            if os.path.exists(path):
                return True
        return False

    def __source_dir(self, env=None):
        if env is None:
            dir = "common"
        else:
            dir = env.name
        return os.path.join(dir, "roles")

    def state_files(self, env):
        dir = self.__state_dir(env)
        return os.listdir(dir)

    def has_state_file(self, env, filename):
        path = self.__state_file(env, filename)
        return os.path.exists(path)

    def read_state(self, env, filename):
        path = self.__state_file(env, filename)
        with open(path, "r") as f:
            return Role(json.load(f))

    def write_state(self, env, role):
        filename = role.id.split("~")[1] + ".json"
        path = self.__state_file(env, filename)
        dir = self.__state_dir(env)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
        with open(path, "w") as f:
            json.dump(role.json, f, indent=2)
            f.write("\n")

    def __state_dir(self, env):
        return f".state/{env.name}/roles"

    def __state_file(self, env, filename):
        dir = self.__state_dir(env)
        return os.path.join(dir, filename)
