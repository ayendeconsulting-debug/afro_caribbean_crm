import os
import re

# Common emojis to find
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"
    "]+", 
    flags=re.UNICODE
)

def find_emojis_in_file(filepath):
    """Find all emojis in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            emojis = EMOJI_PATTERN.findall(content)
            if emojis:
                print(f"\nFound emojis in: {filepath}")
                print(f"Emojis: {set(emojis)}")
                return True
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return False

def scan_directory(directory):
    """Recursively scan directory for emojis."""
    files_with_emojis = []
    
    for root, dirs, files in os.walk(directory):
        # Skip venv and migrations
        if 'venv' in root or 'migrations' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith(('.py', '.html', '.js', '.css')):
                filepath = os.path.join(root, file)
                if find_emojis_in_file(filepath):
                    files_with_emojis.append(filepath)
    
    return files_with_emojis

if __name__ == '__main__':
    project_dir = '.'  # Current directory
    print("Scanning for emojis...")
    files = scan_directory(project_dir)
    
    print(f"\n\nSummary: Found emojis in {len(files)} files")
    if files:
        print("\nFiles to clean:")
        for f in files:
            print(f"  - {f}")