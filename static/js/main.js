document.addEventListener('DOMContentLoaded', function() {
    // Property selection
    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => {
        card.addEventListener('click', function() {
            const propertyId = this.dataset.propertyId;
            window.location.href = `/price_selection/${propertyId}`;
        });
    });

    // Price option selection
    const priceOptionCards = document.querySelectorAll('.price-option-card');
    priceOptionCards.forEach(card => {
        card.addEventListener('click', function() {
            const propertyId = this.dataset.propertyId;
            const priceOptionId = this.dataset.priceOptionId;
            window.location.href = `/discount_selection/${propertyId}/${priceOptionId}`;
        });
    });

    // Discount method selection
    const discountForm = document.getElementById('discount-form');
    const discountMethodCards = document.querySelectorAll('.discount-method-card');
    discountMethodCards.forEach(card => {
        card.addEventListener('click', function() {
            discountMethodCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            document.getElementById('discount_method_id').value = this.dataset.discountMethodId;
        });
    });

    if (discountForm) {
        discountForm.addEventListener('submit', function(e) {
            if (!document.getElementById('discount_method_id').value) {
                e.preventDefault();
                alert('Please select a discount method');
            }
        });
    }

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
