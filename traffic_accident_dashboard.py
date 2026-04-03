import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import random
import math

class TrafficAccidentDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-State Traffic Accident Probability Dashboard")
        self.root.geometry("1600x950")
        self.root.configure(bg='#1e293b')
        
        self.accidents_df = self.generate_sample_data()
        
        self.accident_types = ['Minor Collision', 'Major Collision', 'Hit and Run', 
                              'Pedestrian Involved', 'Vehicle Rollover']
        self.states = ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Gujarat', 'Delhi', 
                      'Uttar Pradesh', 'Rajasthan', 'West Bengal']
        self.locations = {
            'Karnataka': ['MG Road Junction', 'Outer Ring Road', 'Mysore Road', 'Bannerghatta Road'],
            'Maharashtra': ['Mumbai-Pune Highway', 'Western Express', 'Eastern Freeway', 'LBS Marg'],
            'Tamil Nadu': ['Anna Salai', 'OMR Junction', 'GST Road', 'Mount Road'],
            'Gujarat': ['SG Highway', 'CG Road', 'Ashram Road', 'Sarkhej-Gandhinagar Highway'],
            'Delhi': ['Ring Road', 'NH-8 Junction', 'Outer Ring Road', 'Delhi-Gurgaon Border'],
            'Uttar Pradesh': ['Lucknow-Kanpur Road', 'Agra Expressway', 'Noida Extension', 'Ring Road'],
            'Rajasthan': ['Jaipur-Delhi Highway', 'Tonk Road', 'Ajmer Road', 'JLN Marg'],
            'West Bengal': ['EM Bypass', 'VIP Road', 'AJC Bose Road', 'Park Street']
        }
        
        self.create_widgets()
        self.update_dashboard()

    def generate_sample_data(self):
        data = []
        current_year = datetime.datetime.now().year
        
        states = ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Gujarat', 'Delhi', 
                 'Uttar Pradesh', 'Rajasthan', 'West Bengal']
        locations_map = {
            'Karnataka': ['MG Road Junction', 'Outer Ring Road', 'Mysore Road', 'Bannerghatta Road'],
            'Maharashtra': ['Mumbai-Pune Highway', 'Western Express', 'Eastern Freeway', 'LBS Marg'],
            'Tamil Nadu': ['Anna Salai', 'OMR Junction', 'GST Road', 'Mount Road'],
            'Gujarat': ['SG Highway', 'CG Road', 'Ashram Road', 'Sarkhej-Gandhinagar Highway'],
            'Delhi': ['Ring Road', 'NH-8 Junction', 'Outer Ring Road', 'Delhi-Gurgaon Border'],
            'Uttar Pradesh': ['Lucknow-Kanpur Road', 'Agra Expressway', 'Noida Extension', 'Ring Road'],
            'Rajasthan': ['Jaipur-Delhi Highway', 'Tonk Road', 'Ajmer Road', 'JLN Marg'],
            'West Bengal': ['EM Bypass', 'VIP Road', 'AJC Bose Road', 'Park Street']
        }
        
        for i in range(300):
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            
            state = random.choice(states)
            location = random.choice(locations_map[state])
            
            accident_types = ['Minor Collision', 'Major Collision', 'Hit and Run', 
                            'Pedestrian Involved', 'Vehicle Rollover']
            
            data.append({
                'id': i + 1,
                'date': f"{current_year}-{month:02d}-{day:02d}",
                'time': f"{hour:02d}:{minute:02d}",
                'state': state,
                'location': location,
                'type': random.choice(accident_types),
                'cctv_id': f"CAM-{state[:3].upper()}-{random.randint(1, 99)}"
            })
        
        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        df = df.sort_values('datetime', ascending=False).reset_index(drop=True)
        return df

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#1e293b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        header_frame = tk.Frame(main_frame, bg='#dc2626', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Multi-State Traffic Accident Dashboard", 
                font=('Arial', 24, 'bold'), bg='#dc2626', fg='white').pack(pady=10)
        tk.Label(header_frame, text="State-wise Analysis Using Poisson Distribution", 
                font=('Arial', 12), bg='#dc2626', fg='#fee2e2').pack()

        input_frame = tk.LabelFrame(main_frame, text="📹 Capture New Accident (CCTV Input)", 
                                   font=('Arial', 12, 'bold'), bg='white', fg='#1e293b', padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_grid = tk.Frame(input_frame, bg='white')
        input_grid.pack(fill=tk.X)

        tk.Label(input_grid, text="Date:", font=('Arial', 10), bg='white').grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(input_grid, font=('Arial', 10), width=12)
        self.date_entry.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_grid, text="Time:", font=('Arial', 10), bg='white').grid(row=0, column=2, padx=5, pady=5)
        self.time_entry = tk.Entry(input_grid, font=('Arial', 10), width=8)
        self.time_entry.insert(0, datetime.datetime.now().strftime('%H:%M'))
        self.time_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_grid, text="State:", font=('Arial', 10), bg='white').grid(row=0, column=4, padx=5, pady=5)
        self.state_var = tk.StringVar()
        self.state_combo = ttk.Combobox(input_grid, textvariable=self.state_var, 
                                       values=self.states, font=('Arial', 10), width=15, state='readonly')
        self.state_combo.bind('<<ComboboxSelected>>', self.update_location_dropdown)
        self.state_combo.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(input_grid, text="Location:", font=('Arial', 10), bg='white').grid(row=0, column=6, padx=5, pady=5)
        self.location_var = tk.StringVar()
        self.location_combo = ttk.Combobox(input_grid, textvariable=self.location_var, 
                                          font=('Arial', 10), width=20, state='readonly')
        self.location_combo.grid(row=0, column=7, padx=5, pady=5)

        tk.Label(input_grid, text="Type:", font=('Arial', 10), bg='white').grid(row=1, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_grid, textvariable=self.type_var, 
                                      values=self.accident_types, font=('Arial', 10), width=18, state='readonly')
        self.type_combo.current(0)
        self.type_combo.grid(row=1, column=1, columnspan=2)

        tk.Button(input_grid, text="Add Accident", font=('Arial', 10, 'bold'), 
                  bg='#dc2626', fg='white', padx=20, pady=5,
                  command=self.add_accident).grid(row=1, column=4, columnspan=2, padx=10, pady=5)

        filter_frame = tk.Frame(main_frame, bg='white', padx=10, pady=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter State:", font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT)
        self.filter_state_var = tk.StringVar(value='All States')
        ttk.Combobox(filter_frame, textvariable=self.filter_state_var, 
                     values=['All States'] + self.states, font=('Arial', 10), width=15, state='readonly'
                    ).pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Month:", font=('Arial', 10), bg='white').pack(side=tk.LEFT)
        self.month_var = tk.IntVar(value=datetime.datetime.now().month)
        ttk.Combobox(filter_frame, textvariable=self.month_var, 
                     values=list(range(1, 13)), font=('Arial', 10), width=5, state='readonly'
                    ).pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Year:", font=('Arial', 10), bg='white').pack(side=tk.LEFT)
        self.year_var = tk.IntVar(value=datetime.datetime.now().year)
        ttk.Combobox(filter_frame, textvariable=self.year_var, 
                     values=[2023, 2024, 2025], font=('Arial', 10), width=8, state='readonly'
                    ).pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="Update Dashboard", font=('Arial', 10, 'bold'), 
                  bg='#2563eb', fg='white', padx=15, pady=5,
                  command=self.update_dashboard).pack(side=tk.LEFT, padx=20)

        stats_frame = tk.Frame(main_frame, bg='#1e293b')
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stat_cards = []
        stat_labels = [
            ("Total Accidents\n(Selected Period)", '#dc2626'),
            ("Total Accidents\n(Year)", '#f97316'),
            ("Avg Accidents/Month\n(λ)", '#3b82f6'),
            ("States Covered", '#22c55e'),
            ("Total Records", '#a855f7')
        ]
        
        for i, (label, color) in enumerate(stat_labels):
            card = tk.Frame(stats_frame, bg=color, width=180, height=100)
            card.grid(row=0, column=i, padx=8, sticky='ew')
            card.grid_propagate(False)
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(card, text=label, font=('Arial', 8), bg=color, fg='white').pack(pady=(10, 0))
            value_label = tk.Label(card, text="0", font=('Arial', 22, 'bold'), bg=color, fg='white')
            value_label.pack()
            self.stat_cards.append(value_label)

        content_frame = tk.Frame(main_frame, bg='#1e293b')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        chart_frame = tk.Frame(content_frame, bg='white')
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.fig = Figure(figsize=(14, 9), facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        table_frame = tk.LabelFrame(content_frame, text="Recent Accidents (Top 25)", 
                                   font=('Arial', 11, 'bold'), bg='white', fg='#1e293b', width=450)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        table_frame.pack_propagate(False)

        tree_scroll = tk.Scrollbar(table_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(table_frame, columns=('ID', 'Date', 'Time', 'State', 'Location', 'Type'), 
                                show='headings', yscrollcommand=tree_scroll.set, height=30)
        tree_scroll.config(command=self.tree.yview)
        
        for col, width in zip(['ID','Date','Time','State','Location','Type'], [35,75,50,80,110,90]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_location_dropdown(self, event=None):
        selected_state = self.state_var.get()
        if selected_state in self.locations:
            self.location_combo['values'] = self.locations[selected_state]
            self.location_combo.current(0)

    def add_accident(self):
        date = self.date_entry.get()
        time = self.time_entry.get()
        state = self.state_var.get()
        location = self.location_var.get()
        acc_type = self.type_var.get()
        
        if not state or not location:
            messagebox.showwarning("Warning", "Please select state and location!")
            return
        
        new_id = self.accidents_df['id'].max() + 1
        cctv_id = f"CAM-{state[:3].upper()}-{random.randint(1, 99)}"
        
        new_row = pd.DataFrame([{
            'id': new_id,
            'date': date,
            'time': time,
            'state': state,
            'location': location,
            'type': acc_type,
            'cctv_id': cctv_id,
            'datetime': pd.to_datetime(f"{date} {time}")
        }])
        
        self.accidents_df = pd.concat([new_row, self.accidents_df], ignore_index=True)
        self.accidents_df = self.accidents_df.sort_values('datetime', ascending=False).reset_index(drop=True)
        
        messagebox.showinfo("Success", f"Accident added successfully!\nState: {state}\nCCTV ID: {cctv_id}")
        self.update_dashboard()

    def calculate_poisson_probability(self, lambda_val, k):
        if lambda_val == 0:
            return 0
        return (lambda_val ** k) * math.exp(-lambda_val) / math.factorial(k)

    def update_dashboard(self):
        selected_month = self.month_var.get()
        selected_year = self.year_var.get()
        selected_state = self.filter_state_var.get()
        
        self.accidents_df['date_obj'] = pd.to_datetime(self.accidents_df['date'])
        
        filtered_df = self.accidents_df if selected_state == 'All States' else \
                      self.accidents_df[self.accidents_df['state'] == selected_state]
        
        monthly_filtered = filtered_df[
            (filtered_df['date_obj'].dt.month == selected_month) &
            (filtered_df['date_obj'].dt.year == selected_year)
        ]
        yearly_filtered = filtered_df[filtered_df['date_obj'].dt.year == selected_year]

        self.stat_cards[0].config(text=str(len(monthly_filtered)))
        self.stat_cards[1].config(text=str(len(yearly_filtered)))

        monthly_counts = yearly_filtered.groupby(yearly_filtered['date_obj'].dt.month).size()
        avg_accidents = monthly_counts.mean() if len(monthly_counts) else 0
        self.stat_cards[2].config(text=f"{avg_accidents:.2f}")

        self.stat_cards[3].config(text=str(self.accidents_df['state'].nunique()))
        self.stat_cards[4].config(text=str(len(self.accidents_df)))

        self.fig.clear()

        # ---------------------------------------------
        # FIXED ALIGNMENT USING INCREASED PADDING + SMALLER TITLES
        # ---------------------------------------------
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(
            3, 2, figure=self.fig,
            hspace=0.75,   # FIX: Increased spacing between rows
            wspace=0.35,   # FIX: Increased spacing between columns
            left=0.07, right=0.95, top=0.94, bottom=0.06
        )
        title_size = 9  # FIX: Smaller titles for better spacing
        # ---------------------------------------------

        # (Charts code remains SAME, only titles modified)

        ax1 = self.fig.add_subplot(gs[0, 0])
        state_data = yearly_filtered.groupby('state').size().sort_values(ascending=False)
        ax1.barh(state_data.index, state_data.values)
        ax1.set_title(f'State-wise Accidents Comparison - {selected_year}', fontsize=title_size)
        ax1.set_xlabel('Number of Accidents', fontsize=8)
        ax1.tick_params(labelsize=7)
        ax1.invert_yaxis()

        ax2 = self.fig.add_subplot(gs[0, 1])
        top_states = yearly_filtered.groupby('state').size().nlargest(4).index
        months = range(1, 12 + 1)
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        
        for state in top_states:
            monthly_counts = [
                len(yearly_filtered[(yearly_filtered['state']==state) & 
                                    (yearly_filtered['date_obj'].dt.month==m)])
                for m in months
            ]
            ax2.plot(month_names, monthly_counts, marker='o')
        
        ax2.set_title('Monthly Trend - Top 4 States', fontsize=title_size)
        ax2.tick_params(axis='x', rotation=45, labelsize=7)
        ax2.grid(True, alpha=0.3)

        ax3 = self.fig.add_subplot(gs[1, 0])
        k_values = range(0, 20)
        poisson_probs = [self.calculate_poisson_probability(avg_accidents, k)*100 for k in k_values]
        ax3.plot(k_values, poisson_probs, marker='o')
        ax3.set_title(f'Poisson Distribution (λ={avg_accidents:.2f})', fontsize=title_size)
        ax3.set_xlabel('Accidents', fontsize=8)
        ax3.set_ylabel('Probability (%)', fontsize=8)
        ax3.grid(True, alpha=0.3)

        ax4 = self.fig.add_subplot(gs[1, 1])
        type_counts = monthly_filtered['type'].value_counts()
        ax4.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
        ax4.set_title('Accident Types Distribution', fontsize=title_size)

        ax5 = self.fig.add_subplot(gs[2, 0])
        top5 = yearly_filtered.groupby('state').size().nlargest(5).index
        matrix = []

        for t in self.accident_types:
            row = [len(yearly_filtered[(yearly_filtered['state']==s) & 
                                      (yearly_filtered['type']==t)]) for s in top5]
            matrix.append(row)

        matrix = np.array(matrix)
        im = ax5.imshow(matrix, cmap='YlOrRd')
        ax5.set_xticks(range(len(top5)))
        ax5.set_xticklabels(top5, rotation=45, fontsize=7)
        ax5.set_yticks(range(len(self.accident_types)))
        ax5.set_yticklabels(self.accident_types, fontsize=7)
        ax5.set_title('Accident Type Distribution by State', fontsize=title_size)

        for i in range(len(self.accident_types)):
            for j in range(len(top5)):
                ax5.text(j, i, matrix[i][j], ha='center', va='center', fontsize=7)

        ax6 = self.fig.add_subplot(gs[2, 1])
        monthly_filtered['hour'] = pd.to_datetime(monthly_filtered['time']).dt.hour
        hourly_counts = monthly_filtered.groupby('hour').size()
        
        ax6.bar(range(24), [hourly_counts.get(i,0) for i in range(24)])
        ax6.set_title('Hourly Accident Distribution', fontsize=title_size)
        ax6.tick_params(labelsize=7)

        self.canvas.draw()

        for item in self.tree.get_children():
            self.tree.delete(item)

        display_df = filtered_df if selected_state != 'All States' else self.accidents_df
        for _, row in display_df.head(25).iterrows():
            self.tree.insert('', 'end', values=(
                row['id'], row['date'], row['time'], row['state'], row['location'], row['type']
            ))

    def export_data(self):
        filename = f"accident_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.accidents_df.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Data exported to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficAccidentDashboard(root)
    root.mainloop()
