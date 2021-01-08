import tkinter as tk
import traceback
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext as sctxt
from subprocess import check_call, run

import os
from instructions_analysis import analyse

instructions_list = unique_instructions = cfp_count = None


def get_file_name():
    file_path = filedialog.askopenfilename(initialdir=".", title="Select file to measure",
                                           filetypes=(
                                               ("Text files", "*.txt"), ("C files", "*.c"), ("Object files", "*.o"),
                                               ('All files', '*.*')))

    source_file.insert(0, file_path)


def save_text():
    output_text_file = csv_file = open('./out/measurement_' + source_file.get().split('/')[-1].split('.')[0] + '.txt', 'w')

    total = sum(cfp_count)

    # Printing the counts
    underline = '~' * (len('Total CFP count = ') + len(str(total)))

    head = 'Total CFP count = {}\n' + str(
        underline) + '\nNumber of Entries = {}\nNumber of Reads = {}\nNumber of Writes = {}\nNumber of Exits = {}\n'

    output_text_file.write(head.format(total, *cfp_count, 0))

    output_text_file.write(str('=' * len(underline) + '\n'))

    # Printing the unique instructions
    output_text_file.write('CFP count per instruction type\n')
    output_text_file.write(str('~' * len('CFP count per instruction type')) + '\n')
    output_text_file.write(str(unique_instructions).replace('{', '').replace('}', '').replace(', ', '\n') + '\n')

    output_text_file.flush()
    output_text_file.close()
    results.insert(tk.END, 'Text file created.\n')
    return


def output_csv():
    csv_file = open('./out/instruction_summary_' + source_file.get().split('/')[-1].split('.')[0] + '.csv', 'w')

    csv_file.write('hex, name, ops, entries, reads, writes, exits\n')

    for inst in instructions_list:
        csv_file.write(','.join(inst) + '\n')

    csv_file.flush()
    csv_file.close()
    results.insert(tk.END, 'CSV file created.\n')


def start_measurement():
    if source_file.get() == '':
        raise Exception('No file chosen!')

    extension = source_file.get().split('.')[-1]

    global instructions_list
    global unique_instructions
    global cfp_count

    if extension == 'txt':
        instructions_list, unique_instructions, cfp_count = analyse(source_file.get())
        update_text_contents()
    elif extension == 'c':
        # run compiler then the objdump
        check_call('arm-linux-gnueabi-gcc -o test.o \"' + source_file.get() + '\"', shell=True)
        check_call('arm-linux-gnueabi-objdump -d test.o > test.txt', shell=True)
        instructions_list, unique_instructions, cfp_count = analyse(source_file.get().replace('.c', '.txt'))
        os.remove("./test.txt")
        os.remove("./test.o")
        update_text_contents()
    elif extension == 'o':
        # run objdump
        check_call('arm-linux-gnueabi-objdump -d \"' + source_file.get() + '\" > test.txt', shell=True)
        instructions_list, unique_instructions, cfp_count = analyse(source_file.get().replace('.o', '.txt'))
        os.remove("./test.txt")
        update_text_contents()
    else:
        # return error
        raise Exception('Wrong file extension')


def update_text_contents():
    total = sum(cfp_count)

    # Printing the counts
    underline = '~' * (len('Total CFP count = ') + len(str(total)))
    head = 'Total CFP count = {}\n' + str(
        underline) + '\nNumber of Entries = {}\nNumber of Reads = {}\nNumber of Writes = {}\nNumber of Exits = {}\n'

    # star before
    results.insert(tk.END, head.format(total, *cfp_count, 0))

    results.insert(tk.END, str('=' * len(underline) + '\n'))

    # Printing the unique instructions
    results.insert(tk.END, 'CFP count per instruction type\n')
    results.insert(tk.END, str('~' * len('CFP count per instruction type')) + '\n')
    results.insert(tk.END,
                   str({k: v for k, v in sorted(unique_instructions.items(), key=lambda item: item[1], reverse=True)}).replace('{',
                                                                                                                 '').replace(
                       '}', '').replace(', ', '\n') + '\n')

    results.insert(tk.END, str('=' * len(underline) + '\n'))

    # Printing the individual analysis (?)

    return


def show_error(self, *args):
    err = traceback.format_exception(*args)
    print(err)
    messagebox.showerror('Error', err[-1].split(':')[-1].strip())


### Basic Setup ###
window = tk.Tk()

window.title('ARM COSMIC Measurement Tool')

window.resizable(False, False)

tk.Tk.report_callback_exception = show_error

# Center window in screen
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth() / 3 - windowWidth / 2)
positionDown = int(window.winfo_screenheight() / 3 - windowHeight / 2)
window.geometry("+{}+{}".format(positionRight, positionDown))

### Source File stuff ###
tk.Label(window, text="Source File: ", padx=6).grid(row=0)
source_file = tk.Entry(window, width=70)
source_file.grid(row=0, column=1, columnspan=6)
tk.Button(window, text="Browse", command=get_file_name).grid(row=0, column=7, padx=6)

### Options and measure button ###
include_headers = tk.BooleanVar()
tk.Checkbutton(window, text='Include native C headers', variable=include_headers).grid(row=1, column=3)

tk.Button(window, text='Measure CFPs', command=start_measurement, bg='cyan').grid(row=2, column=3, pady=10)

### The output box ###
results = sctxt.ScrolledText(window, height=10, width=50, bg='lightgrey')
results.grid(row=3, column=0, pady=(0, 10), columnspan=8)

### Output buttons ###
tk.Button(window, text='Save Measurement', command=save_text).grid(row=14, column=5, columnspan=2, pady=10)

tk.Button(window, text='Save Analysis', command=output_csv).grid(row=14, column=1, columnspan=2)

window.mainloop()
