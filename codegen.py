class CodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.code = []

    def new_temp(self):
        temp = f't{self.temp_count}'
        self.temp_count += 1
        return temp

    def new_label(self):
        label = f'L{self.label_count}'
        self.label_count += 1
        return label

    def generate(self, node):
        if not node:
            return None
        if node.type == 'programa':
            for child in node.children:
                self.generate(child)
        elif node.type == 'cuerpo':
            for child in node.children:
                self.generate(child)
        elif node.type == 'declaraciones':
            for child in node.children:
                self.generate(child)
        elif node.type == 'declaracion':
            var = node.children[0].value
            self.code.append(f'declare {var} : {node.children[1].value}')
        elif node.type == 'instrucciones':
            for child in node.children:
                self.generate(child)
        elif node.type == 'asignacion':
            var = node.children[0].value
            expr_result = self.generate(node.children[1])
            self.code.append(f'{var} = {expr_result}')
        elif node.type == 'decision':
            cond_result = self.generate(node.children[0])
            label_true = self.new_label()
            label_false = self.new_label()
            label_end = self.new_label()
            self.code.append(f'if {cond_result} goto {label_true}')
            self.code.append(f'goto {label_false}')
            self.code.append(f'{label_true}:')
            self.generate(node.children[1])
            self.code.append(f'goto {label_end}')
            self.code.append(f'{label_false}:')
            self.generate(node.children[2])
            self.code.append(f'{label_end}:')
        elif node.type == 'ciclo':
            label_start = self.new_label()
            label_true = self.new_label()
            label_end = self.new_label()
            self.code.append(f'{label_start}:')
            cond_result = self.generate(node.children[0])
            self.code.append(f'if {cond_result} goto {label_true}')
            self.code.append(f'goto {label_end}')
            self.code.append(f'{label_true}:')
            self.generate(node.children[1])
            self.code.append(f'goto {label_start}')
            self.code.append(f'{label_end}:')
        elif node.type == 'para':
            self.generate(node.children[0])  # Inicialización
            label_start = self.new_label()
            label_true = self.new_label()
            label_end = self.new_label()
            self.code.append(f'{label_start}:')
            cond_result = self.generate(node.children[1])
            self.code.append(f'if {cond_result} goto {label_true}')
            self.code.append(f'goto {label_end}')
            self.code.append(f'{label_true}:')
            self.generate(node.children[3])
            self.generate(node.children[2])  # Incremento
            self.code.append(f'goto {label_start}')
            self.code.append(f'{label_end}:')
        elif node.type == 'do_mientras':
            label_start = self.new_label()
            label_true = self.new_label()
            label_end = self.new_label()
            self.code.append(f'{label_start}:')
            self.generate(node.children[0])
            cond_result = self.generate(node.children[1])
            self.code.append(f'if {cond_result} goto {label_start}')
            self.code.append(f'goto {label_end}')
            self.code.append(f'{label_end}:')
        elif node.type == 'tratamiento_error':
            label_catch = self.new_label()
            label_end = self.new_label()
            self.code.append(f'try:')
            self.generate(node.children[0])
            self.code.append(f'goto {label_end}')
            self.code.append(f'{label_catch}:')
            self.code.append(f'catch {node.children[1].value}:')
            self.generate(node.children[2])
            self.code.append(f'{label_end}:')
        elif node.type == 'seleccion_multiple':
            expr_result = self.generate(node.children[0])
            label_end = self.new_label()
            for caso in node.children[1].children:
                label_case = self.new_label()
                case_value = self.generate(caso.children[0])
                self.code.append(f'if {expr_result} == {case_value} goto {label_case}')
                self.generate(caso.children[1])
                self.code.append(f'goto {label_end}')
                self.code.append(f'{label_case}:')
            self.generate(node.children[2])
            self.code.append(f'{label_end}:')
        elif node.type == 'casos':
            for child in node.children:
                self.generate(child)
        elif node.type == 'caso':
            self.generate(node.children[1])
        elif node.type == 'defecto':
            self.generate(node.children[0])
        elif node.type == 'llamada_funcion':
            func_name = node.children[0].value
            args = [self.generate(arg) for arg in node.children[1].children]
            args_str = ', '.join(str(arg) for arg in args if arg is not None)
            temp = self.new_temp()
            self.code.append(f'{temp} = call {func_name}({args_str})')
            return temp
        elif node.type == 'lista_expresiones':
            return [self.generate(expr) for expr in node.children]
        elif node.type == 'logica':
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            temp = self.new_temp()
            self.code.append(f'{temp} = {left} {node.value} {right}')
            return temp
        elif node.type == 'relacional':
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            temp = self.new_temp()
            self.code.append(f'{temp} = {left} {node.value} {right}')
            return temp
        elif node.type == 'aritmetica':
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            temp = self.new_temp()
            self.code.append(f'{temp} = {left} {node.value} {right}')
            return temp
        elif node.type == 'termino':
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            temp = self.new_temp()
            self.code.append(f'{temp} = {left} {node.value} {right}')
            return temp
        elif node.type == 'bloque':
            for child in node.children:
                self.generate(child)
        elif node.type == 'valor':
            return str(node.value)
        elif node.type == 'identificador':
            return node.value
        return None

    def get_code(self):
        return '\n'.join(self.code)