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
        const CLICK_THRESHOLD = 15; // Increased threshold for better distinction
        const TAP_DELAY = 300; // Maximum time in ms for a tap

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
            
            touchMoveDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            // Allow natural scrolling
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
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
        let touchStartTime;
        let moveDistance = 0;
        let tapTimeout;

        const handleCardInteraction = function(e, isTouchEvent = false) {
            if (!e.target.closest('a')) {
                const propertyId = this.dataset.propertyId;
                if (!isTouchEvent || (moveDistance < CLICK_THRESHOLD && Date.now() - touchStartTime < TAP_DELAY)) {
                    window.location.href = `/price_selection/${propertyId}`;
                }
            }
        };

        card.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].pageX;
            touchStartY = e.touches[0].pageY;
            touchStartTime = Date.now();
            moveDistance = 0;
            
            // Clear any existing tap timeout
            if (tapTimeout) {
                clearTimeout(tapTimeout);
            }
        });

        card.addEventListener('touchmove', (e) => {
            if (!touchStartX) return;
            
            const deltaX = touchStartX - e.touches[0].pageX;
            const deltaY = touchStartY - e.touches[0].pageY;
            moveDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        });

        card.addEventListener('click', function(e) {
            handleCardInteraction.call(this, e, false);
        });

        card.addEventListener('touchend', function(e) {
            // Add a small delay to ensure we don't trigger during scroll
            tapTimeout = setTimeout(() => {
                if (moveDistance < CLICK_THRESHOLD && Date.now() - touchStartTime < TAP_DELAY) {
                    handleCardInteraction.call(this, e, true);
                }
            }, 50);
            
            touchStartX = null;
            touchStartY = null;
        });
    });

    // Add event listeners for price option card clicks and touches
    const priceOptionCards = document.querySelectorAll('.price-option-card');
    priceOptionCards.forEach(card => {
        let touchStartX;
        let touchStartY;
        let touchStartTime;
        let moveDistance = 0;
        let tapTimeout;

        const handleOptionInteraction = function(e, isTouchEvent = false) {
            if (!e.target.closest('a')) {
                const propertyId = this.dataset.propertyId;
                const priceOptionId = this.dataset.priceOptionId;
                if (!isTouchEvent || (moveDistance < CLICK_THRESHOLD && Date.now() - touchStartTime < TAP_DELAY)) {
                    window.location.href = `/discount_selection/${propertyId}/${priceOptionId}`;
                }
            }
        };

        card.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].pageX;
            touchStartY = e.touches[0].pageY;
            touchStartTime = Date.now();
            moveDistance = 0;

            if (tapTimeout) {
                clearTimeout(tapTimeout);
            }
        });

        card.addEventListener('touchmove', (e) => {
            if (!touchStartX) return;
            
            const deltaX = touchStartX - e.touches[0].pageX;
            const deltaY = touchStartY - e.touches[0].pageY;
            moveDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        });

        card.addEventListener('click', function(e) {
            handleOptionInteraction.call(this, e, false);
        });

        card.addEventListener('touchend', function(e) {
            tapTimeout = setTimeout(() => {
                if (moveDistance < CLICK_THRESHOLD && Date.now() - touchStartTime < TAP_DELAY) {
                    handleOptionInteraction.call(this, e, true);
                }
            }, 50);
            
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
            let touchStartTime;

            element.addEventListener('touchstart', (e) => {
                touchStartX = e.touches[0].pageX;
                touchStartY = e.touches[0].pageY;
                touchStartTime = Date.now();
                moveDistance = 0;
                
                if (moveDistance < CLICK_THRESHOLD) {
                    element.style.opacity = '0.7';
                }
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
