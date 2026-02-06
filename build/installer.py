import subprocess
import sys
import os

def install_requirements():
    print("Installing dependencies for Musica...")
    try:
        # Get the path to packages.txt relative to this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(current_dir, "packages.txt")
        
        if not os.path.exists(requirements_path):
            print(f"Error: {requirements_path} not found.")
            return False

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("\nDependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError installing dependencies: {e}")
        return False

if __name__ == "__main__":
    if install_requirements():
        print("\nSetup complete. You can now run the app using 'python build/musica.py' or 'run.bat'.")
    else:
        print("\nSetup failed. Please check the errors above.")
