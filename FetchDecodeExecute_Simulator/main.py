import customtkinter as ctk
import tkinter as tk
from ValidationLogic import Validate


class CPUInterface:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("CPU Simulator")
        self.clock = 0
        self.ram_entries = []
        self.next_button = None
        self.step_number = 0
        self.programme_counter = 0
        self.instruction_register = 0
        self.accumulator = 0
        self.vector = []

        # CPU Frame
        self.cpu_frame = ctk.CTkFrame(self.window)
        self.cpu_frame.pack(side=ctk.LEFT, padx=10, pady=10)

        # CPU Label
        self.cpu_label = ctk.CTkLabel(self.cpu_frame, text="CPU")
        self.cpu_label.pack(anchor=ctk.W, padx=10, pady=10)

        # CPU Clock
        self.clock_label = ctk.CTkLabel(self.cpu_frame, text="Clock: 0")
        self.clock_label.pack(anchor=ctk.W, padx=10, pady=10)

        # CPU Registers
        self.registers_frame = ctk.CTkFrame(self.cpu_frame)
        self.registers_frame.pack(anchor=ctk.W, padx=10)

        self.pc_label = ctk.CTkLabel(self.registers_frame, text="Program Counter:")
        self.pc_label.pack(anchor=ctk.W)
        self.pc_entry = ctk.CTkLabel(self.registers_frame, text="0")
        self.pc_entry.pack(anchor=ctk.W)

        self.ir_label = ctk.CTkLabel(self.registers_frame, text="Instruction Register:")
        self.ir_label.pack(anchor=ctk.W)
        self.ir_entry = ctk.CTkLabel(self.registers_frame, text="0")
        self.ir_entry.pack(anchor=ctk.W)

        self.acc_label = ctk.CTkLabel(self.registers_frame, text="Accumulator:")
        self.acc_label.pack(anchor=ctk.W)
        self.acc_entry = ctk.CTkLabel(self.registers_frame, text="0")
        self.acc_entry.pack(anchor=ctk.W)

        # Vertical Line
        self.line_canvas = ctk.CTkCanvas(self.window, width=2, height=300)
        self.line_canvas.create_line(1, 0, 1, 300, fill="black")
        self.line_canvas.pack(side=ctk.LEFT, padx=10)

        # RAM Frame
        self.ram_frame = ctk.CTkFrame(self.window)
        self.ram_frame.pack(side=ctk.LEFT, padx=10)

        # RAM Label
        self.ram_label = ctk.CTkLabel(self.ram_frame, text="RAM")
        self.ram_label.pack(anchor=ctk.W)

        # RAM Table
        self.ram_table_frame = ctk.CTkFrame(self.ram_frame)
        self.ram_table_frame.pack(anchor=ctk.W)

        self.address_label = ctk.CTkLabel(self.ram_table_frame, text="Address")
        self.address_label.grid(row=0, column=0, padx=5, pady=5)

        self.value_label = ctk.CTkLabel(self.ram_table_frame, text="Value")
        self.value_label.grid(row=0, column=1, padx=5, pady=5)

        self.ram_addresses = [f"{i}" for i in range(0, 8)]  # RAM addresses from 0 to 7
        self.ram_values = []
        self.value_entries = []

        for i, address in enumerate(self.ram_addresses):
            address_label = ctk.CTkLabel(self.ram_table_frame, text=address)
            address_label.grid(row=i + 1, column=0, padx=5, pady=2)

            value = ctk.StringVar()
            value_entry = ctk.CTkEntry(self.ram_table_frame, textvariable=value)
            value_entry.grid(row=i + 1, column=1, padx=5, pady=2)
            self.ram_values.append(value)
            self.value_entries.append(value_entry)

            # Bind Enter press to save the entered value
            value_entry.bind("<Return>", self.save_value)

        # Start Button
        self.start_button = ctk.CTkButton(self.window, text="Start", command=self.start_cycle)
        self.start_button.pack(padx=10, pady=10, side=ctk.TOP)

        # Reset Button
        self.reset_button = ctk.CTkButton(self.window, text="Reset", command=self.reset_interface)
        self.reset_button.pack(padx=10, pady=10, side=ctk.TOP)

        # Cycle Information Label
        self.cycle_label = ctk.CTkLabel(self.window, text="Cycle Information: ")
        self.cycle_label.pack(padx=10, pady=5)

        # Text Box Frame
        self.text_frame = ctk.CTkFrame(self.window)
        self.text_frame.pack(padx=10, pady=5)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text Box
        self.text_box = tk.Text(self.text_frame, width=70, height=10)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH)

        # Select font style
        font_style = ("Arial", 13)
        self.text_box.configure(font=font_style)

        # Put scrollbar in the text box
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_box.yview)

        # Text with "error" tag appears in red
        self.text_box.tag_configure("error", foreground="red")

    def save_value(self, event):
        # Get the entered value
        value_entry = event.widget
        value = value_entry.get()

        # Add the entered value to self.ram_entries
        self.ram_entries.append(value)

    def reset_interface(self):
        # Clear self.ram_entries
        self.ram_entries = []

        # Clear vector
        self.vector = []

        # Reset program counter
        self.programme_counter = 0
        self.pc_entry.configure(text="0")

        # Reset instruction register
        self.instruction_register = 0
        self.ir_entry.configure(text="0")

        # Reset accumulator
        self.accumulator = 0
        self.acc_entry.configure(text="0")

        # Reset the RAM entries
        for value_entry in self.value_entries:
            value_entry.delete(0, ctk.END)

        # Reset the clock
        self.clock = 0
        self.update_clock_label()

        # Remove the Next button if it exists
        if self.next_button:
            self.next_button.destroy()
            self.next_button = None

        # Enable the Start button
        self.start_button.configure(state=ctk.NORMAL)

        # Clear textbox
        self.text_box.delete(1.0, tk.END)

    def start_cycle(self):
        # Verify the entered values
        data_is_valid = True
        if not Validate.validate(self.ram_entries):
            self.text_box.insert(tk.END, "Error: Format not respected, please reset the interface!\n", "error")
            self.text_box.see(tk.END)
            data_is_valid = False

        # Disable the Start button
        self.start_button.configure(state=ctk.DISABLED)

        if data_is_valid:
            # Next Button
            self.next_button = ctk.CTkButton(self.window, text="Next", command=self.next_operation)
            self.next_button.pack(padx=10, pady=10, side=ctk.TOP)

        # Build self.vector for the for loop
        self.build_vector()

    def build_vector(self):
        # Make all elements in ram_entries strings for safety
        for i in range(len(self.ram_entries)):
            self.ram_entries[i] = str(self.ram_entries[i])

        # Create utility vector for the for loop
        for elem in self.ram_entries:
            instructions = elem.split()
            if not instructions[0].isdigit():
                # case example: if 3 > 4 3 -> (if,3,>,4,3) is appended to self.vector
                if instructions[0] == "if":
                    ins = instructions[0]
                    m1 = instructions[1]
                    c = instructions[2]
                    m2 = instructions[3]
                    jump = instructions[4]
                    self.vector.append((ins, m1, c, m2, jump))

                else:
                    string_value1 = instructions[0]
                    address1 = int(instructions[1])
                    int_values = None
                    if address1 <= len(self.ram_entries):
                        int_values = self.ram_entries[address1]
                    the_actual_address = instructions[1]
                    tuple_item = (string_value1, int_values, the_actual_address)
                    self.vector.append(tuple_item)

    def next_operation(self):
        # Check if program counter exceeds the length of ram_entries
        if self.programme_counter >= len(self.ram_entries) and self.step_number == 3:
            self.text_box.insert(tk.END, "End of program, reset to write a new sequence!\n")
            self.text_box.see(tk.END)

            # Disable the Next button
            self.next_button.configure(state=ctk.DISABLED)
            return

        # Increment clock by 1
        self.clock += 1
        self.update_clock_label()

        # Increment step number
        self.step_number += 1

        if self.step_number > 3:
            self.step_number = 1

        if self.step_number == 1:
            self.text_box.insert(tk.END, "~Fetch:" + "\n")
            self.text_box.see(tk.END)
            self.fetch()

        elif self.step_number == 2:
            self.text_box.insert(tk.END, "~Decode:" + "\n")
            self.text_box.see(tk.END)
            self.text_box.insert(tk.END, f"Decoding instruction '{self.instruction_register}' from IR..." + "\n")
            self.text_box.see(tk.END)
            self.decode()

        elif self.step_number == 3:
            self.text_box.insert(tk.END, "~Execute:" + "\n")
            self.text_box.see(tk.END)
            self.execute()

        # Cycle delimitation
        if self.step_number == 3:
            self.text_box.insert(tk.END, "----------------------------------------" + "\n")
            self.text_box.see(tk.END)

    def fetch(self):
        # Add value at program counter index from the ram entries to the instruction register
        self.instruction_register = self.ram_entries[self.programme_counter]

        # Update the instruction register label in the interface
        self.ir_entry.configure(text=str(self.instruction_register))

        # Update the program counter label in the interface
        self.pc_entry.configure(text=str(self.programme_counter))

        self.text_box.insert(tk.END, f"Fetched instruction from address {self.programme_counter}, putting it in the"
                                     f" instruction register" + "\n")
        self.text_box.see(tk.END)

        # Increment the program counter by 1
        self.programme_counter += 1

    def decode(self):
        # Split the instruction register value into a list
        instruction_list = str(self.instruction_register).split()

        return instruction_list

    def execute(self):
        instruction_list = self.decode()

        if instruction_list[0] == "load":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address "
                                             f"(no value at address {int(instruction_list[1])})!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address = int(instruction_list[1])
                value = self.ram_entries[address]
                self.accumulator = int(value)
                self.acc_entry.configure(text=str(self.accumulator))

                self.text_box.insert(tk.END,
                                     f"Loaded information from address {address} into"
                                     f" the accumulator." + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "add":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address "
                                             f"(no value at address {int(instruction_list[1])})!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address = int(instruction_list[1])
                value = self.ram_entries[address]
                self.accumulator += int(value)
                self.acc_entry.configure(text=str(self.accumulator))

                self.text_box.insert(tk.END, f"Added value at address {address} to the value that is already in"
                                             f" the accumulator." + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "sub":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address "
                                             f"(no value at address {int(instruction_list[1])})!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address = int(instruction_list[1])
                value = self.ram_entries[address]
                self.accumulator -= int(value)
                self.acc_entry.configure(text=str(self.accumulator))

                self.text_box.insert(tk.END, f"Subtracted value at address {address} from the value that is already"
                                             f" in"
                                             f" the accumulator." + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "mul":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address "
                                             f"(no value at address {int(instruction_list[1])})!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address = int(instruction_list[1])
                value = self.ram_entries[address]
                self.accumulator *= int(value)
                self.acc_entry.configure(text=str(self.accumulator))

                self.text_box.insert(tk.END, f"Multiplied value at address {address} with the value that is already"
                                             f" in"
                                             f" the accumulator." + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "div":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address "
                                             f"(no value at address {int(instruction_list[1])})!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address = int(instruction_list[1])
                value = self.ram_entries[address]
                self.accumulator //= int(value)
                self.acc_entry.configure(text=str(self.accumulator))

                self.text_box.insert(tk.END, f"Value in the accumulator div value at address {address}. " + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "mod":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address "
                                             f"(no value at address {int(instruction_list[1])})!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address = int(instruction_list[1])
                value = self.ram_entries[address]
                self.accumulator %= int(value)
                self.acc_entry.configure(text=str(self.accumulator))

                self.text_box.insert(tk.END, f"Value in the accumulator mod value at address {address}. " + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "store":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address {int(instruction_list[1])} "
                                             f"(it should be initialized)!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address = int(instruction_list[1])
                self.ram_entries[address] = self.accumulator
                self.value_entries[address].delete(0, ctk.END)
                self.value_entries[address].insert(0, str(self.accumulator))

                self.text_box.insert(tk.END, f"Stored accumulator value '{self.accumulator}' at address {address}."
                                             f" " + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "jump":
            if len(self.ram_entries) <= int(instruction_list[1]):
                self.text_box.insert(tk.END, f"Error: Invalid address {int(instruction_list[1])}"
                                             f" (it should be initialized)!\n",
                                     "error")
                self.text_box.see(tk.END)

            else:
                address_to_jump_to = int(instruction_list[1])
                self.programme_counter = int(instruction_list[1])
                self.pc_entry.configure(text=str(self.programme_counter))

                self.text_box.insert(tk.END, f"Jumped the programme counter to address {address_to_jump_to}." + "\n")
                self.text_box.see(tk.END)

        elif instruction_list[0] == "for":
            no_to_repeat = int(instruction_list[1])  # Number of addresses to repeat
            repetitions = int(instruction_list[2])  # Number of repetitions
            for i in range(0, repetitions):
                self.text_box.insert(tk.END, f"\nFor loop iteration {i + 1}:" + "\n")
                self.text_box.see(tk.END)

                k = len(self.vector) - no_to_repeat - 1
                while k < len(self.vector) - 1:
                    element = self.vector[k]
                    instruction = element[0]
                    instruction_value = element[1]

                    if instruction == "load":
                        value = int(instruction_value)
                        self.accumulator = int(value)
                        self.acc_entry.configure(text=str(self.accumulator))

                        self.text_box.insert(tk.END,
                                             f"Loaded information from address {element[2]}"
                                             f" into"
                                             f" the accumulator." + "\n")
                        self.text_box.see(tk.END)

                    elif instruction == "add":
                        value = int(instruction_value)
                        self.accumulator += int(value)
                        self.acc_entry.configure(text=str(self.accumulator))

                        self.text_box.insert(tk.END,
                                             f"Added value at address {element[2]}"
                                             f" to the value that is already in"
                                             f" the accumulator." + "\n")
                        self.text_box.see(tk.END)

                    elif instruction == "sub":
                        value = int(instruction_value)
                        self.accumulator -= int(value)
                        self.acc_entry.configure(text=str(self.accumulator))

                        self.text_box.insert(tk.END,
                                             f"Subtracted value at address {element[2]}"
                                             f" from the value that is already"
                                             f" in"
                                             f" the accumulator." + "\n")
                        self.text_box.see(tk.END)

                    elif instruction == "mul":
                        value = int(instruction_value)
                        self.accumulator *= int(value)
                        self.acc_entry.configure(text=str(self.accumulator))

                        self.text_box.insert(tk.END,
                                             f"Multiplied value at address {element[2]}"
                                             f" with the value that is already"
                                             f" in"
                                             f" the accumulator." + "\n")
                        self.text_box.see(tk.END)

                    elif instruction == "div":
                        value = int(instruction_value)
                        self.accumulator //= int(value)
                        self.acc_entry.configure(text=str(self.accumulator))

                        self.text_box.insert(tk.END,
                                             f"Value in the accumulator div value at address"
                                             f" {element[2]}. " + "\n")
                        self.text_box.see(tk.END)

                    elif instruction == "mod":
                        value = int(instruction_value)
                        self.accumulator %= int(value)
                        self.acc_entry.configure(text=str(self.accumulator))

                        self.text_box.insert(tk.END,
                                             f"Value in the accumulator mod value at address"
                                             f" {element[2]}. " + "\n")
                        self.text_box.see(tk.END)

                    elif instruction == "store":
                        # address = int(instruction_value)
                        self.ram_entries[int(element[2])] = self.accumulator
                        self.value_entries[int(element[2])].delete(0, ctk.END)
                        self.value_entries[int(element[2])].insert(0, str(self.accumulator))

                        self.text_box.insert(tk.END,
                                             f"Stored accumulator value '{self.accumulator}' "
                                             f"at address {element[2]}."
                                             f" " + "\n")
                        self.text_box.see(tk.END)

                    # if this is true we have: element = (if,3,>,4,3)
                    elif instruction == "if":
                        member1 = int(element[1])
                        comparator = element[2]
                        member2 = int(element[3])
                        no_of_instructions = int(element[4])

                        if comparator == ">":
                            if int(self.ram_entries[member1]) <= int(self.ram_entries[member2]):
                                # address_to_jump_to = self.programme_counter + no_of_instructions
                                # self.programme_counter += no_of_instructions
                                k += no_of_instructions

                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is false."
                                                     f" Jumped the programme counter to address"
                                                     f" {k + 1}." + "\n")
                                self.text_box.see(tk.END)
                            else:
                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is true."
                                                     f" Program continued without jump." + "\n")
                                self.text_box.see(tk.END)

                        elif comparator == ">=":
                            if self.ram_entries[member1] < self.ram_entries[member2]:
                                # address_to_jump_to = self.programme_counter + no_of_instructions
                                # self.programme_counter += no_of_instructions
                                k += no_of_instructions

                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is false."
                                                     f" Jumped the programme counter to address"
                                                     f" {k + 1}." + "\n")
                                self.text_box.see(tk.END)
                            else:
                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is true."
                                                     f" Program continued without jump." + "\n")
                                self.text_box.see(tk.END)

                        elif comparator == "<":
                            if self.ram_entries[member1] >= self.ram_entries[member2]:
                                # address_to_jump_to = self.programme_counter + no_of_instructions
                                # self.programme_counter += no_of_instructions
                                k += no_of_instructions

                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is false."
                                                     f" Jumped the programme counter to address"
                                                     f" {k + 1}." + "\n")
                                self.text_box.see(tk.END)
                            else:
                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is true."
                                                     f" Program continued without jump." + "\n")
                                self.text_box.see(tk.END)

                        elif comparator == "<=":
                            if self.ram_entries[member1] > self.ram_entries[member2]:
                                # address_to_jump_to = self.programme_counter + no_of_instructions
                                # self.programme_counter += no_of_instructions
                                k += no_of_instructions

                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is false."
                                                     f" Jumped the programme counter to address"
                                                     f" {k + 1}." + "\n")
                                self.text_box.see(tk.END)
                            else:
                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is true."
                                                     f" Program continued without jump." + "\n")
                                self.text_box.see(tk.END)

                        elif comparator == "==":
                            if self.ram_entries[member1] != self.ram_entries[member2]:
                                # address_to_jump_to = self.programme_counter + no_of_instructions
                                # self.programme_counter += no_of_instructions
                                k += no_of_instructions

                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is false."
                                                     f" Jumped the programme counter to address"
                                                     f" {k + 1}." + "\n")
                                self.text_box.see(tk.END)
                            else:
                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is true."
                                                     f" Program continued without jump." + "\n")
                                self.text_box.see(tk.END)

                        elif comparator == "!=":
                            if self.ram_entries[member1] == self.ram_entries[member2]:
                                # address_to_jump_to = self.programme_counter + no_of_instructions
                                # self.programme_counter += no_of_instructions
                                k += no_of_instructions

                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is false."
                                                     f" Jumped the programme counter to address"
                                                     f" {k + 1}." + "\n")
                                self.text_box.see(tk.END)
                            else:
                                self.text_box.insert(tk.END,
                                                     f"Statement '{member1} {comparator} {member2}' is true."
                                                     f" Program continued without jump." + "\n")
                                self.text_box.see(tk.END)

                    k += 1

        elif instruction_list[0] == "if":
            member1 = int(instruction_list[1])
            comparator = instruction_list[2]
            member2 = int(instruction_list[3])
            no_of_instructions = int(instruction_list[4])

            if comparator == ">":
                if self.ram_entries[member1] <= self.ram_entries[member2]:
                    address_to_jump_to = self.programme_counter + no_of_instructions
                    self.programme_counter += no_of_instructions
                    self.pc_entry.configure(text=str(self.programme_counter))

                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is false."
                                         f" Jumped the programme counter to address"
                                         f" {address_to_jump_to}." + "\n")
                    self.text_box.see(tk.END)
                else:
                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is true."
                                         f" Program continued without jump." + "\n")
                    self.text_box.see(tk.END)

            elif comparator == ">=":
                if self.ram_entries[member1] < self.ram_entries[member2]:
                    address_to_jump_to = self.programme_counter + no_of_instructions
                    self.programme_counter += no_of_instructions
                    self.pc_entry.configure(text=str(self.programme_counter))

                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is false."
                                         f" Jumped the programme counter to address"
                                         f" {address_to_jump_to}." + "\n")
                    self.text_box.see(tk.END)
                else:
                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is true."
                                         f" Program continued without jump." + "\n")
                    self.text_box.see(tk.END)

            elif comparator == "<":
                if self.ram_entries[member1] >= self.ram_entries[member2]:
                    address_to_jump_to = self.programme_counter + no_of_instructions
                    self.programme_counter += no_of_instructions
                    self.pc_entry.configure(text=str(self.programme_counter))

                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is false."
                                         f" Jumped the programme counter to address"
                                         f" {address_to_jump_to}." + "\n")
                    self.text_box.see(tk.END)
                else:
                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is true."
                                         f" Program continued without jump." + "\n")
                    self.text_box.see(tk.END)

            elif comparator == "<=":
                if self.ram_entries[member1] > self.ram_entries[member2]:
                    address_to_jump_to = self.programme_counter + no_of_instructions
                    self.programme_counter += no_of_instructions
                    self.pc_entry.configure(text=str(self.programme_counter))

                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is false."
                                         f" Jumped the programme counter to address"
                                         f" {address_to_jump_to}." + "\n")
                    self.text_box.see(tk.END)
                else:
                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is true."
                                         f" Program continued without jump." + "\n")
                    self.text_box.see(tk.END)

            elif comparator == "==":
                if self.ram_entries[member1] != self.ram_entries[member2]:
                    address_to_jump_to = self.programme_counter + no_of_instructions
                    self.programme_counter += no_of_instructions
                    self.pc_entry.configure(text=str(self.programme_counter))

                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is false."
                                         f" Jumped the programme counter to address"
                                         f" {address_to_jump_to}." + "\n")
                    self.text_box.see(tk.END)
                else:
                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is true."
                                         f" Program continued without jump." + "\n")
                    self.text_box.see(tk.END)

            elif comparator == "!=":
                if self.ram_entries[member1] == self.ram_entries[member2]:
                    address_to_jump_to = self.programme_counter + no_of_instructions
                    self.programme_counter += no_of_instructions
                    self.pc_entry.configure(text=str(self.programme_counter))

                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is false."
                                         f" Jumped the programme counter to address"
                                         f" {address_to_jump_to}." + "\n")
                    self.text_box.see(tk.END)
                else:
                    self.text_box.insert(tk.END,
                                         f"Statement '{member1} {comparator} {member2}' is true."
                                         f" Program continued without jump." + "\n")
                    self.text_box.see(tk.END)

    def update_clock_label(self):
        self.clock_label.configure(text=f"Clock: {self.clock}")

    def run(self):
        self.window.mainloop()


cpu_interface = CPUInterface()
cpu_interface.run()
