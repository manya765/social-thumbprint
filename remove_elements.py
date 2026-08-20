import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Remove the art-chip lines
index_content = re.sub(r'^\s*<div class="art-chip[^>]*>.*?</div>\n', '', index_content, flags=re.MULTILINE)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

# 2. Update portfolio.html
with open('portfolio.html', 'r', encoding='utf-8') as f:
    portfolio_content = f.read()

# Remove the sm-work-details blocks
portfolio_content = re.sub(
    r'\s*<div class="sm-work-details">\s*<h3 class="sm-work-title">.*?</h3>\s*<p class="sm-work-tags">.*?</p>\s*</div>',
    '',
    portfolio_content,
    flags=re.DOTALL
)

with open('portfolio.html', 'w', encoding='utf-8') as f:
    f.write(portfolio_content)

print("Updates completed successfully.")
