import tkinter as tk
from tkinter import ttk

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


def playfair_encrypt(plaintext, key):
    plaintext = plaintext.replace(' ', '').upper()
    plaintext = plaintext.replace('J', 'I')
    key = key.replace(' ', '').upper()
    grid = generate_grid(key)


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
            
        
    
        print(pairs)

    encrypted = ''
    # rules
    for pair in pairs:
        a,b = pair[0], pair[1]
        r1, c1 = find_position(a, grid)
        r2, c2 = find_position(b, grid)

        # same row
            # if on same row replace with one on left

        if r1 == r2:
            print('same row')
            encrypted += grid[r1][(c1 + 1)%5]
            encrypted += grid[r2][(c2 + 1)%5]
        # same col
            # if on same col replace with one below
        if c1 == c2:
            print('same col')
            encrypted += grid[(r1 +1)%5][c1]
            encrypted += grid[(r2 +1)%5][c2]
            
        # rectangle
            # if rectange swap coordinated ? corner of rectangle
        else:
            print('rectangle')
            encrypted += grid[r1][c2]
            encrypted += grid[r2][c1]
        
    
    output_var.set(f'Encrypted: {encrypted}')

def find_position(letter, grid):
    for i in range(5):
        for j in range(5):
            if grid[i][j] == letter:
                return i, j

def display(grid):
    for widget in grid_frame.winfo_children():
        widget.destroy()

    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            cell = tk.Label(grid_frame, text=char, width=4, height=2,
                            borderwidth=1, relief='solid', font=('Helvetica', 12), bg='white')
            cell.grid(row=r, column=c, padx=2, pady=2)

def reset():
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    if not plaintext or not key:
        return
    
    playfair_encrypt(plaintext, key)


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

tk.Label(input_frame, text = 'rails', bg = '#A9B2C3').grid(row = 1, column = 0, padx=5, pady=5)
key_entry = ttk.Entry(input_frame, width =30)
key_entry.grid(row=1, column=1)

tk.Button(input_frame, text = 'start visulisation',command=reset, bg = '#7A89B8').grid(row=2, column= 0, columnspan = 2, pady=10)


grid_frame = tk.Frame(root,bg = '#A9B2C3')
grid_frame.pack(pady=10)

output_var = tk.StringVar()
tk.Label(root, bg = '#A9B2C3', textvariable=output_var).pack(pady=5)



root.mainloop()