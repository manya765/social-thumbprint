import os
import re

def fix_css():
    base_dir = r"d:\social thumbrint"
    
    cuberto_css_clean = """
  /* CUBERTO STAGGERED STYLES */
  .work-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8rem 4rem;
      align-items: start;
      max-width: 1400px;
      margin: 0 auto;
      padding-top: 4rem;
  }
  
  .work-card {
      background: transparent;
      box-shadow: none;
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      border-radius: 0;
      padding: 0;
      overflow: visible;
      display: block;
      text-decoration: none;
      opacity: 0; 
      transform: translateY(40px);
      transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .work-card.in-view {
      opacity: 1;
      transform: translateY(0);
  }
  
  @media (min-width: 992px) {
      .work-card:nth-child(even) {
          margin-top: 15rem; /* Massive stagger */
      }
  }
  @media (max-width: 991px) {
      .work-grid {
          grid-template-columns: 1fr;
          gap: 6rem;
      }
      .work-card:nth-child(even) {
          margin-top: 0;
      }
  }

  .work-img {
      border-radius: 20px;
      overflow: hidden;
      transform: translateZ(0); 
      position: relative;
      width: 100%;
      aspect-ratio: 4/5; /* Modern aspect ratio, no height hack needed */
      background: #111;
      margin-bottom: 2rem;
  }

  .work-img video {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      object-fit: cover;
      transform: scale(1);
      transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .work-card:hover .work-img video {
      transform: scale(1.08); /* Smooth scale */
  }

  .work-overlay { display: none; }

  .work-info {
      padding: 0 1rem;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: flex-start;
  }
  
  .work-info h4 {
      font-size: 2rem;
      color: var(--white);
      font-family: var(--font-body);
      font-weight: 500;
      letter-spacing: -0.02em;
      margin: 0 0 1rem 0;
      line-height: 1.2;
  }
  
  .work-info p {
      font-size: 1.1rem;
      color: rgba(255, 255, 255, 0.7);
      font-weight: 400;
      margin: 0;
      line-height: 1.6;
      max-width: 90%;
  }

  .cursor-fingerprint {
      transition: transform 0.3s ease, width 0.3s ease, height 0.3s ease, background 0.3s ease, border-radius 0.3s ease;
  }
  .cursor-fingerprint.view-mode {
      width: 120px; height: 120px;
      transform: translate(-50%, -50%);
      background: rgba(0, 176, 185, 0.9);
      border: none;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      opacity: 1;
  }
  .cursor-fingerprint.view-mode svg { display: none; }
  .cursor-fingerprint.view-mode::after {
      content: 'PLAY';
      color: var(--white);
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 2px;
  }
"""

    def process_file(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove the old work-card CSS from the middle of the style block
        # We find the section `/* Work Grid (Our Thumbprints) */` up to `/* Founder Section */`
        # and delete it.
        content = re.sub(r'/\* Work Grid \(Our Thumbprints\) \*/.*?(?=/\* Founder Section \*/)', '', content, flags=re.DOTALL)
        
        # Remove any previously appended CUBERTO STYLES blocks at the end
        content = re.sub(r'<!-- CUBERTO STAGGERED STYLES -->.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- CUBERTO STYLES -->.*?</script>', '', content, flags=re.DOTALL)
        
        # We need to insert our clean CSS. We will just append it before </style> or in a new block.
        # It's safer to just put it in a new block in the head.
        clean_block = f"""
  <style id="cuberto-styles">
{cuberto_css_clean}
  </style>
  <script id="cuberto-scripts">
    window.addEventListener('DOMContentLoaded', () => {{
        const cursor = document.getElementById('customCursor');
        if(!cursor) return;
        
        setTimeout(() => {{
            document.querySelectorAll('.brand-card').forEach(card => {{
                card.addEventListener('mouseenter', () => cursor.classList.add('view-mode'));
                card.addEventListener('mouseleave', () => cursor.classList.remove('view-mode'));
            }});
        }}, 1000);
    }});
  </script>
</head>"""
        content = content.replace('</head>', clean_block)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    process_file(os.path.join(base_dir, "portfolio.html"))
    process_file(os.path.join(base_dir, "index.html"))

    print("CSS successfully cleaned and rewritten for Cuberto style.")

if __name__ == "__main__":
    fix_css()
