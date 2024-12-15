document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
        header.classList.toggle('active');
        const content = header.nextElementSibling;

        // open section
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
            content.style.opacity = 0;
            content.style.paddingTop = null;
            content.style.paddingBottom = null;

        // close section
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
            content.style.opacity = 1;
            content.style.paddingTop = "1rem";
            content.style.paddingBottom = "1rem";
        }
    });
});