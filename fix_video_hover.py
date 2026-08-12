import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove hover play/pause handlers because user wants autoplay
content = re.sub(r' onmouseover="this\.play\(\)"', '', content)
content = re.sub(r' onmouseout="this\.pause\(\)"', '', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed hover handlers")
