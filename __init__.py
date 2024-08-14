import json
from notebook.utils import to_api_path
from notebook.base.handlers import IPythonHandler
from .analyzer import CodeAnalyzer

class CodeDependencyHandler(IPythonHandler):
    def post(self):
        data = self.get_json_body()
        code = data['code']
        analyzer = CodeAnalyzer()
        defined_vars, used_vars = analyzer.analyze_code(code)
        self.finish(json.dumps({'defined_vars': list(defined_vars), 'used_vars': list(used_vars)}))

def load_jupyter_server_extension(nbapp):
    nbapp.log.info("Loaded code dependency analyzer extension")
    nbapp.web_app.add_handlers('.*', [
        (to_api_path('/code_dependencies', nbapp.settings), CodeDependencyHandler),
    ])
    nbapp.web_app.settings['code_dependencies'] = {}

def analyze_and_update_dependencies(cell_index, code, dependencies):
    analyzer = CodeAnalyzer()
    defined_vars, used_vars = analyzer.analyze_code(code)
    dependencies[cell_index] = {
        'defined_vars': defined_vars,
        'used_vars': used_vars
    }
    return dependencies
