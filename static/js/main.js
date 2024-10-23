document.addEventListener('DOMContentLoaded', function() {
    // Touch-friendly scrolling for property cards
    const propertyContainer = document.querySelector('.property-container');
    if (propertyContainer) {
        let isDown = false;
        let startX;
        let scrollLeft;
        let touchStartX;

        // Mouse events
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

        // Touch events
        propertyContainer.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].pageX - propertyContainer.offsetLeft;
            scrollLeft = propertyContainer.scrollLeft;
        });

        propertyContainer.addEventListener('touchmove', (e) => {
            if (!touchStartX) return;
            e.preventDefault();
            const x = e.touches[0].pageX - propertyContainer.offsetLeft;
            const walk = (x - touchStartX) * 2;
            propertyContainer.scrollLeft = scrollLeft - walk;
        });

        propertyContainer.addEventListener('touchend', () => {
            touchStartX = null;
        });
    }

    // Add event listeners for property card clicks and touches
    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => {
        const handleCardInteraction = function(e) {
            if (!e.target.closest('a')) {
                const propertyId = this.dataset.propertyId;
                window.location.href = `/price_selection/${propertyId}`;
            }
        };

        card.addEventListener('click', handleCardInteraction);
        card.addEventListener('touchend', (e) => {
            e.preventDefault();
            handleCardInteraction.call(card, e);
        });
    });

    // Add event listeners for price option card clicks and touches
    const priceOptionCards = document.querySelectorAll('.price-option-card');
    priceOptionCards.forEach(card => {
        const handleOptionInteraction = function(e) {
            if (!e.target.closest('a')) {
                const propertyId = this.dataset.propertyId;
                const priceOptionId = this.dataset.priceOptionId;
                window.location.href = `/discount_selection/${propertyId}/${priceOptionId}`;
            }
        };

        card.addEventListener('click', handleOptionInteraction);
        card.addEventListener('touchend', (e) => {
            e.preventDefault();
            handleOptionInteraction.call(card, e);
        });
    });

    // Add tap highlight animation
    const addTapHighlight = (elements) => {
        elements.forEach(element => {
            element.addEventListener('touchstart', () => {
                element.style.opacity = '0.7';
            });

            element.addEventListener('touchend', () => {
                element.style.opacity = '1';
            });

            element.addEventListener('touchcancel', () => {
                element.style.opacity = '1';
            });
        });
    };

    // Apply tap highlight to interactive elements
    addTapHighlight(propertyCards);
    addTapHighlight(priceOptionCards);
    addTapHighlight(document.querySelectorAll('.btn'));
});
