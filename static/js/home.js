document.addEventListener("DOMContentLoaded", () => {
    setupHeroSlideshow();
});

function setupHeroSlideshow() {
    const heroSlideshow = document.querySelector(".hero-slideshow");
    const heroSlides = Array.from(document.querySelectorAll(".hero-slide"));
    const heroDots = document.querySelector(".hero-dots");

    if (!heroSlideshow || heroSlides.length === 0 || !heroDots) {
        return;
    }

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let activeSlide = 0;
    let slideshowTimer;

    heroDots.innerHTML = heroSlides.map((_, index) => (
        `<button class="hero-dot" type="button" aria-label="Show photo ${index + 1}" aria-current="false"></button>`
    )).join("");

    const dots = Array.from(heroDots.querySelectorAll(".hero-dot"));

    function showHeroSlide(index) {
        activeSlide = (index + heroSlides.length) % heroSlides.length;

        heroSlides.forEach((slide, slideIndex) => {
            const isActive = slideIndex === activeSlide;

            slide.classList.toggle("active", isActive);
            slide.setAttribute("aria-hidden", String(!isActive));
        });

        dots.forEach((dot, dotIndex) => {
            const isActive = dotIndex === activeSlide;

            dot.classList.toggle("active", isActive);
            dot.setAttribute("aria-current", String(isActive));
        });
    }

    function startHeroSlideshow() {
        if (reduceMotion) {
            return;
        }

        window.clearInterval(slideshowTimer);
        slideshowTimer = window.setInterval(() => {
            showHeroSlide(activeSlide + 1);
        }, 5000);
    }

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            showHeroSlide(index);
            startHeroSlideshow();
        });
    });

    heroSlideshow.addEventListener("mouseenter", () => window.clearInterval(slideshowTimer));
    heroSlideshow.addEventListener("mouseleave", startHeroSlideshow);

    showHeroSlide(0);
    startHeroSlideshow();
}
