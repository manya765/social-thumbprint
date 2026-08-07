def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    js_to_add = '''
        const testiPrevBtn = document.querySelector('.testi-prev');
        const testiNextBtn = document.querySelector('.testi-next');
        
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
        
        if (testiPrevBtn) {
            testiPrevBtn.addEventListener('click', () => { 
                slideCards(-1); 
                if(typeof autoScrollInterval !== 'undefined') clearInterval(autoScrollInterval); 
            });
        }
        if (testiNextBtn) {
            testiNextBtn.addEventListener('click', () => { 
                slideCards(1); 
                if(typeof autoScrollInterval !== 'undefined') clearInterval(autoScrollInterval); 
            });
        }
'''

    if 'const testiPrevBtn = document.querySelector' not in content:
        content = content.replace(
            "setTimeout(updateActive, 500);",
            "setTimeout(updateActive, 500);\n" + js_to_add
        )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Arrow JS injected successfully.")

if __name__ == "__main__":
    main()
