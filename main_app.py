import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText



from grey_comparison import GreyNumberBatchComparator, MinimaxRegretApproach
from grey_number_operation import GreyNumberOperationInput
from comsol import COMSOLInput  # NEW



class GreyNumberBatchInput(tk.Frame):
    def __init__(self, parent, result_widget):
        super().__init__(parent)
        self.result_widget = result_widget
        self.max_numbers = 6
        self.input_vars = []
        tk.Label(
            self,
            text="Enter Grey Numbers (Lower and Upper bounds):",
            bg="#2a2a2a",
            fg="white",
        ).grid(row=0, column=0, columnspan=3, pady=5)
        for i in range(self.max_numbers):
            tk.Label(self, text=f"X{i+1}:", bg="#2a2a2a", fg="white").grid(
                row=i + 1, column=0, padx=5, pady=2, sticky="w"
            )
            low_var = tk.StringVar()
            up_var = tk.StringVar()
            tk.Entry(self, textvariable=low_var, width=15).grid(
                row=i + 1, column=1, padx=5, pady=2
            )
            tk.Entry(self, textvariable=up_var, width=15).grid(
                row=i + 1, column=2, padx=5, pady=2
            )
            self.input_vars.append((low_var, up_var))
        self.calc_btn = tk.Button(
            self, text="Compare numbers", command=self.compare_all
        )
        self.calc_btn.grid(row=self.max_numbers + 1, column=0, columnspan=3, pady=10)

    def compare_all(self):
        valid_numbers = []
        for i, (low_var, up_var) in enumerate(self.input_vars):
            low = low_var.get().strip()
            up = up_var.get().strip()
            if low == "" and up == "":
                continue
            try:
                low_val = float(low)
                up_val = float(up)
                if low_val > up_val:
                    messagebox.showerror(
                        "Input Error",
                        f"Lower bound must be ≤ upper bound for X{i+1}",
                    )
                    return
                valid_numbers.append((low_val, up_val))
            except ValueError:
                messagebox.showerror(
                    "Input Error", f"Invalid number input for X{i+1}"
                )
                return
        if len(valid_numbers) < 2:
            messagebox.showwarning(
                "Warning", "Enter at least two grey numbers to compare."
            )
            return
        try:
            comparator = GreyNumberBatchComparator(valid_numbers)
            result_text = comparator.compare_all_pairs()
        except Exception as e:
            messagebox.showerror("Comparison Error", str(e))
            return
        self.result_widget.delete("1.0", tk.END)
        self.result_widget.insert(tk.END, result_text)


class RegretApproachInput(tk.Frame):
    def __init__(self, parent, result_widget):
        super().__init__(parent)
        self.result_widget = result_widget
        self.max_numbers = 6
        self.input_vars = []
        tk.Label(
            self,
            text="Enter Grey Numbers for Regret Approach:",
            bg="#2a2a2a",
            fg="white",
        ).grid(row=0, column=0, columnspan=4, pady=5)
        for i in range(self.max_numbers):
            tk.Label(
                self,
                text=f"X{i+1} Lower:",
                bg="#2a2a2a",
                fg="white",
            ).grid(row=i + 1, column=0, sticky="w", padx=5, pady=2)
            tk.Label(
                self,
                text=f"X{i+1} Upper:",
                bg="#2a2a2a",
                fg="white",
            ).grid(row=i + 1, column=2, sticky="w", padx=5, pady=2)
            low_var = tk.StringVar()
            up_var = tk.StringVar()
            tk.Entry(self, textvariable=low_var, width=15).grid(
                row=i + 1, column=1, padx=5, pady=2
            )
            tk.Entry(self, textvariable=up_var, width=15).grid(
                row=i + 1, column=3, padx=5, pady=2
            )
            self.input_vars.append((low_var, up_var))
        tk.Button(
            self, text="Compute Regret Ranking", command=self.compute_regret
        ).grid(row=self.max_numbers + 1, column=0, columnspan=4, pady=10)

    def compute_regret(self):
        valid_numbers = []
        for i, (low_var, up_var) in enumerate(self.input_vars):
            low = low_var.get().strip()
            up = up_var.get().strip()
            if low == "" and up == "":
                continue
            try:
                low_val = float(low)
                up_val = float(up)
                if low_val > up_val:
                    messagebox.showerror(
                        "Input Error",
                        f"Lower bound must be ≤ upper bound for X{i+1}",
                    )
                    return
                valid_numbers.append((low_val, up_val))
            except ValueError:
                messagebox.showerror(
                    "Input Error", f"Invalid number input for X{i+1}"
                )
                return
        if len(valid_numbers) < 2:
            messagebox.showwarning("Warning", "Enter at least two grey numbers")
            return
        mra = MinimaxRegretApproach(valid_numbers)
        sorted_indices, ranks = mra.rank_numbers()
        result_lines = ["Regret approach ranking (largest to smallest):"]
        for idx in sorted_indices:
            result_lines.append(
                f"X{idx+1} with rank {ranks[idx]} "
                f"(Interval: [{valid_numbers[idx][0]}, {valid_numbers[idx][1]}])"
            )
        self.result_widget.delete("1.0", tk.END)
        self.result_widget.insert(tk.END, "\n".join(result_lines))


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application of GST in POM")
        self.geometry("1200x750")
        self.configure(bg="#121212")

        self.left_frame = tk.Frame(self, bg="#1e1e1e", width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.tree = ttk.Treeview(self.left_frame)
        self.tree.pack(fill="both", expand=True)

        self.right_frame = tk.Frame(self, bg="#2a2a2a")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.input_frame = tk.Frame(self.right_frame, bg="#2a2a2a")
        self.input_frame.pack(fill="x", padx=10, pady=10)

        self.result_frame = tk.Frame(self.right_frame, bg="#a9c9ff")
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.result_text = ScrolledText(
        self.result_frame, bg="#a9c9ff", font=("Consolas", 10), undo=True, wrap="word"
        )
        self.result_text.pack(fill="both", expand=True)

# فعال کردن انتخاب متن و کپی با     Ctrl+C
        def copy_event(event=None):
            try:
                self.result_text.event_generate("<<Copy>>")
            except Exception:
                pass
           
        self.result_text.bind("<Control-c>", copy_event)
 

        self.current_analysis = None

        root = self.tree.insert("", "end", text="Grey System Theory", open=True)

        
        # --- Grey POM ---
        pom_root = self.tree.insert(root, "end", text="Grey POM", open=True)
        line_balancing = self.tree.insert(pom_root, "end", text="Grey line balancing", open=True)
        self.tree.insert(line_balancing, "end", text="COMSOL")


        self.analysis_registry = {
       


            "Grey possibility approach": GreyNumberBatchInput,
            "Regret approach": RegretApproachInput,
            "Grey number operation": GreyNumberOperationInput,
       	       "COMSOL": COMSOLInput,  # NEW

        }

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        text = self.tree.item(item, "text")
        self.result_text.delete("1.0", "end")
        for w in self.input_frame.winfo_children():
            w.destroy()
        cls = self.analysis_registry.get(text)
        if cls is None:
            self.current_analysis = None
            self.result_text.insert("end", "Select a valid leaf node.\n")
            return
        if hasattr(cls, "show_inputs"):
            self.current_analysis = cls(self.input_frame, self.result_text)
            self.current_analysis.show_inputs()
        else:
            self.current_analysis = None
            form = cls(self.input_frame, self.result_text)
            form.pack(fill="x", expand=True)

    def calculate(self):
        if self.current_analysis:
            self.current_analysis.calculate()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
