import nltk
import sys
import subprocess

def download_nltk_data():
    print("Downloading required NLTK data...")
    try:
        # Download required NLTK data
        nltk.download('wordnet')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        print("NLTK data downloaded successfully!")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        sys.exit(1)

def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except Exception as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Setting up CareerPro AI...")
    install_requirements()
    download_nltk_data()
    print("Setup completed successfully!") 