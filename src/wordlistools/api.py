from .base import tools


# Class so that we can use all plugins with an API
class API:
    def __init__(self):
        self.instances = {}

    def __getattr__(self, item):
        if item in self.instances:
            return self.instances[item]
        else:
            run_tool = tools[item]().run
            self.instances[item] = run_tool
            # print("returned tool", run_tool)
            # print("test run tool")
            # print(list(run_tool(["a", "b"])))
            # print("finish runtool")
            return run_tool


api = API()
