"""
ATM Fraud Detection - Python UI
This UI interfaces with the Prolog fraud detection engine and visualizes the results.
"""

import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re


class ATMFraudDetectionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Fraud Detection System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        
        # Track transactions
        self.transactions_history = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🏧 ATM Fraud Detection System", 
            font=('Arial', 24, 'bold'),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        title_label.pack(pady=10)
        
        # Create two columns
        left_frame = tk.Frame(main_frame, bg='#1e1e1e')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        right_frame = tk.Frame(main_frame, bg='#1e1e1e')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Left side: Input form
        self.create_input_form(left_frame)
        
        # Right side: Visualization
        self.create_visualization(right_frame)
        
    def create_input_form(self, parent):
        form_frame = tk.LabelFrame(
            parent, 
            text="Transaction Details", 
            font=('Arial', 14, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=15,
            pady=15
        )
        form_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Account Number
        tk.Label(form_frame, text="Account Number:", bg='#2d2d2d', fg='#ffffff').grid(row=0, column=0, sticky='w', pady=5)
        self.account_entry = ttk.Combobox(form_frame, values=['12345', '67890', '11111', '22222'], width=25)
        self.account_entry.set('12345')
        self.account_entry.grid(row=0, column=1, pady=5)
        
        # Amount
        tk.Label(form_frame, text="Transaction Amount ($):", bg='#2d2d2d', fg='#ffffff').grid(row=1, column=0, sticky='w', pady=5)
        self.amount_entry = tk.Entry(form_frame, width=27)
        self.amount_entry.insert(0, "150")
        self.amount_entry.grid(row=1, column=1, pady=5)
        
        # Location
        tk.Label(form_frame, text="Location:", bg='#2d2d2d', fg='#ffffff').grid(row=2, column=0, sticky='w', pady=5)
        self.location_entry = ttk.Combobox(
            form_frame, 
            values=['New York', 'Los Angeles', 'Chicago', 'Miami', 'Moscow', 'London', 'Tokyo'],
            width=25
        )
        self.location_entry.set('New York')
        self.location_entry.grid(row=2, column=1, pady=5)
        
        # Time (Hour)
        tk.Label(form_frame, text="Time (Hour 0-23):", bg='#2d2d2d', fg='#ffffff').grid(row=3, column=0, sticky='w', pady=5)
        self.time_entry = tk.Spinbox(form_frame, from_=0, to=23, width=25)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "14")
        self.time_entry.grid(row=3, column=1, pady=5)
        
        # Transaction Count Today
        tk.Label(form_frame, text="Transactions Today:", bg='#2d2d2d', fg='#ffffff').grid(row=4, column=0, sticky='w', pady=5)
        self.count_entry = tk.Spinbox(form_frame, from_=0, to=20, width=25)
        self.count_entry.delete(0, tk.END)
        self.count_entry.insert(0, "2")
        self.count_entry.grid(row=4, column=1, pady=5)
        
        # Days Since Last Transaction
        tk.Label(form_frame, text="Days Since Last Transaction:", bg='#2d2d2d', fg='#ffffff').grid(row=5, column=0, sticky='w', pady=5)
        self.days_entry = tk.Spinbox(form_frame, from_=0, to=365, width=25)
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, "1")
        self.days_entry.grid(row=5, column=1, pady=5)
        
        # Analysis Button
        self.analyze_btn = tk.Button(
            form_frame,
            text="🔍 Analyze Transaction",
            font=('Arial', 12, 'bold'),
            bg='#0066cc',
            fg='white',
            command=self.analyze_transaction,
            cursor='hand2',
            padx=20,
            pady=10
        )
        self.analyze_btn.grid(row=6, column=0, columnspan=2, pady=15)
        
        # Test Scenarios Frame
        test_frame = tk.LabelFrame(
            parent,
            text="Quick Test Scenarios",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=15,
            pady=10
        )
        test_frame.pack(fill=tk.X, pady=5)
        
        scenarios = [
            ("✅ Normal", self.load_normal),
            ("⚠️ High Amount", self.load_suspicious_amount),
            ("🌍 Foreign Location", self.load_foreign),
            ("⚡ High Velocity", self.load_velocity),
        ]
        
        for i, (text, command) in enumerate(scenarios):
            btn = tk.Button(
                test_frame,
                text=text,
                command=command,
                bg='#444444',
                fg='white',
                width=13
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
        
        # Result Display
        result_frame = tk.LabelFrame(
            parent,
            text="Analysis Result",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(
            result_frame,
            height=10,
            width=50,
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
    def create_visualization(self, parent):
        viz_frame = tk.LabelFrame(
            parent,
            text="Fraud Risk Visualization",
            font=('Arial', 14, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(6, 8), facecolor='#2d2d2d')
        
        # Risk Score Gauge
        self.ax1 = self.fig.add_subplot(211)
        self.ax1.set_facecolor('#2d2d2d')
        
        # Transaction History
        self.ax2 = self.fig.add_subplot(212)
        self.ax2.set_facecolor('#2d2d2d')
        
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize with default visualization
        self.update_visualization(0, "APPROVED")
        
    def update_visualization(self, risk_score, decision):
        self.ax1.clear()
        self.ax2.clear()
        
        # Risk Score Gauge
        colors = ['#00ff00', '#ffff00', '#ff6600', '#ff0000']
        if risk_score < 20:
            color = colors[0]
        elif risk_score < 40:
            color = colors[1]
        elif risk_score < 70:
            color = colors[2]
        else:
            color = colors[3]
        
        self.ax1.barh(['Risk Score'], [risk_score], color=color, height=0.5)
        self.ax1.set_xlim(0, 100)
        self.ax1.set_xlabel('Risk Score', color='white')
        self.ax1.set_title(f'Fraud Risk: {risk_score}/100\nDecision: {decision}', 
                          color='white', fontsize=14, fontweight='bold')
        self.ax1.tick_params(colors='white')
        self.ax1.spines['bottom'].set_color('white')
        self.ax1.spines['left'].set_color('white')
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        
        # Add reference lines
        self.ax1.axvline(x=40, color='yellow', linestyle='--', linewidth=1, alpha=0.5)
        self.ax1.text(40, 0.6, 'Threshold', color='yellow', fontsize=8)
        
        # Transaction History
        if self.transactions_history:
            approved = sum(1 for t in self.transactions_history if t['decision'] == 'APPROVED')
            declined = len(self.transactions_history) - approved
            
            labels = ['Approved', 'Declined']
            sizes = [approved, declined]
            colors_pie = ['#00ff00', '#ff0000']
            
            wedges, texts, autotexts = self.ax2.pie(
                sizes, 
                labels=labels, 
                colors=colors_pie,
                autopct='%1.0f%%',
                startangle=90
            )
            
            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                
            self.ax2.set_title(f'Transaction History (Total: {len(self.transactions_history)})', 
                             color='white', fontweight='bold')
        else:
            self.ax2.text(0.5, 0.5, 'No transactions yet', 
                         ha='center', va='center', 
                         transform=self.ax2.transAxes,
                         color='white', fontsize=12)
            self.ax2.set_title('Transaction History', color='white', fontweight='bold')
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def analyze_transaction(self):
        try:
            account = self.account_entry.get()
            amount = self.amount_entry.get()
            location = self.location_entry.get()
            hour = self.time_entry.get()
            count = self.count_entry.get()
            days = self.days_entry.get()
            
            # Validate inputs
            if not all([account, amount, location, hour, count, days]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            # Create Prolog query
            query = f"process_transaction({account}, {amount}, '{location}', {hour}, {count}, {days})."
            
            # Call Prolog
            result = self.call_prolog(query)
            
            # Display result
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
            # Extract risk score and decision
            risk_score = self.extract_risk_score(result)
            decision = self.extract_decision(result)
            
            # Update visualization
            self.update_visualization(risk_score, decision)
            
            # Add to history
            self.transactions_history.append({
                'account': account,
                'amount': amount,
                'risk_score': risk_score,
                'decision': decision
            })
            
            # Update visualization again to show history
            self.update_visualization(risk_score, decision)
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            
    def call_prolog(self, query):
        """Execute Prolog query and return result"""
        try:
            # Check if SWI-Prolog is installed
            prolog_file = os.path.join(os.path.dirname(__file__), 'goal_based_atm.pl')
            
            # Create a temporary file for the query
            query_command = f"swipl -s \"{prolog_file}\" -g \"{query}\" -g halt"
            
            # Execute Prolog
            result = subprocess.run(
                query_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            output = result.stdout + result.stderr
            
            if not output.strip():
                return "No output from Prolog. Make sure SWI-Prolog is installed."
            
            return output
            
        except subprocess.TimeoutExpired:
            return "Error: Prolog query timed out"
        except FileNotFoundError:
            return "Error: SWI-Prolog not found. Please install SWI-Prolog and add it to PATH."
        except Exception as e:
            return f"Error executing Prolog: {str(e)}"
    
    def extract_risk_score(self, result):
        """Extract risk score from Prolog output"""
        match = re.search(r'RISK SCORE CALCULATED:\s*(\d+)', result)
        if match:
            return int(match.group(1))
        return 0
    
    def extract_decision(self, result):
        """Extract decision from Prolog output"""
        if 'TRANSACTION APPROVED' in result:
            return 'APPROVED'
        elif 'TRANSACTION DECLINED' in result:
            return 'DECLINED'
        return 'UNKNOWN'
    
    # Quick test scenario loaders
    def load_normal(self):
        self.account_entry.set('12345')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, '150')
        self.location_entry.set('New York')
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, '14')
        self.count_entry.delete(0, tk.END)
        self.count_entry.insert(0, '2')
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, '1')
        
    def load_suspicious_amount(self):
        self.account_entry.set('12345')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, '2000')
        self.location_entry.set('New York')
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, '14')
        self.count_entry.delete(0, tk.END)
        self.count_entry.insert(0, '2')
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, '1')
        
    def load_foreign(self):
        self.account_entry.set('67890')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, '500')
        self.location_entry.set('Moscow')
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, '2')
        self.count_entry.delete(0, tk.END)
        self.count_entry.insert(0, '1')
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, '5')
        
    def load_velocity(self):
        self.account_entry.set('11111')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, '400')
        self.location_entry.set('Chicago')
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, '15')
        self.count_entry.delete(0, tk.END)
        self.count_entry.insert(0, '6')
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, '2')


def main():
    root = tk.Tk()
    app = ATMFraudDetectionUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
