import os
import glob
import re

def update_portfolio():
    base_dir = r"d:\social thumbrint"
    portfolio_path = os.path.join(base_dir, "portfolio.html")
    videos_dir = os.path.join(base_dir, "videos")
    
    mp4_files = glob.glob(os.path.join(videos_dir, "*.mp4"))
    
    # Sort files naturally
    import re as regex
    def natural_keys(text):
        return [ int(c) if c.isdigit() else c for c in regex.split(r'(\d+)', text) ]
    
    mp4_files.sort(key=natural_keys)
    
    cards_html = ""
    for video in mp4_files:
        filename = os.path.basename(video)
        # Skip the massive TV video for the main grid if we want, but let's include it for now.
        title = filename.replace('.mp4', '').title()
        
        cards_html += f"""
        <div class="work-card reveal-heading in-view">
          <div class="work-img" style="padding: 0; background: #000; overflow: hidden; position: relative;">
             <video src="videos/{filename}" muted loop onmouseover="this.play()" onmouseout="this.pause()" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;"></video>
             <div class="work-overlay">Play Reel</div>
          </div>
          <div class="work-info">
            <h4>Project: {title}</h4>
            <p>Content Production</p>
          </div>
        </div>
"""

    with open(portfolio_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace the contents of the work-grid
    # Find <div class="work-grid" ...> ... </div>
    # This might be tricky with regex, so let's just replace the whole section.
    
    # The portfolio body from generate_pages.py is:
    # <section class="portfolio-gallery" style="padding: 2rem 0 6rem;">
    #   <div class="container">
    #     <div class="work-grid" style="grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem;">
    
    pattern = r'(<div class="work-grid" style="grid-template-columns: repeat\(auto-fit, minmax\(320px, 1fr\)\); gap: 2rem;">).*?(</section>)'
    
    new_grid = f'\\1\n{cards_html}\n      </div>\n    </div>\n  \\2'
    
    new_content = re.sub(pattern, new_grid, content, flags=re.DOTALL)
    
    with open(portfolio_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Portfolio updated with video cards.")

if __name__ == "__main__":
    update_portfolio()
