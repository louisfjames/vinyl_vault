// Increment quantity
document.querySelectorAll('.increment-qty').forEach((button) => {
    button.addEventListener('click', (e) => {
        const itemId = e.target.dataset.item_id;
        const input = document.getElementById(`id_qty_${itemId}`);
        const currentValue = parseInt(input.value);
        const maxValue = parseInt(input.max);

        if (currentValue < maxValue) {
            input.value = currentValue + 1;
        }
    });
});

// Decrement quantity
document.querySelectorAll('.decrement-qty').forEach((button) => {
    button.addEventListener('click', (e) => {
        const itemId = e.target.dataset.item_id;
        const input = document.getElementById(`id_qty_${itemId}`);
        const currentValue = parseInt(input.value);
        const minValue = parseInt(input.min);

        if (currentValue > minValue) {
            input.value = currentValue - 1;
        }
    });
});