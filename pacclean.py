import subprocess
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QScrollArea, QCheckBox, QPushButton, 
                            QLabel, QMessageBox)

def list_packages():
    # Run pacman to list all packages with dependency info
    cmd = "pacman -Qent"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Check if the command was successful
    if result.returncode != 0:
        print("Error running pacman command:", result.stderr)
        return []

    # Split the output into lines
    packages = result.stdout.strip().split('\n')
    package_list = []

    for package in packages:
        # Split the package name and version
        name, version = package.split(' ', 1)

        info_result = subprocess.run(f"pacman -Qi {name}", shell=True, capture_output=True, text=True)
        if info_result.returncode != 0:
            print(f"Error getting info for package {name}: {info_result.stderr}")
            continue
        # Parse the package info to extract Description
        info_text = info_result.stdout
        description = "No description"

        # Look for the Description line in the package info
        for line in info_text.split('\n'):
            if line.startswith("Description"):
                # Extract the description part after the colon
                description = line.split(':', 1)[1].strip()
                break

        name = f"{name} - {description}"

        # Append the package name to the list
        package_list.append(name)

    return package_list

def ui():
    # Create the main application
    app = QApplication(sys.argv)
    
    # Create the main window
    window = QMainWindow()
    window.setWindowTitle("Pacclean - Package Manager")
    window.resize(600, 500)
    
    # Create central widget and main layout
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)
    
    # Add a label
    label = QLabel("Select packages to manage:")
    main_layout.addWidget(label)
    
    # Create scrollable area
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    
    # Get all packages
    packages = list_packages()
    
    # Create dictionary to store checkbox states
    checkbox_dict = {}
    
    # Add checkboxes for each package
    for package in packages:
        checkbox = QCheckBox(package)
        scroll_layout.addWidget(checkbox)
        checkbox_dict[package] = checkbox
    
    # Set the scroll content and add to main layout
    scroll_area.setWidget(scroll_content)
    main_layout.addWidget(scroll_area)
    
    # Function to handle button click
    def get_selected_packages():
        selected = [pkg.split(' ')[0] for pkg, checkbox in checkbox_dict.items() if checkbox.isChecked()]
        if selected:
            print("sudo pacman -R", " ".join(selected))
        else:
            QMessageBox.information(window, "Selection", "No packages selected")
        return selected
    
    # Add button at the bottom
    button_layout = QHBoxLayout()
    select_button = QPushButton("Process Selected Packages")
    select_button.clicked.connect(get_selected_packages)
    button_layout.addStretch()
    button_layout.addWidget(select_button)
    main_layout.addLayout(button_layout)
    
    # Show the window and run the application
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ui()