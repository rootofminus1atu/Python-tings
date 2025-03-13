from dataclasses import dataclass
from typing import List
import random
import os

@dataclass
class Message:
    content: str
    frequency: float = 1  # 1 = default, equally as likely as any other default msg

def generate_msg_sequence(messages: List[Message], length: int) -> List[str]:
    weights = [msg.frequency for msg in messages]
    return [msg.content for msg in random.choices(messages, weights=weights, k=length)]

def generate_bind_script(msg_sequence: List[str], key: str) -> str:
    if len(msg_sequence) == 0:
        raise Exception("nah i aint creating an empty script (add more than 0 messages)")

    s = ""
    for i, msg in enumerate(msg_sequence):
        start_idx = 1
        idx = start_idx + i
        next_idx = start_idx + i + 1 if i != len(msg_sequence) - 1 else start_idx
        
        s += f"alias chat{idx} \"say {msg}; alias chat_cycle chat{next_idx}\";\n"
    
    s += f"alias chat_cycle \"chat1\";\nbind \"{key}\" \"chat_cycle\"\n"

    return s

def save_to_tfcfg(bind_script: str, tfcfg_path: str):
    bind_file_name = "pseudorandom_bind.cfg"
    autoexec_file = "autoexec.cfg"

    bind_file = os.path.join(tfcfg_path, bind_file_name)
    autoexec_file = os.path.join(tfcfg_path, autoexec_file)
    exec_line = f"exec {bind_file_name}"

    if not os.path.exists(tfcfg_path):
        raise Exception(f"TF2 config dir not found: {tfcfg_path}")
    
    with open(bind_file, 'w') as f:
        f.write(bind_script)

    if not os.path.exists(autoexec_file):
        with open(autoexec_file, 'w') as f:
            f.write(exec_line)
    else:
        with open(autoexec_file, 'r') as f:
            content = f.read()
        
        if exec_line not in content:
            with open(autoexec_file, 'a') as f:
                f.write(f"\n{exec_line}")

    print(f"created bind script at {bind_file}")
    print(f"config updated at {autoexec_file}")

def read_messages_from_file(filename: str) -> List[Message]:
    messages = []

    with open(filename, 'r') as f:
        for line in f.readline():
            line = line.strip()
            if line:
                messages.append(Message(line))
        
    return messages

# can be changed
SEQUENCE_LEN = 100
TFCFG_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg"

def create_pseudorandom_bind(messages: List[Message], key: str): 
    msg_sq = generate_msg_sequence(messages, SEQUENCE_LEN)
    script = generate_bind_script(msg_sq, key)

    save_to_tfcfg(script, TFCFG_PATH)


if __name__ == "__main__":
    # feel free to change as much as your heart desires
    messages = [
        *read_messages_from_file("bot.txt"),
        Message("I'm not a bottom.", 0.01)  # 0.01 = very rare, no guarantee itd even happen
    ]
    # feel free to change this too
    key = 'h'

    create_pseudorandom_bind(messages, key)

    # NOTE: to refresh while in-game, you have to run the `exec autoexec` command in the tf2 console