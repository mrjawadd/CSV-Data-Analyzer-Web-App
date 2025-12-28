# CSV Data Analyzer Web App

A Flask-based web application designed to help users quickly analyze CSV files. This app allows you to upload your datasets, explore the data, generate statistical summaries, identify missing values, and create interactive visualizations—all from a simple web interface. It is ideal for data enthusiasts, students, or anyone who wants to gain insights from CSV files without writing any code.

## Features

* **CSV File Upload:** Easily upload your CSV files through a user-friendly interface.
* **Data Preview:** View the first few rows of your dataset to get an immediate overview of the data.
* **Column Information:** Quickly check column names, data types, and basic metadata.
* **Missing Value Analysis:** Detect and visualize missing values to understand data quality issues.
* **Statistical Summary:** Generate descriptive statistics including mean, median, standard deviation, min, and max for numeric columns.
* **Interactive Charts:** Visualize your data with interactive plots such as bar charts, histograms, and scatter plots.
* **Summary CSV Download:** Export the analyzed summary and cleaned data as a new CSV file for further use.

## Installation and Setup

To run this application locally:

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask application:

   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000/` to access the app.

## Usage

1. Upload your CSV file using the upload form.
2. Preview the data and check column information.
3. Explore missing values and statistical summaries.
4. Generate interactive visualizations to gain insights.
5. Download the summary CSV for offline use.

## Technologies Used

* **Flask** – Web framework for Python.
* **Pandas** – For data manipulation and analysis.
* **Matplotlib / Seaborn / Plotly** – For generating charts and visualizations.
* **HTML/CSS/Bootstrap** – Frontend interface for user interaction.

## Future Improvements

* Add support for multiple file formats (Excel, JSON).
* Include more advanced visualization options like heatmaps and pair plots.
* Add user authentication to save and manage datasets securely.
