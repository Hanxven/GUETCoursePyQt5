# GUETCoursePyQt

A script written by PyQt5 Library

# Configuration & Environment

- Python Interpreter: python3.9 x64
- IDE: IntelliJ PyCharm 2021.1.3 (Community Edition)
- Required: see also `requirements.txt`

---

# Other Information

- Author: Hanxven Marvels 7/3/2021

# PyCharm Settings - External Tools

File > Settings > Tools > External Tools:

You need to add a tools group named "Qt":

- Qt Designer:
  - Program: ... designer.exe (where your `pyqt5-tools` is installed)
  - Arguments: `$FilePath$`
  - Working directory: `$ProjectFileDir$`


- Qt UI Compiler
  - Program: ... pyuic5.exe (where your `pyqt5-tools` is installed)
  - Arguments: `-o UI_$FileNameWithoutExtension$.py $FileName$`
  - Working directory: `$FileDir$`


- Qt RCC Comelier
  - Program: ... pyrcc5.exe (where your `pyqt5-tools` is installed)
  - Arguments: `-o $FileDir$\RCC_$FileNameWithoutExtension$.py $FilePath$`
  - Working directory: `$ProjectFileDir$`