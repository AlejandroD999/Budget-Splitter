import ttkbootstrap as ttk
from tkinter import messagebox
from tabulate import tabulate
import time
import os

#Constants
window_geometry = f"450x150+200+100"
current_directory = os.getcwd()


def clear_default_text(event):
    event.widget.delete(0, ttk.END)


def refresh_results(master):

    master.destroy()

    results_window()

def submit_income():
    global total_income

    try:
        amount = round(float(income_entry.get()), 2)
        total_income = amount

        submitted_label = ttk.Label(master= income_frame, text="Submitted",
                                    font = ("Times New Roman", 16, 'italic'))
        submitted_label.pack(side = 'right', padx= 35)


    except ValueError:
        messagebox.showerror("Value Error", "Enter a valid currency. ")

def submit_filename():
    global filename

    filename = FileName_entry.get()

        
def create_table():

    data = {
        "Invest": ['25%', f"${round(total_income * .25, 2)}"],
        "Stability": ['15%',f"${round(total_income * .15, 2)}"],
        "Needs": ['50%',f"${round(total_income * .5, 2)}"],
        "Wants": ['10%',f"${round(total_income * .10, 2)}"]
    }


    table = tabulate(data, headers="keys" ,tablefmt = "grid")
    
    return table

def save_file(branch):

    try:
        file_path = os.path.join(current_directory,"data", f"{filename}.txt")
    

        with open(file_path, 'w') as file:
            file.write("-------------------Results-------------------")
            for i in range(0, 4):
                file.write('\n')
            
            file.write(f"Total Income:{total_income}\n\n")

            file.writelines(create_table())
            file.close()

        
        saved_frame = ttk.Frame(master = branch, borderwidth= 5, relief='solid')
        saved_frame.pack(anchor = 'sw', padx = 15, pady= 10)

        
        saved_label = ttk.Label(master= saved_frame, text=f"Successfully saved at:",
                                    font = ("Times New Roman", 14, 'italic'))
        saved_label.pack(padx=0)

        saved_text  =ttk.Entry(master= saved_frame)
        saved_text.insert(0, file_path)        
        saved_text.pack(padx = 15, pady= 5)




    except NameError:
        messagebox.showinfo("File name", "File name must be entered")


def save_results():
    global FileName_entry


    save_branch = ttk.Toplevel("Save as txt")
    save_branch.geometry("450x250+200+290")
    

    FileName_frame = ttk.Frame(master=save_branch)
    FileName_frame.pack(anchor= 'nw', pady=25, padx=15)

    FileName_entry = ttk.Entry(master = FileName_frame)
    FileName_entry.insert(0, "Enter File Name")
    FileName_entry.bind("<FocusIn>", clear_default_text)
    FileName_entry.pack(side="left")

    FileName_button = ttk.Button(master=FileName_frame, text="Submit",
                                 width= 6, command= submit_filename)
    FileName_button.pack(side = 'left', padx = 5)

    FileLocation_frame = ttk.Frame(master= save_branch)
    FileLocation_frame.pack(anchor='w')

    bottom_frame = ttk.Frame(master= save_branch)
    bottom_frame.pack(anchor= 'center', padx = 0, pady = 5)

    cancel_button = ttk.Button(master=bottom_frame, text= "Cancel", width=10, style='outline',
                               command = lambda: save_branch.destroy())
    cancel_button.pack(side='left')

    save_button = ttk.Button(master = bottom_frame,text = 'Save',
                                width = 7, command=lambda: save_file(FileLocation_frame))
    save_button.pack(side = 'left', padx = 6)
    

    save_branch.mainloop()

def BudgetTable(master):
    global results_data
    


    results_data = {
        "Invest": ['25%', total_income * .25],
        "Stability": ['15%', total_income * .15],
        "Needs": ['50%', total_income * .5],
        "Wants": ['10%', total_income * .10]
    }


    treeview = ttk.Treeview(master, columns=("Percentage", "Amount"), style="Treeview")
    


    treeview.column("#0", width=80, minwidth=25, stretch = False)
    treeview.column('Percentage', width=100, minwidth=50, stretch=False)
    treeview.column('Amount', width=100, minwidth=50, stretch=False)
    
    treeview.heading("#0", text="Category", anchor='w')
    treeview.heading("Percentage", text="Percentage", anchor="w")
    treeview.heading("Amount", text="Amount", anchor= 'w')
    

    for key, value in results_data.items():       
        
        treeview.insert("",
                        "2",
                        text= key,
                        values=(value[0],f"${value[1]}")
                        )
        



    treeview.pack(anchor = 'center', pady=10)        

def results_window():
    
    
    results_branch = ttk.Toplevel("Results")
    results_branch.geometry("450x350+200+290")


    total_income_label = ttk.Label(master=results_branch, text=f"Total Income: ${total_income}",
                                   font = ("Times New Roman", 16))
    total_income_label.pack()

    results = BudgetTable(results_branch)

    outcome_content = ttk.Label(master=results_branch, text= results,
                                font=("Times New Roman", 15))
    outcome_content.pack(pady = 0)

    buttons_frame = ttk.Frame(results_branch)
    buttons_frame.pack(anchor= 'se', padx=10, pady=5)

    refresh_button = ttk.Button(master=buttons_frame, text='Refresh',
                                 width = 10, command =lambda: refresh_results(results_branch))
    refresh_button.pack(side = 'left')

    ok_button = ttk.Button(master=buttons_frame, text="Ok", width=7, command=lambda: results_branch.destroy())
    ok_button.pack(side = 'left', padx = 5)

    results_branch.mainloop()


root = ttk.Window(themename="darkly")
root.geometry(window_geometry)
root.title("Budget Splitter")


income_frame = ttk.Frame(master=root)
income_frame.pack(anchor= 'nw', pady=25, padx=15)

income_entry = ttk.Entry(master=income_frame)
income_entry.insert(0, "Enter weekly income here")
income_entry.bind("<FocusIn>", clear_default_text)
income_entry.pack(side="left")


income_button = ttk.Button(master=income_frame, text="submit",
                           command=submit_income)
income_button.pack(side="left", padx = 5)



outcome_frame = ttk.Frame(master=root)
outcome_frame.pack()

outcome_buttons_frame = ttk.Frame(master= root)
outcome_buttons_frame.pack(anchor="se", padx=5)


SaveAs_button = ttk.Button(master=outcome_buttons_frame, text="Save as Txt",
                        style='outline', command=lambda: save_results() if type(total_income) == float else messagebox.showerror("Result Error", "Income must be submitted"))
SaveAs_button.pack(side="left")

results_button = ttk.Button(master=outcome_buttons_frame, text="Results",
                            command=lambda: results_window() if type(total_income) == float else messagebox.showerror("Result Error", "Income must be submitted"))

results_button.pack(side="left", padx = 10)



if __name__ == "__main__":

    root.mainloop()
