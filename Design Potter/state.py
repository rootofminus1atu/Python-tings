from abc import ABC, abstractmethod

# why tf is this even name state?
# confusing name but cool pattern

class Tool(ABC):
    @abstractmethod
    def mouse_up(self):
        pass
    
    @abstractmethod
    def mouse_down(self):
        pass
    
    
class SelectionTool(Tool):
    def mouse_down(self):
        print("Selection icon")
        
    def mouse_up(self):
        print("Draw a dashed rectangle")
    
    
class BrushTool(Tool):
    def mouse_down(self):
        print("Brush icon")
        
    def mouse_up(self):
        print("Draw a line")

    
class Canvas:
    def __init__(self):
        self.current_tool: Tool = SelectionTool()
        
    def mouse_up(self):
        self.current_tool.mouse_up()
    
    def mouse_down(self):
        self.current_tool.mouse_down()


canvas = Canvas()
canvas.current_tool = BrushTool()
canvas.mouse_down()
canvas.mouse_up()
canvas.current_tool = SelectionTool()
canvas.mouse_down()
canvas.mouse_up()