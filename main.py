import ttkbootstrap as ttk
from tkinter import messagebox
from tabulate import tabulate
import os

#Constants
window_geometry = "500x350"
total_income = ['']

def clear_default_text(event):

    if income_entry.get() == "Enter weekly income here":
        income_entry.delete(0, ttk.END)

def refresh_results(master):

    master.destroy()

    results_window()

def get_income():
    global total_income

    try:
        amount = float(income_entry.get())
        total_income = amount


    except ValueError:
        messagebox.showerror("Value Error", "Input must be a number")

def create_table():

    data = {
        "Invest": ['25%', f"${round(total_income * .25)}"],
        "Stability": ['15%',f"${round(total_income * .15)}"],
        "Needs": ['50%',f"${round(total_income * .5)}"],
        "Wants": ['10%',f"${round(total_income * .10)}"]
    }


    table = tabulate(data, headers="keys" ,tablefmt = "grid")
    
    return table

def create_file():
    
    current_directory = os.getcwd()

    file_path = os.path.join(current_directory, 'BudgetResults.txt')
    
    try:
        with open(file_path, 'w') as file:
            file.write("-------------------Results-------------------")
            for i in range(0, 4):
                file.write('\n')

            file.writelines(create_table())
            file.close()
    except FileExistsError:
        messagebox.showerror('File Exists', "A file with this name exists already")
    
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
                        values=(value[0],f"${round(value[1], 2)}")
                        )
        



    treeview.pack(anchor = 'center', pady=10)        

def results_window():
    
    
    branch = ttk.Toplevel("Results")
    branch.geometry("400x350+550+-10")


    total_income_label = ttk.Label(master=branch, text=f"Total Income: ${total_income}",
                                   font = ("Times New Roman", 16))
    total_income_label.pack()

    results = BudgetTable(branch)

    outcome_content = ttk.Label(master=branch, text= results,
                                font=("Times New Roman", 15))
    outcome_content.pack(pady = 0)

    buttons_frame = ttk.Frame(branch)
    buttons_frame.pack(anchor= 'se', padx=10, pady=5)

    refresh_button = ttk.Button(master=buttons_frame, text='Refresh',
                                 width = 10, command =lambda: refresh_results(branch))
    refresh_button.pack(side = 'left')

    ok_button = ttk.Button(master=buttons_frame, text="Ok", width=7, command=lambda: branch.destroy())
    ok_button.pack(side = 'left', padx = 5)

    branch.mainloop()


root = ttk.Window(themename="darkly")
root.geometry(window_geometry)
root.title("Budget Advisor")


input_frame = ttk.Frame(master=root)
input_frame.pack(anchor= 'nw', pady=75, padx=15)

income_entry = ttk.Entry(master=input_frame)
income_entry.insert(0, "Enter weekly income here")
income_entry.bind("<FocusIn>", clear_default_text)
income_entry.pack(side="left")


income_button = ttk.Button(master=input_frame, text="submit",
                           command=get_income)
income_button.pack(side="left", padx = 5)

outcome_frame = ttk.Frame(master=root)
outcome_frame.pack()

outcome_buttons_frame = ttk.Frame(master= root)
outcome_buttons_frame.pack(anchor="se", padx=5)


txt_button = ttk.Button(master=outcome_buttons_frame, text="Save as Txt",
                        style='outline', command= create_file)
txt_button.pack(side="left")

results_button = ttk.Button(master=outcome_buttons_frame, text="Results",
                            command=lambda: results_window() if type(total_income) == float else messagebox.showerror("Result Error", "Income must be submitted"))

results_button.pack(side="left", padx = 10)



if __name__ == "__main__":

    root.mainloop()
