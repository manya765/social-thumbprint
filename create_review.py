import os
import glob

def create_review_page():
    base_dir = r"d:\social thumbrint"
    videos_dir = os.path.join(base_dir, "videos")
    
    # Get all mp4 files
    mp4_files = glob.glob(os.path.join(videos_dir, "*.mp4"))
    
    # Filter out the kira ones we already know
    unknown_videos = [f for f in mp4_files if "kira" not in os.path.basename(f).lower()]
    unknown_videos.sort()
    
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Video Review & Classification</title>
<style>
  body { font-family: sans-serif; background: #111; color: #fff; padding: 2rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; }
  .card { background: #222; padding: 1rem; border-radius: 8px; text-align: center; }
  video { width: 100%; height: 200px; object-fit: cover; background: #000; border-radius: 4px; margin-bottom: 1rem; }
  h3 { margin: 0 0 1rem 0; font-size: 1.2rem; color: #00B0B9; }
</style>
</head>
<body>
  <h1>Video Review Dashboard</h1>
  <p>Please review these videos and let me know which video belongs to which campaign (e.g., SBA, Baulkline, Kokolo, etc.)</p>
  
  <div class="grid">
"""
    for video in unknown_videos:
        filename = os.path.basename(video)
        html += f"""
    <div class="card">
      <video controls>
        <source src="videos/{filename}" type="video/mp4">
      </video>
      <h3>{filename}</h3>
    </div>
"""

    html += """
  </div>
</body>
</html>
"""

    with open(os.path.join(base_dir, "video-review.html"), "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Video review page created.")

if __name__ == "__main__":
    create_review_page()
