# SmartSiteReviewer

## Overview

SmartSiteReviewer is a Python application that leverages the OpenAI API to analyze websites and generate detailed reviews. The application provides a user-friendly interface built with Tkinter, allowing users to input a CSV file containing website information and receive structured feedback on various aspects of the sites, including performance, design, and accessibility.

## Features

- **CSV Input**: Load a CSV file containing website names and URLs for analysis.
- **OpenAI Integration**: Utilize the OpenAI API to generate comprehensive reviews based on user-defined prompts.
- **Progress Feedback**: Visual indicators to show loading status while processing requests.
- **Output Generation**: Save the generated reviews and emails to a specified output file.
- **User-Friendly Interface**: Simple and intuitive GUI for easy interaction.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- OpenAI Python client library
- CSV file for input

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartSiteReviewer.git
   cd SmartSiteReviewer
   ```

2. Install the required packages:
   ```bash
   pip install openai
   ```

3. Ensure you have a valid OpenAI API key.

## Usage

1. Run the application:
   ```bash
   python AICall_scraper_v1.py
   ```

2. Input the required fields:
   - Select the input CSV file containing website data.
   - Specify the output file path for saving results.
   - Enter your OpenAI API key.
   - Choose the model (e.g., `gpt-4o`).
   - Provide a prompt for the analysis.

3. Click the "Run Script" button to start the analysis.

4. Once completed, the results will be saved to the specified output file, and a success message will be displayed.

## Example CSV Format

The input CSV doesnt have a specific Formatting.
