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

    // Add event listeners for property card clicks
    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {
                const propertyId = this.dataset.propertyId;
                window.location.href = `/price_selection/${propertyId}`;
            }
        });
    });

    // Add event listeners for price option card clicks
    const priceOptionCards = document.querySelectorAll('.price-option-card');
    priceOptionCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {
                const propertyId = this.dataset.propertyId;
                const priceOptionId = this.dataset.priceOptionId;
                window.location.href = `/discount_selection/${propertyId}/${priceOptionId}`;
            }
        });
    });
});
