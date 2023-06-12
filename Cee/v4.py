class Memory:
    def __init__(self):
        self.memory = {}

    def read(self, address):
        if address in self.memory:
            return self.memory[address]
        else:
            print(f"Error: Address {address} is not allocated.")

    def write(self, address, value):
        self.memory[address] = value
        
        
class CVariable:
    def __init__(self, initial_value=None):
        self.value = initial_value
        self.address = None

    def allocate_memory(self, memory):
        self.address = memory.allocate(self.value)

    def update_memory(self, memory):
        if self.address is not None:
            memory.write(self.address, self.value)
        else:
            print("Error: Variable is not allocated in memory.")

    def get(self):
        return self.value

    def set(self, new_value):
        self.value = new_value

    def deallocate_memory(self, memory):
        if self.address is not None:
            memory.deallocate(self.address)
            self.address = None


# Example usage
mem = Memory()

x = CVariable(10)  # Create a variable 'x' with an initial value of 10
x.allocate_memory(mem)  # Allocate memory for 'x'
x.update_memory(mem)  # Update the value of 'x' in memory
print(mem.read(x.address))  # Output: 10

x.set(20)  # Set the value of 'x' to 20
x.update_memory(mem)  # Update the value of 'x' in memory
print(mem.read(x.address))  # Output: 20

x.deallocate_memory(mem)  # Deallocate memory for 'x'