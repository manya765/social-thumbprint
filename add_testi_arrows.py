import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add HTML for arrows inside the container
    arrows_html = '''
        <button class="testi-arrow testi-prev" aria-label="Previous">
          <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
        <button class="testi-arrow testi-next" aria-label="Next">
          <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
'''
    if 'testi-arrow' not in content:
        # insert right after <div class="testimonials-track-container"...>
        content = content.replace(
            '<div class="testimonials-track-container" style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;">',
            '<div class="testimonials-track-container" style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;">' + arrows_html
        )

    # 2. Add CSS for arrows
    arrows_css = '''
    .testi-arrow {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #fff;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: var(--teal);
        cursor: pointer;
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.3s, color 0.3s, transform 0.3s;
    }
    .testi-arrow:hover {
        background: var(--teal);
        color: #fff;
        transform: translateY(-50%) scale(1.1);
    }
    .testi-prev {
        left: max(2rem, calc(50vw - 650px));
    }
    .testi-next {
        right: max(2rem, calc(50vw - 650px));
    }
'''
    if '.testi-arrow {' not in content:
        content = content.replace(
            '</style>',
            arrows_css + '\n  </style>'
        )

    # 3. Add JS for arrows
    js_to_add = '''
        const prevBtn = document.querySelector('.testi-prev');
        const nextBtn = document.querySelector('.testi-next');
        
        const slideCards = (direction) => {
            let activeIdx = -1;
            cards.forEach((card, idx) => {
                if (card.classList.contains('is-active')) activeIdx = idx;
            });
            if (activeIdx !== -1) {
                let nextIdx = (activeIdx + direction + cards.length) % cards.length;
                let nextCard = cards[nextIdx];
                let scrollPos = nextCard.offsetLeft - track.offsetLeft - (track.clientWidth / 2) + (nextCard.clientWidth / 2);
                track.scrollTo({ left: scrollPos, behavior: 'smooth' });
            }
        };
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => { 
                slideCards(-1); 
                if(typeof autoScrollInterval !== 'undefined') clearInterval(autoScrollInterval); 
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', () => { 
                slideCards(1); 
                if(typeof autoScrollInterval !== 'undefined') clearInterval(autoScrollInterval); 
            });
        }
'''
    if 'prevBtn.addEventListener' not in content:
        content = content.replace(
            "setTimeout(updateActive, 500);",
            "setTimeout(updateActive, 500);\n" + js_to_add
        )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Arrows added successfully.")

if __name__ == "__main__":
    main()
