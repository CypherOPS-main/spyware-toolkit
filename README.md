# CypherOps Spyware Toolkit

The CypherOps Spyware Toolkit is a simple and versatile command-line tool designed to assist in installing and managing various software programs on both Windows and Linux operating systems. This tool is especially useful for setting up software commonly used in cybersecurity, penetration testing, and network analysis.

## Features

- Cross-platform compatibility: The toolkit works on both Windows and Linux.
- Easy installation: The toolkit automatically checks and installs required dependencies such as `pipx` for Python package management.
- Simple program installation: Easily install specified programs from a predefined list with just a few commands.
- Program customization: The list of available programs can be extended and customized by editing the `list.json` file.

## Getting Started

1. **Clone the Repository:** Clone the CypherOps Spyware Toolkit repository using the following command:

   ```bash
   git clone https://github.com/CypherOPS-main/spyware-toolkit.git
   ```

2. **Navigate to the Directory:** Move into the cloned repository's directory:

   ```bash
   cd spyware-toolkit
   ```

3. **Install Required Packages:** Install the necessary Python packages using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Toolkit:** Execute the toolkit by running the main Python script:

   - On Windows:

     ```bash
     python main.py
     ```

   - On Linux:

     ```bash
     python3 main.py
     ```

5. **Follow the Menu:** Choose the desired action from the provided menu options.

## Usage

1. **Install Programs:** Select this option to install specified programs from the predefined list. Programs are automatically installed based on the operating system you are using.

2. **List Programs:** View the available programs along with their descriptions.

3. **Add a Program:** Extend the list of available programs by adding new entries to the `list.json` file. Specify program details, including the name, description, and installation instructions for Windows and Linux.

4. **Exit:** Quit the toolkit.

## Customization

To customize the available programs, edit the `list.json` file in the repository. Each program entry contains information for both Windows and Linux installations, including package managers, commands, or `pipx` package names.

## Requirements

- Python 3.6+
- For Linux installations, ensure that you have the appropriate permissions for executing installation commands.