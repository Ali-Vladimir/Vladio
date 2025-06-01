class CodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []
        self.label_count = 0

    def new_temp(self):
        temp = f't{self.temp_count}'
        self.temp_count += 1
        return temp

    def new_label(self):
        label = f'L{self.label_count}'
        self.label_count += 1
        return label

    def generate(self, node):
        if node.type == 'program':
            for child in node.children:
                self.generate(child)
        elif node.type == 'statements':
            for child in node.children:
                self.generate(child)
        elif node.type == 'assign':
            var = node.children[0].value
            expr_result = self.generate(node.children[1])
            self.code.append(f'{var} = {expr_result}')
        elif node.type == 'if':
            cond_result = self.generate(node.children[0])
            label_true = self.new_label()
            label_end = self.new_label()
            self.code.append(f'if {cond_result} goto {label_true}')
            self.code.append(f'goto {label_end}')
            self.code.append(f'{label_true}:')
            self.generate(node.children[1])
            self.code.append(f'{label_end}:')
        elif node.type == 'while':
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
        elif node.type == 'binop':
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            temp = self.new_temp()
            self.code.append(f'{temp} = {left} {node.value} {right}')
            return temp
        elif node.type == 'number':
            return str(node.value)
        elif node.type == 'id':
            return node.value
        return None

    def get_code(self):
        return '\n'.join(self.code)