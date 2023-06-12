class NaiveEditor:
    def __init__(self):
        self.content = ""
        self.history = []
        
    def set_content(self, content):
        self.content = content
        self.history.append(content)
        
    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.content = self.history[-1]
        else:
            print("Can't undo")
        
        
editor = NaiveEditor()
editor.set_content("Hello World")
editor.set_content("Hello World 2")
editor.set_content("Hello World 3")
print(editor.content)
editor.undo()
print(editor.content)
editor.undo()
print(editor.content)


print("=====================================")


class Editor:
    def __init__(self):
        self.content = ""
        
    def set_content(self, content):
        self.content = content
        
    def create_state(self):
        return EditorState(self.content)
    
    def restore(self, state):
        self.content = state.get_content()


class EditorState:
    def __init__(self, content):
        self.content = content
        
    def get_content(self):
        return self.content
    

class History:
    def __init__(self):
        self.states = []
        
    def push(self, state):
        self.states.append(state)
        
    def pop(self):
        return self.states.pop()


# sorry but this is really fucking stupid

new_editor = Editor()
new_history = History()

new_editor.set_content("Hello World")
new_history.push(new_editor.create_state())

new_editor.set_content("Hello World 2")
new_history.push(new_editor.create_state())

new_editor.set_content("Hello World 3")
new_history.push(new_editor.create_state())
new_editor.restore(new_history.pop())

print(new_editor.content)



print("===================================")

class EditorV2:
    def __init__(self, state):
        self.state = state
        # self.history
        

class EditorStateV2:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        
    
    