---

# Job Hunter - Web Scraping Desktop Application

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Important Notes](#important-notes)
- [Disclaimer](#disclaimer)

## Project Overview

**Job Hunter** is a desktop application built using Python's `tkinter` library, enhanced with `ttkbootstrap` for a modern look and feel. The application scrapes job listings from selected websites and displays the results in a user-friendly interface. The application allows users to filter job listings by date, search by job position, and export selected job listings to an Excel file. Users can also open job links directly in a web browser and refresh the data to its original state.

## Features

- **Website Selection:** Choose from predefined websites to scrape job listings.
- **Field Selector:** Select specific fields (e.g., Banking, Finance) to scrape targeted job listings.
- **Job Listings Display:** View job listings in a table with columns for Company, Position, Date Posted, and Link.
- **Date Filter:** Filter job listings by the date they were posted.
- **Search by Position:** Search for jobs based on specific keywords in the job title.
- **Export to Excel:** Export selected job listings to an Excel file for easy access and sharing.
- **Apply Button:** Open the selected job listing link directly in your default web browser.
- **Refresh Button:** Reset the table data to its original state before any filters were applied.
- **Log Panel:** View status messages and logs during scraping and other operations.

## Technologies Used

- **Python 3.x**
- **Tkinter**: For building the GUI.
- **ttkbootstrap**: For modern styling of the Tkinter widgets.
- **pandas**: For data manipulation and exporting to Excel.
- **requests**: For making HTTP requests to scrape data.
- **BeautifulSoup**: For parsing HTML and scraping job listings from web pages.
- **openpyxl**: For working with Excel files.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/job-hunter.git
   cd job-hunter
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python job_hunter.py
   ```

## Usage

1. **Select Website and Field:**
   - Choose the website and the job field from the dropdown menus.

2. **Scrape Data:**
   - Click the "Scrape" button to fetch the job listings.

3. **Filter/Search Jobs:**
   - Use the date filter to view jobs posted within a specific timeframe.
   - Use the search bar to find jobs by position.

4. **Apply for Jobs:**
   - Select a job listing and click the "Apply" button to open the job link in your web browser.

5. **Export Data:**
   - Select the desired job listings and click "Export" to save them in an Excel file.

6. **Refresh Data:**
   - Click the "Refresh" button to reset the table to its original state before any filtering or searching.

## Code Structure

```plaintext
├── assets/                # Folder containing images and other assets
├── job_hunter.py          # Main application script
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── .gitignore             # Files and directories to ignore in Git
```

### Important Methods:
- `scrape_data()`: Fetches job listings from the selected website.
- `populate_table(data)`: Populates the table with job listings.
- `refresh_table()`: Resets the table to the original job listings data.
- `filter_by_date()`: Filters the table based on the posted date.
- `search_by_position()`: Searches for job listings by position.
- `export_to_excel()`: Exports selected job listings to an Excel file.

## Customization

- **Adding More Websites:** To add more websites or fields, update the `URLS` dictionary in `job_hunter.py` with the necessary URLs.
- **Modular Code:** The code is modular, allowing easy updates and scalability. You can add more features or customize the existing ones as per your needs.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch for your feature or bug fix, and submit a pull request for review.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) for providing a modern theme for the Tkinter GUI.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [requests](https://docs.python-requests.org/en/latest/) for simplifying the web scraping process.
- OpenAI for developing the GPT-4 model that assisted in developing this project.

## Important Notes

- Please be considerate when scraping websites. Frequent and aggressive scraping may put strain on the website's server. Make sure to review the website's terms of service and robots.txt file to ensure compliance with their policies.

- This script is specifically designed for Myjobmag site and may require modification if you intend to use it with other job search websites.

- The script uses basic error handling but may require further enhancements for robustness and reliability in a production environment.

- Make sure you have the required Python packages installed before running the script.


## Disclaimer

This script is provided for educational purposes and personal use. Be mindful of the legality and ethical considerations when scraping websites, and always respect the terms of service of the website you are scraping.
---
