document.addEventListener('DOMContentLoaded', function() {
    // Touch-friendly scrolling for property cards
    const propertyContainer = document.querySelector('.property-container');
    if (propertyContainer) {
        let isDown = false;
        let startX;
        let scrollLeft;
        let touchStartX;
        let touchStartY;
        let touchStartTime;
        let touchMoveDistance = 0;
        const CLICK_THRESHOLD = 10; // pixels
        const SWIPE_THRESHOLD = 50; // pixels

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
            const walk = (x - startX) * 2;
            propertyContainer.scrollLeft = scrollLeft - walk;
        });

        // Touch events with improved handling
        propertyContainer.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].pageX;
            touchStartY = e.touches[0].pageY;
            touchStartTime = Date.now();
            touchMoveDistance = 0;
            scrollLeft = propertyContainer.scrollLeft;
        });

        propertyContainer.addEventListener('touchmove', (e) => {
            if (!touchStartX) return;
            
            const currentX = e.touches[0].pageX;
            const currentY = e.touches[0].pageY;
            const deltaX = touchStartX - currentX;
            const deltaY = touchStartY - currentY;
            
            // Calculate total movement distance
            touchMoveDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            // Only prevent default if the movement is more horizontal than vertical
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                e.preventDefault();
                propertyContainer.scrollLeft = scrollLeft + deltaX;
            }
        });

        propertyContainer.addEventListener('touchend', () => {
            touchStartX = null;
            touchStartY = null;
        });
    }

    // Add event listeners for property card clicks and touches
    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => {
        let touchStartX;
        let touchStartY;
        let moveDistance = 0;

        const handleCardInteraction = function(e) {
            if (!e.target.closest('a') && moveDistance < CLICK_THRESHOLD) {
                const propertyId = this.dataset.propertyId;
                window.location.href = `/price_selection/${propertyId}`;
            }
        };

        card.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].pageX;
            touchStartY = e.touches[0].pageY;
            moveDistance = 0;
        });

        card.addEventListener('touchmove', (e) => {
            if (!touchStartX) return;
            
            const deltaX = touchStartX - e.touches[0].pageX;
            const deltaY = touchStartY - e.touches[0].pageY;
            moveDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        });

        card.addEventListener('click', handleCardInteraction);
        card.addEventListener('touchend', (e) => {
            if (moveDistance < CLICK_THRESHOLD) {
                handleCardInteraction.call(card, e);
            }
            touchStartX = null;
            touchStartY = null;
        });
    });

    // Add event listeners for price option card clicks and touches
    const priceOptionCards = document.querySelectorAll('.price-option-card');
    priceOptionCards.forEach(card => {
        let touchStartX;
        let touchStartY;
        let moveDistance = 0;

        const handleOptionInteraction = function(e) {
            if (!e.target.closest('a') && moveDistance < CLICK_THRESHOLD) {
                const propertyId = this.dataset.propertyId;
                const priceOptionId = this.dataset.priceOptionId;
                window.location.href = `/discount_selection/${propertyId}/${priceOptionId}`;
            }
        };

        card.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].pageX;
            touchStartY = e.touches[0].pageY;
            moveDistance = 0;
        });

        card.addEventListener('touchmove', (e) => {
            if (!touchStartX) return;
            
            const deltaX = touchStartX - e.touches[0].pageX;
            const deltaY = touchStartY - e.touches[0].pageY;
            moveDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        });

        card.addEventListener('click', handleOptionInteraction);
        card.addEventListener('touchend', (e) => {
            if (moveDistance < CLICK_THRESHOLD) {
                handleOptionInteraction.call(card, e);
            }
            touchStartX = null;
            touchStartY = null;
        });
    });

    // Add tap highlight animation with improved touch handling
    const addTapHighlight = (elements) => {
        elements.forEach(element => {
            let touchStartX;
            let touchStartY;
            let moveDistance = 0;

            element.addEventListener('touchstart', (e) => {
                touchStartX = e.touches[0].pageX;
                touchStartY = e.touches[0].pageY;
                moveDistance = 0;
                element.style.opacity = '0.7';
            });

            element.addEventListener('touchmove', (e) => {
                if (!touchStartX) return;
                const deltaX = touchStartX - e.touches[0].pageX;
                const deltaY = touchStartY - e.touches[0].pageY;
                moveDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
                
                if (moveDistance > CLICK_THRESHOLD) {
                    element.style.opacity = '1';
                }
            });

            element.addEventListener('touchend', () => {
                element.style.opacity = '1';
                touchStartX = null;
                touchStartY = null;
            });

            element.addEventListener('touchcancel', () => {
                element.style.opacity = '1';
                touchStartX = null;
                touchStartY = null;
            });
        });
    };

    // Apply tap highlight to interactive elements
    addTapHighlight(propertyCards);
    addTapHighlight(priceOptionCards);
    addTapHighlight(document.querySelectorAll('.btn'));
});
