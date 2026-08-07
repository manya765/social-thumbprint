import os
import glob
import re

def build_cuberto():
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
        for brand in brands.keys():
            search_brand = "cappacino" if brand == "The Cappacino Collection" else brand.lower()
            if search_brand in lower_name:
                brands[brand].append(basename)
                break
            
    for brand in brands:
        brands[brand].sort()

    # Create Cuberto CSS
    cuberto_css = """
  <!-- CUBERTO STYLES -->
  <style>
    /* Remove card background and shadow, make transparent */
    .work-card {
        background: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
    }
    .work-grid {
        gap: 4rem 2.5rem !important;
    }

    /* The media container */
    .work-img {
        border-radius: 20px !important; 
        overflow: hidden !important;
        transform: translateZ(0); /* Force GPU */
        position: relative;
        padding-bottom: 110% !important; /* Cuberto tall portrait format */
        background: #111 !important;
    }

    /* The video scales on hover */
    .work-img video {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover;
        transform: scale(1);
        transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .work-card:hover .work-img video {
        transform: scale(1.08); /* Smooth scale */
    }

    /* Hide the old white "View Project" overlay badge */
    .work-overlay {
        display: none !important;
    }

    /* Elegant Typography Outside */
    .work-info {
        padding: 1.5rem 0.5rem 0 0.2rem !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-direction: row !important;
    }
    .work-info h4 {
        font-size: 1.6rem !important;
        color: var(--white) !important;
        font-family: var(--font-body) !important;
        font-weight: 500 !important;
        letter-spacing: -0.02em !important;
        margin: 0 !important;
        transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .work-info p {
        font-size: 1rem !important;
        color: var(--ink-faint) !important;
        font-weight: 400 !important;
        margin: 0 !important;
    }
    .work-card:hover .work-info h4 {
        transform: translateX(10px); /* subtle slide */
        color: var(--teal-light) !important;
    }

    /* Custom Cursor Morphing to "VIEW" */
    .cursor-fingerprint {
        transition: transform 0.3s ease, width 0.3s ease, height 0.3s ease, background 0.3s ease, border-radius 0.3s ease;
    }
    .cursor-fingerprint.view-mode {
        width: 90px; height: 90px;
        transform: translate(-50%, -50%) !important;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        opacity: 1 !important;
    }
    .cursor-fingerprint.view-mode svg {
        display: none; /* Hide fingerprint */
    }
    .cursor-fingerprint.view-mode::after {
        content: 'VIEW';
        color: var(--white);
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 1px;
    }
  </style>
  <script>
    // Cuberto Cursor Logic
    window.addEventListener('DOMContentLoaded', () => {
        const cursor = document.getElementById('customCursor');
        if(!cursor) return;
        
        // Use event delegation for dynamically injected cards
        document.body.addEventListener('mouseenter', (e) => {
            const card = e.target.closest('.brand-card');
            if (card) {
                cursor.classList.add('view-mode');
            }
        }, True); // Use capture phase if needed, or just hover directly
        
        // Actually, let's just query and attach directly for simplicity since cards are mostly static after load
        setTimeout(() => {
            document.querySelectorAll('.brand-card').forEach(card => {
                card.addEventListener('mouseenter', () => cursor.classList.add('view-mode'));
                card.addEventListener('mouseleave', () => cursor.classList.remove('view-mode'));
            });
        }, 1000);
    });
  </script>
"""

    def generate_card_html(brand, videos):
        if not videos: return ""
        videos_json = "[" + ",".join([f"'{v}'" for v in videos]) + "]"
        first_video = videos[0]
        count_text = f"{len(videos)} Video" if len(videos) == 1 else f"{len(videos)} Videos"
        
        return f"""
        <div class="work-card reveal-heading in-view brand-card" data-brand="{brand}" data-videos="{videos_json}" style="cursor: pointer;">
          <div class="work-img">
             <video src="videos/{first_video}" muted loop playsinline onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="work-info">
            <h4>{brand}</h4>
            <p>{count_text}</p>
          </div>
        </div>
"""

    # 1. Update portfolio.html
    portfolio_path = os.path.join(base_dir, "portfolio.html")
    with open(portfolio_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate all cards
    all_cards = ""
    for brand, videos in brands.items():
        all_cards += generate_card_html(brand, videos)

    # Replace grid
    pattern = r'(<div class="work-grid" style="grid-template-columns: repeat\(auto-fit, minmax\(320px, 1fr\)\); gap: 2rem;">).*?(</section>)'
    new_grid = f'\\1\n{all_cards}\n      </div>\n    </div>\n  \\2'
    content = re.sub(pattern, new_grid, content, flags=re.DOTALL)
    
    if '<!-- CUBERTO STYLES -->' not in content:
        content = content.replace('</head>', cuberto_css + '\n</head>')

    with open(portfolio_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Update index.html
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        idx_content = f.read()

    # Replace just the first 3 featured brands
    featured_brands = ["Meena Bazaar", "Luzo", "Kira"]
    featured_cards = ""
    for b in featured_brands:
        featured_cards += generate_card_html(b, brands[b])

    idx_pattern = r'(<div class="work-grid">).*?(</div>\s*</div>\s*</section>)'
    
    # Check if we already injected it previously
    if 'data-brand="Meena Bazaar"' in idx_content:
        # We need a robust regex to replace everything inside .work-grid
        idx_pattern = r'(<div class="work-grid">).*?(</section>)'
        idx_new_grid = f'\\1\n{featured_cards}\n      </div>\n    </div>\n  \\2'
        idx_content = re.sub(idx_pattern, idx_new_grid, idx_content, flags=re.DOTALL)
    else:
        # Original replacement
        idx_new_grid = f'\\1\n{featured_cards}\n      </div>\n    </div>\n  </section>'
        idx_content = re.sub(r'(<div class="work-grid">).*?(</section>)', idx_new_grid, idx_content, flags=re.DOTALL)

    if '<!-- CUBERTO STYLES -->' not in idx_content:
        idx_content = idx_content.replace('</head>', cuberto_css + '\n</head>')

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

    print("Cuberto design successfully applied to cards.")

if __name__ == "__main__":
    build_cuberto()
