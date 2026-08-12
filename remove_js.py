import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = "    document.addEventListener('DOMContentLoaded', () => {\n      const track = document.querySelector('.testimonials-track');"
end_str = "        });\n      }\n\n    });"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_str)
    content = content[:start_idx] + "    // Testimonials JS removed for continuous CSS marquee\n" + content[end_idx:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully removed the testimonials JS block.")
else:
    print("Could not find the start or end string.")
