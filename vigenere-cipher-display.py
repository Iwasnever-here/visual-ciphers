import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# generate the vingenere table
def generate_table():
    return [[chr((i+j) % 26 + ord('A')) for j in range(26)] for i in range(26)]

# encrypt the input with the given key and remove any spaces
def vingenere_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    key_stream = (key *(len(plaintext)//len(key) + 1))[:len(plaintext)]
    table =generate_table()
    result = []
    

    for i, j in zip(plaintext, key_stream):
        row = ord(j) - ord('A')
        col = ord(i) - ord('A')
        cipher = table[row][col]
        result.append({'i': i, 'j': j, 'c': cipher, 'row':row, 'col': col})

    
    return result

def show_step(index):
    if index >= len(steps):
        return
    step = steps[index]
    i, j, c, row_idx, col_idx = step['i'], step['j'], step['c'], step['row'], step['col']  # ✅ correct keys!
    step_label.config(text = f"Step {index+1}: {i} + {j} = {c}")

    for i in range(26):
        for j in range(26):
            bg = 'white'
            if i == row_idx and j == col_idx:
                bg = '#4F69C6'
            elif i == row_idx:
                bg = '#C3CDE6'
            elif j == col_idx:
                bg = '#7A89B8'
            cell_labels[i][j].config(bg=bg)

def next_step():
    global current_step
    if current_step < len(steps):
        show_step(current_step)
        current_step += 1

def reset():
    global steps, current_step
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    if not plaintext or not key:
        return
    steps = vingenere_encrypt(plaintext, key)
    current_step = 0
    next_step()

##############################GUI#########################################

root = tk.Tk()
root.title('vigenere cipher step-by-step example')
root.geometry('800x800')
root.resizable(False, False)
root.config(bg = '#A9B2C3')

def open_info_window():
    explain_win = tk.Toplevel(root)
    explain_win.title('How it works')
    text = tk.Text(explain_win, wrap='word', width =60, height =30, bg = '#A9B2C3')
    text.pack(padx=10,pady=10)
    explanation = (
        'the vigenere cipher works by: \n'
        'taking in a sentence of letters \n'
        'and taking in a key \n'
        'the key is then repeated in a circular manner until it matches length of the sentence \n'
        'and each character in the sentence is encryped by the calculation: \n'
        'c = (p + k) mod 26 \n'
        'where p is the plaintext sentence and k is the key \n'
        '\n'
        'can be decryped with calculation: \n'
        'd = (c - k) mod 26 \n'
        'where c is encrypted character'
    )
    text.insert(tk.END, explanation)
    text.config(state = 'disabled')

def open_encryption_window():
    if not steps:
        return
    result = ''.join(step['c'] for step in steps)
    result_win = tk.Toplevel(root)
    result_win.title('Final encrypted message')
    result_win.config(bg = '#A9B2C3')
    result_win.geometry('200x150')

    tk.Label(result_win, text = 'encrypted text').pack(pady=10)
    tk.Label(result_win, text=result).pack(pady=10)

input_frame = tk.Frame(root, padx=10, pady=10, bg = '#A9B2C3')
input_frame.pack()

tk.Label(input_frame, text = 'text', bg = '#A9B2C3').grid(row = 0, column = 0, padx=5, pady=5)
plaintext_entry = ttk.Entry(input_frame, width =30)
plaintext_entry.grid(row=0, column=1)

tk.Label(input_frame, text = 'key', bg = '#A9B2C3').grid(row = 1, column = 0, padx=5, pady=5)
key_entry = ttk.Entry(input_frame, width =30)
key_entry.grid(row=1, column=1)

tk.Button(input_frame, text = 'start visulisation', command=reset, bg = '#7A89B8').grid(row=2, column= 0, columnspan = 2, pady=10)

step_label = tk.Label(root, text='step', bg = '#A9B2C3')
step_label.pack()

grid_frame = tk.Frame(root, bg = '#A9B2C3', pady=10)
grid_frame.pack()
cell_labels = []
alphabet = [chr(i + ord('A')) for i in range (26)]
tk.Label(grid_frame, text = '', bg = '#A9B2C3').grid(row=0, column=0)
for i, char in enumerate(alphabet):
    tk.Label(grid_frame, text = char, bg = '#A9B2C3').grid(row=0, column=i+1)
    tk.Label(grid_frame, text = char, bg = '#A9B2C3').grid(row=i+1, column=0)

for i in range(26):
    row_labels = []
    for j in range(26):
        value = tk.Label(grid_frame, text = chr((i+j)% 26 + ord('A')),width=2, borderwidth=0.5, relief='solid')
        value.grid(row=i+1, column = j+1)
        row_labels.append(value)
    cell_labels.append(row_labels)

control_frame = tk.Frame(root, padx=10, pady=10, bg = '#7A89B8')
control_frame.pack()

ttk.Button(control_frame, text="Next", command=next_step).pack(side=tk.LEFT, padx=5)
ttk.Button(control_frame, text="Explanation", command=open_info_window).pack(side=tk.LEFT, padx=5)
ttk.Button(control_frame, text="Show Result", command=open_encryption_window).pack(side=tk.LEFT, padx=5)


steps = []
current_step = 0

root.mainloop()