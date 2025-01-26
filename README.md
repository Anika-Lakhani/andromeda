# Intern Onboarding Guide

A dual-interface onboarding system that provides information about Andromeda Protocol's internship program through both a CLI and web interface. The system uses OpenAI's API to provide intelligent responses to follow-up questions.

## Prerequisites

- Python 3.8+
- OpenAI API key
- Required Python packages:
  ```bash
  pip install flask openai
  ```

## Project Structure
intern_onboarding/
├── web_onboarding.py # Web interface server
├── intern_onboarding.py # Core functionality and CLI interface
├── apikey.txt # OpenAI API key
├── static/ # Web static files
│ ├── style.css
│ └── script.js
├── templates/ # Web HTML templates
│ ├── index.html
│ ├── company_overview.html
│ ├── responsibilities.html
│ ├── tools.html
│ └── expectations.html
└── txt_files/ # Content files
├── company_info.txt
├── company_summary.txt
├── tools_summary.txt
├── external_tools.txt
├── expectations_summary.txt
├── project_expectations.txt
├── marketing_responsibilities.txt
├── tech_responsibilities.txt
├── ops_responsibilities.txt
├── ai_responsibilities.txt
└── intern_responsibilities.txt


## Setup

1. Clone the repository
2. Create an `apikey.txt` file in the root directory and add your OpenAI API key
3. Ensure all required text files are present in the `txt_files` directory

## Running the CLI Interface

1. Open a terminal in the project directory
2. Run the CLI version:
   ```bash
   python intern_onboarding.py
   ```
3. Use the numbered menu to navigate:
   - 1: Company Overview
   - 2: Intern Responsibilities
   - 3: Tools & Technologies
   - 4: Project Expectations
   - 5: Save Conversation
   - 6: Exit

4. For intern responsibilities, select your intern type:
   - Marketing
   - Tech
   - Operations
   - AI
   - I don't know

5. After viewing information, you can ask follow-up questions
   - Enter 'Y' when prompted for follow-up questions
   - Type your question
   - Get AI-powered responses using the OpenAI API

## Running the Web Interface

1. Open a terminal in the project directory
2. Start the web server:
   ```bash
   python web_onboarding.py
   ```
3. Open a web browser and navigate to:
   ```
   http://localhost:5000 or other URL given by the terminal
   ```
4. Use the navigation tabs to access different sections:
   - Company Overview
   - Intern Responsibilities
   - Tools & Technologies
   - Project Expectations
   - Save Conversation

5. For intern responsibilities:
   - Select your intern type from the dropdown
   - View role-specific information
   - Ask follow-up questions using the question input field

## Features

- Dual interface (CLI and Web)
- Role-specific information for different intern types
- AI-powered responses to follow-up questions
- Conversation history saving
- Comprehensive information about:
  - Company overview
  - Intern responsibilities
  - Tools and technologies
  - Project expectations

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `apikey.txt` exists and contains a valid OpenAI API key
   - Check file permissions

2. **Missing Text Files**
   - Verify all required .txt files exist in the correct directory
   - Check file permissions

3. **Web Interface Not Loading**
   - Confirm Flask is running (check terminal output)
   - Verify you're using the correct URL
   - Check browser console for JavaScript errors

4. **No AI Responses**
   - Verify internet connection
   - Check API key validity
   - Look for error messages in terminal output

### Getting Help

If you encounter issues:
1. Check the terminal output for error messages
2. For web interface issues, use browser developer tools (F12)
3. Verify all dependencies are installed correctly
4. Ensure all required files are present and readable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

Copyright (c) 2024 Anika Lakhani with Andromeda Protocol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.