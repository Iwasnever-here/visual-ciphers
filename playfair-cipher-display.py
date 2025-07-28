import tkinter as tk
from tkinter import ttk

pairs = []
current_step = 0
key_grid = []
grid_cells = []
full_encrypted = ''


def generate_grid(key):
    grid = [[' ' for x in range(5)] for y in range(5)]
    # comine i/j
    alphabet = [chr(i + ord('A')) for i in range(26) if chr(i + ord('A')) != 'J']
    gridletters = []
    seen = set()
    
    for char in key:
         if char in alphabet and char not in seen:
              gridletters.append(char)
              seen.add(char)

    for char in alphabet:
         if char not in seen:
              gridletters.append(char)
              seen.add(char)

    grid = [[gridletters[i * 5 + j] for j in range(5)] for i in range(5)]
                     

    display(grid)
    return grid

def find_position(letter, grid):
    for i in range(5):
        for j in range(5):
            if grid[i][j] == letter:
                return i, j
            
    return None, None

def display(grid):
    global grid_cells
    for widget in grid_frame.winfo_children():
        widget.destroy()

    grid_cells = []  

    for r, row in enumerate(grid):
        row_cells = []
        for c, char in enumerate(row):
            cell = tk.Label(grid_frame, text=char, width=4, height=2,
                            borderwidth=1, relief='solid', font=('Helvetica', 12), bg='white')
            cell.grid(row=r, column=c, padx=2, pady=2)
            row_cells.append(cell)
        grid_cells.append(row_cells)



def reset():
    global pairs, current_step, key_grid, grid_cells, full_encrypted
    full_encrypted = ''

    plaintext = plaintext_entry.get()
    key = key_entry.get()
    if not plaintext or not key:
        return
    
    plaintext = plaintext.replace(' ', '').upper().replace('J', 'I')
    key = key.replace(' ', '').upper()
    key_grid = generate_grid(key)
    pairs = []

    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:
                pairs.append(a + 'X')
                
            else:
                pairs.append(a + b)
            
            i += 2  

        else:
            pairs.append(a + 'X') 
            i += 1
    current_step = 0


def next_step():
    global current_step, full_encrypted
    if current_step >= len(pairs):
        output_var.set(f'encrypted: {full_encrypted}')
        return

    pair = pairs[current_step]
    a, b = pair[0], pair[1]
    r1, c1 = find_position(a, key_grid)
    r2, c2 = find_position(b, key_grid)

    # Reset all cell backgrounds
    for row in grid_cells:
        for cell in row:
            cell.config(bg='white')

    # Highlight the current pair
    if r1 is not None and c1 is not None:
        grid_cells[r1][c1].config(bg='#4F69C6')
    if r2 is not None and c2 is not None:
        grid_cells[r2][c2].config(bg='#4F69C6')

    # Encrypt pair
    encrypted = ''
    if r1 == r2:
        encrypted += key_grid[r1][(c1 + 1) % 5]
        grid_cells[r1][(c1 + 1) % 5].config(bg='#7A89B8')
        encrypted += key_grid[r2][(c2 + 1) % 5]
        grid_cells[r2][(c2 + 1) % 5].config(bg='#7A89B8')
    elif c1 == c2:
        encrypted += key_grid[(r1 + 1) % 5][c1]
        grid_cells[(r1 + 1) % 5][c1].config(bg='#7A89B8')
        encrypted += key_grid[(r2 + 1) % 5][c2]
        grid_cells[(r2 + 1) % 5][c2].config(bg='#7A89B8')
    else:
        encrypted += key_grid[r1][c2]
        grid_cells[r1][c2].config(bg='#7A89B8')
        encrypted += key_grid[r2][c1]
        grid_cells[r2][c1].config(bg='#7A89B8')

    output_var.set(f'Step {current_step + 1}/{len(pairs)}: {pair} → {encrypted}')
    full_encrypted = full_encrypted + encrypted
    print(full_encrypted)
    current_step += 1 

    

################################################GUI#######################################
root = tk.Tk()
root.title('playfair cipher example')
root.geometry('500x500')
root.resizable(False, False)
root.config(bg = '#A9B2C3')

input_frame = tk.Frame(root, padx=10, pady=10, bg = '#A9B2C3')
input_frame.pack()

tk.Label(input_frame, text = 'text', bg = '#A9B2C3').grid(row = 0, column = 0, padx=5, pady=5)
plaintext_entry = ttk.Entry(input_frame, width =30)
plaintext_entry.grid(row=0, column=1)

tk.Label(input_frame, text = 'key', bg = '#A9B2C3').grid(row = 1, column = 0, padx=5, pady=5)
key_entry = ttk.Entry(input_frame, width =30)
key_entry.grid(row=1, column=1)

tk.Button(input_frame, text = 'start visulisation',command=reset, bg = '#7A89B8').grid(row=2, column= 0, columnspan = 2, pady=10)


grid_frame = tk.Frame(root,bg = '#A9B2C3')
grid_frame.pack(pady=10)

output_var = tk.StringVar()
tk.Label(root, bg = '#A9B2C3', textvariable=output_var).pack(pady=5)


control_frame = tk.Frame(root, padx=10, pady=10, bg = '#7A89B8')
control_frame.pack()

ttk.Button(control_frame, text="Next", command=next_step).pack(side=tk.LEFT, padx=5)

root.mainloop()