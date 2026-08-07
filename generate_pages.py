import os
import re

def create_pages():
    base_dir = r"d:\social thumbrint"
    index_path = os.path.join(base_dir, "index.html")
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Head + Navbar
    # We want everything from <!doctype html> up to the end of the <nav> element
    # The navbar ends right before the <!-- Hero --> section
    head_nav_match = re.search(r'(<!doctype html>.*?<!-- Hero -->)', content, re.DOTALL | re.IGNORECASE)
    if not head_nav_match:
        # fallback
        head_nav_match = re.search(r'(<!doctype html>.*?)(?:<section class="hero"|<!-- Hero -->)', content, re.DOTALL | re.IGNORECASE)
    
    head_nav = head_nav_match.group(1) if head_nav_match else ""

    # Extract Footer + Scripts
    # We want everything from <footer> to </html>
    footer_match = re.search(r'(<footer.*</html>)', content, re.DOTALL | re.IGNORECASE)
    footer_scripts = footer_match.group(1) if footer_match else ""

    # Template
    template = f"""{head_nav}
  {{body}}
{footer_scripts}
"""

    # 1. Project Kira
    kira_body = """
  <section class="hero" style="min-height: 60vh; padding-top: 10rem; padding-bottom: 3rem;">
    <div class="container hero-inner">
      <h1 class="hero-title load-stagger" style="font-size: clamp(2.5rem, 5vw, 4rem);">Video Reel for <span class="highlight-wrapper"><span class="highlight">Kira</span></span></h1>
      <p class="hero-intro load-stagger" style="max-width: 700px; margin-top: 1rem;">Content Production & Video Editing</p>
    </div>
  </section>

  <section class="project-details" style="padding: 4rem 0;">
    <div class="container">
      <div style="max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <!-- Video Player -->
        <div style="position: relative; padding-bottom: 56.25%; height: 0; background: #000;">
          <video controls style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;" poster="fingerprint.png">
            <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
      
      <div style="max-width: 800px; margin: 4rem auto 0; text-align: left;">
        <h3 style="color: var(--teal); margin-bottom: 1rem; font-size: 1.8rem;">The Challenge</h3>
        <p style="margin-bottom: 2rem; color: var(--ink-soft); line-height: 1.8;">Kira needed a dynamic video reel to showcase their content production capabilities and engage their audience on social media platforms. The goal was to create a fast-paced, visually stunning compilation that highlighted their best work.</p>
        
        <h3 style="color: var(--teal); margin-bottom: 1rem; font-size: 1.8rem;">Our Approach</h3>
        <p style="margin-bottom: 2rem; color: var(--ink-soft); line-height: 1.8;">We curated their top-performing video clips, synchronized them to an upbeat, modern soundtrack, and applied seamless transitions and color grading to ensure a cohesive and premium look.</p>
        
        <div style="display: flex; justify-content: space-between; margin-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem;">
            <a href="portfolio.html" class="btn btn-ghost">Back to Portfolio</a>
            <a href="project-sba.html" class="btn btn-primary">Next Project: SBA &rarr;</a>
        </div>
      </div>
    </div>
  </section>
"""

    with open(os.path.join(base_dir, "project-kira.html"), "w", encoding="utf-8") as f:
        f.write(template.replace("{body}", kira_body))

    # 2. Project SBA
    sba_body = """
  <section class="hero" style="min-height: 60vh; padding-top: 10rem; padding-bottom: 3rem;">
    <div class="container hero-inner">
      <h1 class="hero-title load-stagger" style="font-size: clamp(2.5rem, 5vw, 4rem);">Performance Campaign <br>for <span class="highlight-wrapper"><span class="highlight">SBA</span></span></h1>
      <p class="hero-intro load-stagger" style="max-width: 700px; margin-top: 1rem;">Growth & Paid Media</p>
    </div>
  </section>

  <section class="project-details" style="padding: 4rem 0;">
    <div class="container">
      <div style="max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); padding: 4rem; text-align: center;">
        <h2 style="font-size: 4rem; color: var(--teal-light); margin-bottom: 1rem;">+340%</h2>
        <p style="font-size: 1.2rem; color: var(--ink-soft); text-transform: uppercase; letter-spacing: 2px;">Increase in Lead Generation</p>
      </div>
      
      <div style="max-width: 800px; margin: 4rem auto 0; text-align: left;">
        <h3 style="color: var(--teal); margin-bottom: 1rem; font-size: 1.8rem;">The Strategy</h3>
        <p style="margin-bottom: 2rem; color: var(--ink-soft); line-height: 1.8;">For SBA, we designed a hyper-targeted performance marketing campaign across Meta and Google Ads. By A/B testing multiple ad creatives and optimizing landing pages, we significantly drove down the cost-per-acquisition (CPA).</p>
        
        <div style="display: flex; justify-content: space-between; margin-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem;">
            <a href="project-kira.html" class="btn btn-ghost">&larr; Previous: Kira</a>
            <a href="project-baulkline.html" class="btn btn-primary">Next Project: Baulkline &rarr;</a>
        </div>
      </div>
    </div>
  </section>
"""
    with open(os.path.join(base_dir, "project-sba.html"), "w", encoding="utf-8") as f:
        f.write(template.replace("{body}", sba_body))

    # 3. Project Baulkline
    baulkline_body = """
  <section class="hero" style="min-height: 60vh; padding-top: 10rem; padding-bottom: 3rem;">
    <div class="container hero-inner">
      <h1 class="hero-title load-stagger" style="font-size: clamp(2.5rem, 5vw, 4rem);">Brand Identity <br>for <span class="highlight-wrapper"><span class="highlight">Baulkline</span></span></h1>
      <p class="hero-intro load-stagger" style="max-width: 700px; margin-top: 1rem;">Branding & Visual Design</p>
    </div>
  </section>

  <section class="project-details" style="padding: 4rem 0;">
    <div class="container">
      <div style="max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); padding: 4rem; text-align: center; display: flex; justify-content: center; align-items: center; min-height: 400px;">
         <!-- Placeholder for brand imagery -->
         <div style="width: 150px; height: 150px; border-radius: 50%; border: 4px solid var(--teal); display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: bold; font-family: var(--font-heading); color: var(--white);">
            B.
         </div>
      </div>
      
      <div style="max-width: 800px; margin: 4rem auto 0; text-align: left;">
        <h3 style="color: var(--teal); margin-bottom: 1rem; font-size: 1.8rem;">The Vision</h3>
        <p style="margin-bottom: 2rem; color: var(--ink-soft); line-height: 1.8;">Baulkline needed a brand identity that reflected their modern, minimalist, yet bold approach to their industry. We crafted a comprehensive brand guidelines document, including logo variations, color palettes, and typography.</p>
        
        <div style="display: flex; justify-content: space-between; margin-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem;">
            <a href="project-sba.html" class="btn btn-ghost">&larr; Previous: SBA</a>
            <a href="portfolio.html" class="btn btn-primary">View All Work</a>
        </div>
      </div>
    </div>
  </section>
"""
    with open(os.path.join(base_dir, "project-baulkline.html"), "w", encoding="utf-8") as f:
        f.write(template.replace("{body}", baulkline_body))


    # 4. Portfolio Page
    portfolio_body = """
  <section class="hero" style="min-height: 50vh; padding-top: 10rem; padding-bottom: 3rem;">
    <div class="container hero-inner">
      <h1 class="hero-title load-stagger" style="font-size: clamp(3rem, 6vw, 4.5rem);">Our <span class="highlight-wrapper"><span class="highlight">Portfolio</span></span></h1>
      <p class="hero-intro load-stagger" style="max-width: 700px; margin-top: 1rem;">Explore our complete collection of digital experiences, campaigns, and creative content.</p>
    </div>
  </section>

  <section class="portfolio-gallery" style="padding: 2rem 0 6rem;">
    <div class="container">
      <div class="work-grid" style="grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem;">
        
        <a href="project-kira.html" class="work-card reveal-heading in-view">
          <div class="work-img">
            <div class="work-overlay">Play Reel</div>
          </div>
          <div class="work-info">
            <h4>Video Reel for Kira</h4>
            <p>Content Production</p>
          </div>
        </a>

        <a href="project-sba.html" class="work-card reveal-heading in-view">
          <div class="work-img">
            <div class="work-overlay">View Campaign</div>
          </div>
          <div class="work-info">
            <h4>Performance Campaign for SBA</h4>
            <p>Growth & Paid Media</p>
          </div>
        </a>

        <a href="project-baulkline.html" class="work-card reveal-heading in-view">
          <div class="work-img">
            <div class="work-overlay">View Project</div>
          </div>
          <div class="work-info">
            <h4>Brand Identity for Baulkline</h4>
            <p>Branding</p>
          </div>
        </a>

        <!-- Additional Placeholders -->
        <div class="work-card reveal-heading in-view">
          <div class="work-img" style="background: rgba(255,255,255,0.05);">
            <div class="work-overlay">Coming Soon</div>
          </div>
          <div class="work-info">
            <h4>Social Media for Kokolo</h4>
            <p>Community Management</p>
          </div>
        </div>

        <div class="work-card reveal-heading in-view">
          <div class="work-img" style="background: rgba(255,255,255,0.05);">
            <div class="work-overlay">Coming Soon</div>
          </div>
          <div class="work-info">
            <h4>Launch Campaign for Arctic Star</h4>
            <p>Strategy & Execution</p>
          </div>
        </div>

        <div class="work-card reveal-heading in-view">
          <div class="work-img" style="background: rgba(255,255,255,0.05);">
            <div class="work-overlay">Coming Soon</div>
          </div>
          <div class="work-info">
            <h4>Creative Direction for Adorne</h4>
            <p>Photography & Art Direction</p>
          </div>
        </div>
        
      </div>
    </div>
  </section>
"""
    with open(os.path.join(base_dir, "portfolio.html"), "w", encoding="utf-8") as f:
        f.write(template.replace("{body}", portfolio_body))

    print("Pages generated successfully.")

if __name__ == "__main__":
    create_pages()
