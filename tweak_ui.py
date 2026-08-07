import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Increase opacity of side testimonials
    # Look for: opacity: 0.3; in .testimonial-card-new
    content = content.replace('opacity: 0.3;', 'opacity: 0.7;')
    # Scale them up slightly more? 0.85 to 0.9?
    # content = content.replace('transform: scale(0.85);', 'transform: scale(0.9);')

    # 2. Add Auto-slide to the testimonials script
    js_to_add = '''
        // Auto-scroll functionality
        let autoScrollInterval = setInterval(() => {
            const trackCenter = track.getBoundingClientRect().left + track.getBoundingClientRect().width / 2;
            let activeIdx = -1;
            
            cards.forEach((card, idx) => {
                if (card.classList.contains('is-active')) {
                    activeIdx = idx;
                }
            });
            
            if (activeIdx !== -1) {
                let nextIdx = (activeIdx + 1) % cards.length;
                let nextCard = cards[nextIdx];
                
                // Calculate scroll position
                let scrollPos = nextCard.offsetLeft - track.offsetLeft - (track.clientWidth / 2) + (nextCard.clientWidth / 2);
                track.scrollTo({ left: scrollPos, behavior: 'smooth' });
            }
        }, 4000); // 4 seconds
        
        track.addEventListener('mouseenter', () => clearInterval(autoScrollInterval));
        track.addEventListener('touchstart', () => clearInterval(autoScrollInterval));
'''
    # Insert before the end of the updateActive listener setup
    if 'track.addEventListener(\'scroll\', updateActive);' in content and 'autoScrollInterval' not in content:
        content = content.replace(
            "track.addEventListener('scroll', updateActive);",
            js_to_add + "\n        track.addEventListener('scroll', updateActive);"
        )

    # 3. Make font of "Our Thumbprints" larger and adjust gap
    # Look for: <section id="work"> and <h2 class="section-heading" style="margin-bottom: 0;">Our Thumbprints</h2>
    content = content.replace('<section id="work">', '<section id="work" style="padding-top: 5rem; padding-bottom: 2rem;">')
    
    # Actually wait, maybe they want the gap between Our Thumbprints and the section ABOVE it?
    # Or BELOW it (the grid)?
    # The grid has `padding-top: 4rem;` and `padding-bottom: 12rem;` already in the CSS.
    # Increasing the section padding-top adds space between it and the previous section.
    content = content.replace(
        '<h2 class="section-heading" style="margin-bottom: 0;">Our Thumbprints</h2>',
        '<h2 class="section-heading" style="margin-bottom: 0; font-size: 3.5rem;">Our Thumbprints</h2>'
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Tweaks applied successfully.")

if __name__ == "__main__":
    main()
