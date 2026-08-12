import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix work-grid margin
work_grid_target = '''    .work-grid {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: nowrap;
      gap: 0;
      padding: 4rem 2vw 8rem;
      max-width: 1200px;
      margin: 16rem auto 0;
      overflow: visible;
    }'''

work_grid_replace = '''    .work-grid {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: nowrap;
      gap: 0;
      padding: 4rem 2vw 8rem;
      max-width: 1200px;
      margin: 2rem auto 0;
      overflow: visible;
    }'''
content = content.replace(work_grid_target, work_grid_replace)

# 2. Add service descriptions
services_target = '''      <div class="services-list">
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">BRANDING</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">CONTENT WRITING</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">SOCIAL MEDIA ADS</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">GRAPHIC DESIGNING</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">CONTENT CREATION & CURATION</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">CAMPAIGN CONCEPTS & STRATEGIES</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">START TO END SOCIAL MEDIA MANAGEMENT</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">LIVE EVENT CONTENT COVERAGE</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">WEDDING SOCIAL MEDIA COVERAGE</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">BESPOKE INVITATION DESIGN</div>
          </div>
        </a>
      </div>'''

services_replace = '''      <div class="services-list">
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">BRANDING</div>
            <div class="service-list-desc">Shaping your identity and leaving a lasting impression.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">CONTENT WRITING</div>
            <div class="service-list-desc">Crafting compelling stories that engage your audience.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">SOCIAL MEDIA ADS</div>
            <div class="service-list-desc">Targeted campaigns that drive conversions and growth.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">GRAPHIC DESIGNING</div>
            <div class="service-list-desc">Visually stunning designs that speak volumes.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">CONTENT CREATION & CURATION</div>
            <div class="service-list-desc">Delivering high-quality content that resonates.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">CAMPAIGN CONCEPTS & STRATEGIES</div>
            <div class="service-list-desc">Strategic planning for maximum impact.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">START TO END SOCIAL MEDIA MANAGEMENT</div>
            <div class="service-list-desc">Full-service management for your online presence.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">LIVE EVENT CONTENT COVERAGE</div>
            <div class="service-list-desc">Capturing the magic of your events in real-time.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">WEDDING SOCIAL MEDIA COVERAGE</div>
            <div class="service-list-desc">Preserving your special moments beautifully.</div>
          </div>
        </a>
        <a href="#contact" class="service-list-item reveal-heading">
          <div class="service-list-content">
            <div class="service-list-title">BESPOKE INVITATION DESIGN</div>
            <div class="service-list-desc">Custom invitations tailored to your unique style.</div>
          </div>
        </a>
      </div>'''
content = content.replace(services_target, services_replace)

# 3. Fix service-list-desc text color to white
content = re.sub(r'color:\s*var\(--teal-light\);', 'color: #ffffff;', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Restored good changes without touching hexes!")
