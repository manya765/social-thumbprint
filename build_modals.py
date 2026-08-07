import os
import glob
import re
from collections import defaultdict

def build_modals():
    base_dir = r"d:\social thumbrint"
    videos_dir = os.path.join(base_dir, "videos")
    
    mp4_files = glob.glob(os.path.join(videos_dir, "*.mp4"))
    
    brands = {
        "Adorne": [],
        "Arctic Star": [],
        "Baggit": [],
        "Baulkline": [],
        "Kira": [],
        "Luzo": [],
        "Meena Bazaar": [],
        "Riwaaj": [],
        "The Cappacino Collection": [],
        "Velvet Reverie": []
    }
    
    for f in mp4_files:
        basename = os.path.basename(f)
        lower_name = basename.lower()
        matched = False
        for brand in brands.keys():
            # For "The Cappacino Collection", just "cappacino" is fine
            search_brand = "cappacino" if brand == "The Cappacino Collection" else brand.lower()
            if search_brand in lower_name:
                brands[brand].append(basename)
                matched = True
                break
        if not matched:
            print(f"Warning: could not match {basename} to a brand")
            
    # Sort videos within brands
    for brand in brands:
        brands[brand].sort()
        
    print({k: len(v) for k, v in brands.items()})

    # 1. Generate the brand cards for portfolio.html
    cards_html = ""
    for brand, videos in brands.items():
        if not videos: continue
        # Data attribute holds JSON of videos
        videos_json = "[" + ",".join([f"'{v}'" for v in videos]) + "]"
        
        cards_html += f"""
        <div class="work-card reveal-heading in-view brand-card" data-brand="{brand}" data-videos="{videos_json}" style="cursor: pointer;">
          <div class="work-img">
            <div class="work-overlay">View Campaign</div>
          </div>
          <div class="work-info">
            <h4>{brand}</h4>
            <p>{len(videos)} Video{'s' if len(videos) > 1 else ''}</p>
          </div>
        </div>
"""

    portfolio_path = os.path.join(base_dir, "portfolio.html")
    with open(portfolio_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace grid content in portfolio.html
    pattern = r'(<div class="work-grid" style="grid-template-columns: repeat\(auto-fit, minmax\(320px, 1fr\)\); gap: 2rem;">).*?(</section>)'
    new_grid = f'\\1\n{cards_html}\n      </div>\n    </div>\n  \\2'
    content = re.sub(pattern, new_grid, content, flags=re.DOTALL)

    # 2. The Modal HTML, CSS, JS
    modal_code = """
  <!-- VIDEO MODAL -->
  <style>
    .video-modal {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0, 0, 0, 0.9);
      backdrop-filter: blur(10px);
      z-index: 99999;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }
    .video-modal.active {
      opacity: 1;
      pointer-events: all;
    }
    .video-modal-close {
      position: absolute;
      top: 30px; right: 40px;
      background: none; border: none; color: white;
      font-size: 3rem; cursor: pointer;
      line-height: 1;
      z-index: 100000;
    }
    .video-modal-content {
      width: 90%;
      max-width: 1000px;
      position: relative;
    }
    .video-player-container {
      width: 100%;
      padding-bottom: 56.25%; /* 16:9 */
      position: relative;
      background: #000;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 10px 40px rgba(0,176,185,0.2);
    }
    .video-player-container video {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      object-fit: contain;
    }
    .video-modal-header {
      margin-bottom: 1rem;
      text-align: center;
    }
    .video-modal-header h2 {
      color: var(--teal-light);
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }
    .video-controls-custom {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-top: 1.5rem;
    }
    .vid-btn {
      background: var(--teal);
      color: white;
      border: none;
      padding: 0.75rem 1.5rem;
      border-radius: 999px;
      font-weight: bold;
      cursor: pointer;
      display: none;
    }
    .vid-btn.active {
      display: inline-block;
    }
    .vid-counter {
      color: var(--ink-soft);
      align-self: center;
      font-size: 1.1rem;
      display: none;
    }
    .vid-counter.active {
      display: inline-block;
    }
  </style>

  <div class="video-modal" id="videoModal">
    <button class="video-modal-close" id="closeModal">&times;</button>
    <div class="video-modal-content">
      <div class="video-modal-header">
        <h2 id="modalBrandTitle">Brand</h2>
      </div>
      <div class="video-player-container">
        <video id="modalVideoPlayer" controls autoplay>
          <source src="" type="video/mp4">
        </video>
      </div>
      <div class="video-controls-custom">
        <button class="vid-btn" id="prevVideo">&larr; Previous</button>
        <span class="vid-counter" id="videoCounter">1 / 3</span>
        <button class="vid-btn" id="nextVideo">Next &rarr;</button>
      </div>
    </div>
  </div>

  <script>
    const modal = document.getElementById('videoModal');
    const closeBtn = document.getElementById('closeModal');
    const videoPlayer = document.getElementById('modalVideoPlayer');
    const modalBrandTitle = document.getElementById('modalBrandTitle');
    const prevBtn = document.getElementById('prevVideo');
    const nextBtn = document.getElementById('nextVideo');
    const counter = document.getElementById('videoCounter');
    
    let currentVideos = [];
    let currentIndex = 0;

    function openModal(brand, videosArray) {
      currentVideos = videosArray;
      currentIndex = 0;
      modalBrandTitle.textContent = brand;
      updateVideo();
      modal.classList.add('active');
    }

    function updateVideo() {
      if (currentVideos.length === 0) return;
      videoPlayer.src = 'videos/' + currentVideos[currentIndex];
      videoPlayer.play();
      
      if (currentVideos.length > 1) {
        prevBtn.classList.add('active');
        nextBtn.classList.add('active');
        counter.classList.add('active');
        counter.textContent = (currentIndex + 1) + ' / ' + currentVideos.length;
        
        prevBtn.disabled = currentIndex === 0;
        prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
        nextBtn.disabled = currentIndex === currentVideos.length - 1;
        nextBtn.style.opacity = currentIndex === currentVideos.length - 1 ? '0.5' : '1';
      } else {
        prevBtn.classList.remove('active');
        nextBtn.classList.remove('active');
        counter.classList.remove('active');
      }
    }

    prevBtn.addEventListener('click', () => {
      if (currentIndex > 0) { currentIndex--; updateVideo(); }
    });
    nextBtn.addEventListener('click', () => {
      if (currentIndex < currentVideos.length - 1) { currentIndex++; updateVideo(); }
    });

    closeBtn.addEventListener('click', () => {
      modal.classList.remove('active');
      videoPlayer.pause();
      videoPlayer.src = '';
    });

    // Attach to cards
    document.querySelectorAll('.brand-card').forEach(card => {
      card.addEventListener('click', (e) => {
        e.preventDefault();
        const brand = card.getAttribute('data-brand');
        // Simple manual parsing to avoid strict JSON errors with single quotes
        const rawVideos = card.getAttribute('data-videos');
        const videos = rawVideos.replace(/^\\[|\\]$/g, '').split(',').map(s => s.replace(/^'|'$/g, '').trim());
        openModal(brand, videos);
      });
    });
  </script>
"""

    # Inject modal into portfolio.html before </body>
    content = content.replace('</body>', modal_code + '\n</body>')
    with open(portfolio_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 3. Modify index.html to use the modal for the cards
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        idx_content = f.read()

    # Find Kira, SBA, and Baulkline links in index.html and update them
    kira_videos = "[" + ",".join([f"'{v}'" for v in brands["Kira"]]) + "]"
    sba_videos = "[" + ",".join([f"'{v}'" for v in brands["Meena Bazaar"]]) + "]" # No SBA videos? Wait.
    # Wait, the user didn't rename any video to "SBA". SBA was just an example text in the old template.
    # Let's replace the index.html cards with the top 3 actual brands: Meena Bazaar, Luzo, Kira
    
    meena_videos = "[" + ",".join([f"'{v}'" for v in brands["Meena Bazaar"]]) + "]"
    luzo_videos = "[" + ",".join([f"'{v}'" for v in brands["Luzo"]]) + "]"
    
    idx_content = re.sub(
        r'<a href="project-kira.html" class="work-card reveal-heading">.*?</a>',
        f'<a href="#" class="work-card reveal-heading brand-card" data-brand="Kira" data-videos="{kira_videos}">\n          <div class="work-img"><div class="work-overlay">Play Reel</div></div>\n          <div class="work-info"><h4>Video Reel for Kira</h4><p>Content Production</p></div>\n        </a>',
        idx_content, flags=re.DOTALL
    )
    
    idx_content = re.sub(
        r'<a href="project-sba.html" class="work-card reveal-heading">.*?</a>',
        f'<a href="#" class="work-card reveal-heading brand-card" data-brand="Meena Bazaar" data-videos="{meena_videos}">\n          <div class="work-img"><div class="work-overlay">View Campaign</div></div>\n          <div class="work-info"><h4>Meena Bazaar</h4><p>Growth & Paid Media</p></div>\n        </a>',
        idx_content, flags=re.DOTALL
    )
    
    baulkline_videos = "[" + ",".join([f"'{v}'" for v in brands["Baulkline"]]) + "]"
    idx_content = re.sub(
        r'<a href="project-baulkline.html" class="work-card reveal-heading">.*?</a>',
        f'<a href="#" class="work-card reveal-heading brand-card" data-brand="Baulkline" data-videos="{baulkline_videos}">\n          <div class="work-img"><div class="work-overlay">View Project</div></div>\n          <div class="work-info"><h4>Brand Identity for Baulkline</h4><p>Branding</p></div>\n        </a>',
        idx_content, flags=re.DOTALL
    )

    if 'id="videoModal"' not in idx_content:
        idx_content = idx_content.replace('</body>', modal_code + '\n</body>')

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

    print("Modal successfully injected into portfolio.html and index.html")

if __name__ == "__main__":
    build_modals()
