document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.querySelector(".nav-toggle");
    const navLinks = document.querySelector(".nav-links");
    const siteHeader = document.querySelector(".site-header");
    const backToTop = document.querySelector(".back-to-top");
    const lightbox = document.querySelector(".lightbox");
    const lightboxImage = document.querySelector(".lightbox-image");
    const lightboxCaption = document.querySelector(".lightbox-caption");
    const lightboxClose = document.querySelector(".lightbox-close");
    const headerScrollOffset = 60;

    function closeNav() {
        if (!navToggle || !navLinks) {
            return;
        }

        navToggle.classList.remove("is-open");
        navLinks.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
    }

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            const isOpen = navLinks.classList.toggle("is-open");
            navToggle.classList.toggle("is-open", isOpen);
            navToggle.setAttribute("aria-expanded", String(isOpen));
            document.body.classList.toggle("nav-open", isOpen);
        });

        navLinks.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", closeNav);
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach((link) => {
        link.addEventListener("click", (event) => {
            const targetId = link.getAttribute("href");
            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);
            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });

    function updateHeaderState() {
        if (!siteHeader) {
            return;
        }

        siteHeader.classList.toggle("is-scrolled", window.scrollY > headerScrollOffset);
    }

    function updateScrollState() {
        updateHeaderState();

        if (backToTop) {
            backToTop.classList.toggle("is-visible", window.scrollY > 420);
        }
    }

    if (siteHeader || backToTop) {
        updateScrollState();
        window.addEventListener("scroll", updateScrollState, { passive: true });
    }

    if (backToTop) {
        backToTop.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    function closeLightbox() {
        if (!lightbox) {
            return;
        }

        lightbox.classList.remove("is-open");
        lightbox.setAttribute("aria-hidden", "true");
        document.body.classList.remove("lightbox-open");

        if (lightboxImage) {
            lightboxImage.src = "";
            lightboxImage.alt = "";
        }
    }

    document.querySelectorAll(".lightbox-trigger").forEach((trigger) => {
        trigger.addEventListener("click", () => {
            if (!lightbox || !lightboxImage) {
                return;
            }

            const imageSrc = trigger.dataset.full;
            const caption = trigger.dataset.caption || trigger.querySelector("span")?.textContent || "Gallery image";
            const altText = trigger.querySelector("img")?.alt || caption;

            lightboxImage.src = imageSrc;
            lightboxImage.alt = altText;

            if (lightboxCaption) {
                lightboxCaption.textContent = caption;
            }

            lightbox.classList.add("is-open");
            lightbox.setAttribute("aria-hidden", "false");
            document.body.classList.add("lightbox-open");
            lightboxClose?.focus();
        });
    });

    lightboxClose?.addEventListener("click", closeLightbox);

    lightbox?.addEventListener("click", (event) => {
        if (event.target === lightbox) {
            closeLightbox();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeLightbox();
            closeNav();
        }
    });

});
