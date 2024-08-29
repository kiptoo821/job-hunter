import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import webbrowser
import warnings
import logging
from concurrent.futures import ThreadPoolExecutor

# Setup warnings and logging
warnings.filterwarnings('ignore')
logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Define URLs
URLS = {
    "MyJobMag": {
        "Banking": "https://www.myjobmag.co.ke/search/jobs?field=Banking&experience=1+-+4",
        "Data, Business Analysis and AI": "https://www.myjobmag.co.ke/search/jobs?field=Data%2C+Business+Analysis+and+AI&experience=1+-+4",
        "Finance, Accounting, Audit": "https://www.myjobmag.co.ke/search/jobs?field=Finance+%2F+Accounting+%2F+Audit&experience=1+-+4",
        "Internships, Volunteering": "https://www.myjobmag.co.ke/search/jobs?field=Internships+%2F+Volunteering&experience=1+-+4",
        "Research": "https://www.myjobmag.co.ke/search/jobs?field=Research&experience=1+-+4"
    }
}

class JobHunterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Hunter")
        self.root.geometry("800x600")
        self.original_data = None  # Initialize the original data storage
        
        self.create_widgets()
    
    def create_widgets(self):
        # URL Selection
        self.website_selector = ttk.Combobox(self.root, values=list(URLS.keys()), state="readonly")
        self.website_selector.set("Select Website")
        self.website_selector.pack(pady=10)
        self.website_selector.bind("<<ComboboxSelected>>", self.update_field_selector)
        
        # Field Selector
        self.field_selector = ttk.Combobox(self.root, state="readonly")
        self.field_selector.pack(pady=5)
        
        # Scrape Button
        self.scrape_button = ttk.Button(self.root, text="Scrape", command=self.scrape_data)
        self.scrape_button.pack(pady=5)
        
        # Filter and Search
        self.search_frame = ttk.Frame(self.root)
        self.search_frame.pack(pady=10)
        
        self.date_filter_label = ttk.Label(self.search_frame, text="Date Filter:")
        self.date_filter_label.pack(side=tk.LEFT, padx=5)
        self.date_filter_entry = ttk.Entry(self.search_frame)
        self.date_filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_button = ttk.Button(self.search_frame, text="Filter", command=self.filter_by_date)
        self.filter_button.pack(side=tk.LEFT, padx=5)
        
        self.search_label = ttk.Label(self.search_frame, text="Search by Position:")
        self.search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_by_position)
        self.search_button.pack(side=tk.LEFT, padx=5)
        # Add the Refresh Button
        self.refresh_button = ttk.Button(self.search_frame, text="Refresh", command=self.refresh_table)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Tree View
        self.tree = ttk.Treeview(self.root, columns=('Company', 'Position', 'Date posted', 'Link'), show='headings')
        self.tree.heading('Company', text='Company')
        self.tree.heading('Position', text='Position')
        self.tree.heading('Date posted', text='Date posted')
        self.tree.heading('Link', text='Link')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scroll Bars
        self.vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.vsb.pack(side='right', fill='y')
        self.hsb.pack(side='bottom', fill='x')
        
        # Buttons
        self.apply_button = ttk.Button(self.root, text="Apply", command=self.open_link)
        self.apply_button.pack(side=tk.LEFT, padx=5)
        self.export_button = ttk.Button(self.root, text="Export", command=self.export_data)
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        # Log Panel
        self.log_var = tk.StringVar()
        self.log_label = ttk.Label(self.root, textvariable=self.log_var, anchor='w')
        self.log_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    def update_field_selector(self, event):
        selected_website = self.website_selector.get()
        fields = list(URLS.get(selected_website, {}).keys())
        self.field_selector['values'] = fields
        if fields:
            self.field_selector.set(fields[0])
        else:
            self.field_selector.set('')


    def fetch_page_data(self, page, base_url):
        url = f'{base_url}&currentpage={page}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            jobs = soup.find_all('li', class_='job-info')

            jobs_data = []
            for job in jobs:
                name_text = job.find('h2').text.strip()
                title = text_before_at(name_text)
                company = text_after_at(name_text)
                date_post = job.find(id='job-date').text.strip()
                link = job.h2.a['href']
                jobs_data.append({
                    'Company': company,
                    'Position': title,
                    'Date posted': date_post,
                    'Link': f'https://www.myjobmag.co.ke{link}'
                })

            return jobs_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Network error on page {page}: {e}")
            return []
        except Exception as e:
            logging.error(f"Error parsing page {page}: {e}")
            return []

    def get_data(self, url):
        jobs_data = []
        page = 1

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            total_jobs_text = soup.find('h1').text
            total_jobs = find_integer_in_text(total_jobs_text)

            jobs_per_page = len(soup.find_all('li', class_='job-info'))
            total_pages = (total_jobs // jobs_per_page) + 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Network error while fetching total jobs: {e}")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"Error finding total jobs: {e}")
            return pd.DataFrame()

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda page: self.fetch_page_data(page, url), range(1, total_pages + 1)))

        jobs_data = [job for sublist in results for job in sublist]
        return pd.DataFrame(jobs_data)

    def scrape_data(self):
        site_name = self.website_selector.get()
        field_name = self.field_selector.get()
        base_url = URLS.get(site_name, {}).get(field_name)
        if not base_url:
            messagebox.showwarning("Input Error", "Please select valid site and field.")
            return

        try:
            df = self.get_data(base_url)
            if not df.empty:
                self.original_data = df  # Store the original data
                self.populate_table(df)
                self.log_var.set("Scraping completed successfully.")
            else:
                self.log_var.set("No data scraped.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log_var.set(f"Error: {str(e)}")
    
    def refresh_table(self):
        if hasattr(self, 'original_data'):  # Check if original data is available
            self.populate_table(self.original_data)
            self.log_var.set("Table refreshed to original data.")
        else:
            self.log_var.set("No original data to refresh.")

    def populate_table(self, data):
        # Clear the current data in the table
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Insert new data into the table
        for _, row in data.iterrows():
            self.tree.insert('', tk.END, values=row.tolist())

    def export_data(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Export Error", "No rows selected to export.")
            return

        data = [self.tree.item(item, 'values') for item in selected_items]
        df = pd.DataFrame(data, columns=['Company', 'Position', 'Date posted', 'Link'])

        try:
            df.to_excel('selected_jobs.xlsx', sheet_name='jobs', index=False)
            self.log_var.set("Export completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log_var.set(f"Error: {str(e)}")

    def filter_by_date(self):
        date_filter = self.date_filter_entry.get()
        if not date_filter:
            self.log_var.set("Please enter a date to filter.")
            return

        for row in self.tree.get_children():
            item_date = self.tree.item(row, 'values')[2]
            if date_filter not in item_date:
                self.tree.delete(row)
        
        self.log_var.set("Filtering completed.")

    def search_by_position(self):
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.log_var.set("Please enter a position to search.")
            return

        for row in self.tree.get_children():
            item_position = self.tree.item(row, 'values')[1].lower()
            if search_term not in item_position:
                self.tree.delete(row)
        
        self.log_var.set("Search completed.")

    def open_link(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Apply Error", "No row selected.")
            return
        
        link = self.tree.item(selected_item[0], 'values')[3]
        webbrowser.open(link)

# Helper functions
def text_before_at(text):
    match = re.search(r'(.*)\bat\b', text)
    return match.group(1).strip() if match else None

def text_after_at(text):
    match = re.search(r'\bat\b(.*)', text)
    return match.group(1).strip() if match else None

def find_integer_in_text(text):
    try:
        match = re.search(r'\d+', text)
        return int(match.group()) if match else None
    except Exception as e:
        logging.error(f"Error finding integer in text: {e}")
        return None

# Create and run the application
def main():
    root = tb.Window(themename="superhero")
    app = JobHunterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()