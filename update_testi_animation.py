import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the testimonials section
    start_str = '<section class="testimonials" id="testimonials"'
    end_str = '</section>'
    
    start_idx = content.find(start_str)
    if start_idx == -1:
        print("Could not find testimonials section")
        return
        
    end_idx = content.find(end_str, start_idx) + len(end_str)
    testimonials_section = content[start_idx:end_idx]

    # Extract all slides
    # Since we previously rewrote them to testimonial-card-new, we must extract from there
    slide_pattern = r'<div class="testimonial-card-new".*?<h4 class="testi-name".*?>(.*?)</h4>.*?<p class="testi-role".*?>(.*?)</p>.*?<p class="testi-text".*?>(.*?)</p>.*?</div>'
    
    slides = re.findall(slide_pattern, testimonials_section, re.DOTALL)
    
    if not slides:
        print("No slides found in the new format. Aborting.")
        return

    print(f"Found {len(slides)} testimonials")

    # Rebuild the section WITHOUT the white background
    new_section = '''<section id="testimonials" style="padding: 6rem 0; overflow: hidden; background: transparent;">
    <div class="container" style="max-width: 1400px;">
      <div class="section-head-row reveal-heading" style="margin-bottom: 3rem; text-align: center; display: flex; flex-direction: column; align-items: center;">
        <span class="eyebrow" style="margin-bottom: 0.5rem; letter-spacing: 2px; color: var(--teal-light);">What out customers say about us</span>
        <h2 class="section-heading" style="margin:0; font-size: 3rem;">Testimonials</h2>
      </div>
      
      <div class="testimonials-track-container" style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;">
        <div class="testimonials-track" style="display: flex; gap: 2rem; overflow-x: auto; padding: 4rem 5vw 6rem; scroll-snap-type: x mandatory; scrollbar-width: none; -ms-overflow-style: none; align-items: center;">
'''
    
    for name, role, quote in slides:
        new_section += f'''
          <div class="testimonial-card-new" style="flex: 0 0 auto; width: 340px; border-radius: 24px; padding: 2.5rem; scroll-snap-align: center; display: flex; flex-direction: column;">
            <div class="testi-header" style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem;">
              <div class="testi-avatar" style="width: 50px; height: 50px; border-radius: 50%; background: var(--teal); display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 1.2rem;">
                {name[0].upper() if name else 'C'}
              </div>
              <div>
                <h4 class="testi-name" style="font-family: var(--font-body); font-weight: 600; font-size: 1.2rem; margin: 0 0 0.2rem 0;">{name}</h4>
                <p class="testi-role" style="font-size: 0.85rem; margin: 0; line-height: 1.4;">{role}</p>
              </div>
            </div>
            <p class="testi-text" style="font-size: 0.95rem; line-height: 1.6; margin: 0; font-weight: 400; text-align: left;">"{quote}"</p>
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
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease, background 0.4s ease, box-shadow 0.4s ease;
      opacity: 0.3;
      transform: scale(0.85);
      background: transparent !important;
      box-shadow: none !important;
      color: rgba(255, 255, 255, 0.6);
    }
    .testimonial-card-new .testi-name {
      color: rgba(255, 255, 255, 0.8);
    }
    .testimonial-card-new .testi-role {
      color: rgba(255, 255, 255, 0.5);
    }
    
    /* The Center/Active Card */
    .testimonial-card-new.is-active {
      opacity: 1;
      transform: scale(1.05);
      background: #fff !important;
      box-shadow: 0 20px 50px rgba(0,0,0,0.15) !important;
      color: #555; /* Dark text for light bg */
    }
    .testimonial-card-new.is-active .testi-name {
      color: #111; /* Dark name */
    }
    .testimonial-card-new.is-active .testi-role {
      color: #888;
    }
  </style>
  <script>
    document.addEventListener('DOMContentLoaded', () => {
        const track = document.querySelector('.testimonials-track');
        const cards = document.querySelectorAll('.testimonial-card-new');
        if(!track || cards.length === 0) return;
        
        const updateActive = () => {
            const trackCenter = track.getBoundingClientRect().left + track.getBoundingClientRect().width / 2;
            let closest = cards[0];
            let minDiff = Infinity;
            
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const cardCenter = rect.left + rect.width / 2;
                const diff = Math.abs(trackCenter - cardCenter);
                if (diff < minDiff) {
                    minDiff = diff;
                    closest = card;
                }
            });
            
            cards.forEach(card => {
                if (card === closest) {
                    card.classList.add('is-active');
                } else {
                    card.classList.remove('is-active');
                }
            });
        };
        
        track.addEventListener('scroll', updateActive);
        updateActive();
        
        // Wait for images/fonts to load and layout to stabilize
        setTimeout(updateActive, 100);
        setTimeout(updateActive, 500);
    });
  </script>'''

    # We also need to remove any old `<style>` or `<script>` tags that were added by my previous script
    # to avoid duplication. The previous script added `<style>` at the end of the section block.
    # Let's just do a clean replace. The `end_idx` might not cover the style/script if they were outside the section.
    # In my previous script, I placed `<style>` AFTER `</section>`.
    # So I need to find `</style>` if it immediately follows `</section>`.
    
    match = re.search(r'</section>\s*<style>.*?</style>', content, re.DOTALL)
    if match and match.start() == end_idx - 10: # approx check
        end_idx = match.end()
        testimonials_section = content[start_idx:end_idx]

    content = content.replace(testimonials_section, new_section)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Done")

if __name__ == '__main__':
    main()
