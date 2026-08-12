import re
import glob

for filename in glob.glob('*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add -webkit-clip-path if missing
    content = re.sub(r'(?<!-webkit-)clip-path:\s*([^;]+);', lambda m: f'-webkit-clip-path: {m.group(1)};\n      clip-path: {m.group(1)};', content)
    
    # Add -webkit-backdrop-filter if missing
    content = re.sub(r'(?<!-webkit-)backdrop-filter:\s*([^;]+);', lambda m: f'-webkit-backdrop-filter: {m.group(1)};\n      backdrop-filter: {m.group(1)};', content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Added iOS vendor prefixes to all HTML files")
