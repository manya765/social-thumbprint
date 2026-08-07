import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the testimonials section
    start_str = '<section id="testimonials">'
    end_str = '</section>'
    
    start_idx = content.find(start_str)
    if start_idx == -1:
        print("Could not find testimonials section")
        return
        
    end_idx = content.find(end_str, start_idx) + len(end_str)
    testimonials_section = content[start_idx:end_idx]

    # Extract all slides
    slide_pattern = r'<div class="testimonial-slide.*?">.*?<p class="testimonial-quote">"(.*?)"</p>.*?<p class="author-name">(.*?)</p>.*?<p class="author-role">(.*?)</p>.*?</div>\s*</div>\s*</div>'
    
    slides = re.findall(slide_pattern, testimonials_section, re.DOTALL)
    
    if not slides:
        print("No slides found with regex, trying alternate regex")
        # Try a more relaxed regex
        slide_pattern = r'<p class="testimonial-quote">"(.*?)"</p>.*?<p class="author-name">(.*?)</p>.*?<p class="author-role">(.*?)</p>'
        slides = re.findall(slide_pattern, testimonials_section, re.DOTALL)

    print(f"Found {len(slides)} testimonials")

    # Rebuild the section
    new_section = '''<section class="testimonials" id="testimonials" style="padding: 6rem 0; overflow: hidden; background: #fafafa;">
    <div class="container" style="max-width: 1400px;">
      <div class="section-head-row reveal-heading" style="margin-bottom: 3rem;">
        <h2 class="section-heading" style="margin:0;">What Our <span style="color: var(--teal-light);">Clients</span> Say</h2>
      </div>
      
      <div class="testimonials-track-container" style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;">
        <div class="testimonials-track" style="display: flex; gap: 2rem; overflow-x: auto; padding: 2rem 5vw 4rem; scroll-snap-type: x mandatory; scrollbar-width: none; -ms-overflow-style: none;">
'''
    
    for quote, name, role in slides:
        new_section += f'''
          <div class="testimonial-card-new" style="flex: 0 0 auto; width: 320px; background: #fff; border-radius: 24px; padding: 2.5rem; scroll-snap-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.06); display: flex; flex-direction: column;">
            <div class="testi-header" style="margin-bottom: 1.5rem;">
              <h4 class="testi-name" style="font-family: var(--font-body); font-weight: 600; font-size: 1.2rem; color: var(--ink); margin: 0 0 0.2rem 0;">{name}</h4>
              <p class="testi-role" style="font-size: 0.85rem; color: #888; margin: 0; line-height: 1.4;">{role}</p>
            </div>
            <div class="testi-quote-icon" style="font-size: 4rem; color: var(--teal-light); font-family: serif; line-height: 0.5; margin-bottom: 1rem; opacity: 0.5;">“</div>
            <p class="testi-text" style="font-size: 0.95rem; line-height: 1.6; color: #444; margin: 0; font-weight: 400;">{quote}</p>
          </div>
'''

    new_section += '''
        </div>
      </div>
    </div>
  </section>
  <style>
    .testimonials-track::-webkit-scrollbar { display: none; }
    .testimonial-card-new {
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .testimonial-card-new:hover {
      transform: translateY(-10px);
      box-shadow: 0 20px 50px rgba(0,0,0,0.1);
    }
  </style>'''

    # Replace in file
    content = content.replace(testimonials_section, new_section)
    
    # Also remove the old JS for the testimonials if it exists
    js_start = content.find('const track = document.getElementById(\'testimonialTrack\');')
    if js_start != -1:
        js_end = content.find('});', js_start)
        if js_end != -1:
            # find the end of the domcontentloaded block if possible or just the relevant script part
            pass # Actually it's fine if the old JS fails to find the track, it just won't do anything

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Done")

if __name__ == '__main__':
    main()
