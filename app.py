from flask import Flask, request, jsonify, send_from_directory
from lexer.lexer import lexer
from parser.parser import parser
from semantic.analyzer import SemanticAnalyzer
from ir.ir_generator import IRGenerator
from codegen.python_generator import PythonCodeGenerator
from codegen.cpp_generator import CppCodeGenerator
from codegen.java_generator import JavaCodeGenerator
from codegen.js_generator import JavaScriptCodeGenerator
import os

app = Flask(__name__, static_folder='.')

GENERATORS = {
    'python': PythonCodeGenerator,
    'cpp':    CppCodeGenerator,
    'java':   JavaCodeGenerator,
    'js':     JavaScriptCodeGenerator,
}

@app.route('/')
def index():
    return send_from_directory('.', 'transpiler_platform.html')

@app.route('/transpile', methods=['POST'])
def transpile():
    data = request.json
    code = data.get('code', '')
    target = data.get('target', 'python')
    try:
        ast = parser.parse(code)
        SemanticAnalyzer().analyze(ast)
        ir = IRGenerator().generate(ast)
        result = GENERATORS[target]().generate(ir)
        return jsonify({'success': True, 'output': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)