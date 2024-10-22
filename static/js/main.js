document.addEventListener('DOMContentLoaded', function() {
    // Touch-friendly scrolling for property cards
    const propertyContainer = document.querySelector('.property-container');
    if (propertyContainer) {
        let isDown = false;
        let startX;
        let scrollLeft;

        propertyContainer.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - propertyContainer.offsetLeft;
            scrollLeft = propertyContainer.scrollLeft;
        });

        propertyContainer.addEventListener('mouseleave', () => {
            isDown = false;
        });

        propertyContainer.addEventListener('mouseup', () => {
            isDown = false;
        });

        propertyContainer.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - propertyContainer.offsetLeft;
            const walk = (x - startX) * 3;
            propertyContainer.scrollLeft = scrollLeft - walk;
        });
    }
});
