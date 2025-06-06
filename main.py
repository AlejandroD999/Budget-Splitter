import tkinter as tk
import ttkbootstrap as ttk
import pandas as pd
from tkinter import messagebox
#Constants
window_geometry = "500x350"
total_income = ['']

def clear_default_text(event):

    if income_entry.get() == "Enter weekly income here":
        income_entry.delete(0, ttk.END)


def get_income():
    global total_income

    try:
        amount = float(income_entry.get())
        total_income = amount


    except ValueError:
        messagebox.showerror("Value Error", "Input must be a number")
    
def create_results():
    #Make Borders -> color: white & thick

    income = total_income

    results_data = {
        "Growth": ['25%', income * .25],
        "Stability": ['15%', income * .15],
        "Needs": ['50%', income * .5],
        "Wants": ['10%', income * .10]
    }



    results_table = pd.DataFrame(results_data,index=['Percentage', 'Amount'])
    
    styled_results = results_table.style.set_table_styles([{
        'selector': 'th', 'props': [('border', '1px solid black')]
        }])
    
    styled_results

    return results_table
    


def outcome_branch():
    
    results = create_results()
    
    branch = ttk.Toplevel("Outcome")

    branch.geometry("400x400")

    total_income_label = ttk.Label(master=branch, text=f"Total Income: ${total_income}",
                                   font = ("Times New Roman", 16))
    total_income_label.pack()

    outcome_content = ttk.Label(master=branch, text= results,
                                font=("Times New Roman", 15))
    outcome_content.pack(pady = 10)

    ok_button = ttk.Button(master=branch, text="Ok", width=7, command=lambda: branch.destroy())
    ok_button.pack(anchor='se', padx=7, pady=10)

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

outcome_frame = tk.Frame(master=root)
outcome_frame.pack()



outcome_buttons_frame = ttk.Frame(master= root)
outcome_buttons_frame.pack(anchor="se", padx=5)


pdf_button = ttk.Button(master=outcome_buttons_frame, text="Save as PDF",
                        style='outline')
pdf_button.pack(side="left")

results_button = ttk.Button(master=outcome_buttons_frame, text="Results",
                            command=lambda: outcome_branch() if type(total_income) == float else messagebox.showerror("Result Error", "Income must be submitted"))

results_button.pack(side="left", padx = 10)



if __name__ == "__main__":

    root.mainloop()
