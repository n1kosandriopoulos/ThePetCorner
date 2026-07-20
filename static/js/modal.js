console.log("modal.js loaded");

const productCards = document.querySelectorAll(".product-card");

const modalOverlay = document.querySelector(".product-modal-overlay");

const modalImage = document.querySelector(".modal-product-image");
const modalName = document.querySelector(".modal-product-name");
const modalBrand = document.querySelector(".modal-product-brand");
const modalCategory = document.querySelector(".modal-product-category");
const modalPrice = document.querySelector(".modal-product-price");
const modalStock = document.querySelector(".modal-product-stock");
const modalDescription = document.querySelector(".modal-product-description");
const modalRating = document.querySelector(".modal-product-rating");
const modalStars = document.querySelector(".modal-product-stars");
const modalReviews = document.querySelector(".modal-product-reviews");
const modalReviewSection = document.querySelector(".modal-review-section"); 
const modalRelatedProducts = document.querySelector(".modal-related-products");
const quantityMinus = document.querySelector(".quantity-minus");
const quantityPlus = document.querySelector(".quantity-plus");
const quantityValue = document.querySelector(".quantity-value");
const addCartButton = document.querySelector(".add-cart-btn");

let currentQuantity = 1;
let maxStock = 0;
let currentProductId = null;

function updateQuantityButtons() {

    if (maxStock === 0) {

        quantityMinus.classList.add("disabled");

        quantityPlus.classList.add("disabled");

        return;

    }

    //Minus Button
    if (currentQuantity === 1) {

        quantityMinus.classList.add("disabled");

    }
    else {

        quantityMinus.classList.remove("disabled");

    }

    //Plus Button
    if (currentQuantity >= maxStock) {

        quantityPlus.classList.add("disabled");

    }
    else {

        quantityPlus.classList.remove("disabled");

    }

}

async function loadProduct(productId) {

    currentProductId = productId;

    const response = await fetch(`/products/${productId}/details/`);
    const product = await response.json();
    maxStock = product.stock;

    modalName.textContent = product.name;
    modalBrand.textContent = product.brand;
    modalCategory.textContent = product.category;
    modalPrice.textContent = "€" + product.price;
    if (product.stock === 0) {

        modalStock.textContent = "Out of Stock";

    }
    else if (product.stock <= 5) {

        modalStock.textContent = `Only ${product.stock} left in stock!`;

    }
    else {

        modalStock.textContent = `In Stock: ${product.stock}`;

    }

    if (product.stock === 0) {

        addCartButton.disabled = true;
        addCartButton.textContent = 'Out of Stock';

    }
    else {

        addCartButton.disabled = false;
        addCartButton.textContent = 'Add to Cart';

    }
    modalDescription.textContent = product.description;
    modalRating.textContent = `${product.rating}/5 (${product.review_count} reviews)`;
    modalImage.src = product.image;
    modalImage.alt = product.name;
    modalReviews.innerHTML = "";

    if (product.reviews.length === 0) {

        modalReviews.innerHTML = "<p>No reviews yet. Be the first to review this product!</p>";

    } 
    else {

        product.reviews.forEach(review => {

            const reviewCard = document.createElement("div");

            reviewCard.classList.add("review-card");

            reviewCard.innerHTML = `

                <div class="review-header">

                    <strong>${review.user}</strong>

                    <span>${"⭐".repeat(review.rating)}</span>

                </div>

                <small>${review.date}</small>

                <p>${review.comment}</p>

            `;

            modalReviews.appendChild(reviewCard);

        });

    }

    modalReviewSection.innerHTML = "";

    if (product.can_review) {

        modalReviewSection.innerHTML = `

            <div class="review-form">

                <label><strong>Your Rating</strong></label>

                <div class="review-stars">

                    <span class="review-star" data-rating="1">☆</span>
                    <span class="review-star" data-rating="2">☆</span>
                    <span class="review-star" data-rating="3">☆</span>
                    <span class="review-star" data-rating="4">☆</span>
                    <span class="review-star" data-rating="5">☆</span>

                </div>

                <textarea
                    class="review-comment"
                    placeholder="Share your experience with this product..."
                    rows="4">
                </textarea>

                <button class="submit-review-btn">

                    Submit Review

                </button>

            </div>

        `;

        initializeReviewStars();

        const submitButton = document.querySelector(".submit-review-btn");

        submitButton.addEventListener("click", async () => {

            if (selectedRating === 0) {

                showToast("Please select a rating.", true);
                
                return;

            }

            const comment = document.querySelector(".review-comment").value;

            const formData = new FormData();

            formData.append("product_id", currentProductId);
            formData.append("rating", selectedRating);
            formData.append("comment", comment);

            const response = await fetch("/reviews/submit/", {

                method: "POST",

                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },

                body: formData

            });

            if (!response.ok) {

                const data = await response.json();

                showToast(data.message, true);

                return;

            }

    const data = await response.json();

    if (data.success) {

        showToast(data.message);

        loadProduct(currentProductId);

    }
    else {

        showToast(data.message, true);

    }

});

    }
    else {

        modalReviewSection.innerHTML = `<p>${product.review_message}</p>`;

    }

    modalRelatedProducts.innerHTML = "";

    if (product.related_products.length === 0) {

        modalRelatedProducts.innerHTML = "<p>No related products found.</p>";

    } 
    else {

        product.related_products.forEach(item => {

            const relatedCard = document.createElement("div");

            relatedCard.classList.add("related-product-card");

            relatedCard.innerHTML = `

                <img src="${item.image}" alt="${item.name}">

                <div class="related-product-info">

                    <h5>${item.name}</h5>

                    <p>${item.brand}</p>

                    <span>⭐ ${item.rating}/5</span>

                    <strong>€${item.price}</strong>

                </div>

            `;

            // Make related products clickable

            relatedCard.addEventListener("click", () => {

                loadProduct(item.id);

            });

            modalRelatedProducts.appendChild(relatedCard);

        });

    }

    if (product.stock === 0) {

        currentQuantity = 0;

    }
    else {

        currentQuantity = 1;

    }

    quantityValue.textContent = currentQuantity;

    updateQuantityButtons();

    modalOverlay.classList.add("active");

}

productCards.forEach(card => {

    card.addEventListener("click", () => {

        loadProduct(card.dataset.id);

    });

});

quantityPlus.addEventListener("click", () => {

    if (currentQuantity < maxStock) {

        currentQuantity++;

        quantityValue.textContent = currentQuantity;

        updateQuantityButtons();

    }

});

quantityMinus.addEventListener("click", () => {

    if (currentQuantity > 1) {

        currentQuantity--;

        quantityValue.textContent = currentQuantity;

        updateQuantityButtons();

    }

});

const closeButton = document.querySelector(".modal-close");

closeButton.addEventListener("click", () => {

    modalOverlay.classList.remove("active");

});

modalOverlay.addEventListener("click", (event) => {

    if (event.target === modalOverlay) {

        modalOverlay.classList.remove("active");

    }

});

document.addEventListener("keydown", (event) => {

    if (event.key === "Escape") {

        modalOverlay.classList.remove("active");

    }

});

addCartButton.addEventListener("click", async () => {

    const formData = new FormData();

    formData.append("product_id", currentProductId);
    formData.append("quantity", currentQuantity);

    const response = await fetch('/cart/add/', {

        method: "POST",
        headers: {

            "X-CSRFToken": getCookie("csrftoken")

        },
        body: formData

    });

    const data = await response.json();

    if (data.login_required) {

        window.location.href = '/accounts/login/';

        return;

    }

    if (data.success) {

        modalOverlay.classList.remove("active");

        showToast(data.message);

    }
    else {

        showToast(data.message, true);

    }

});

function getCookie(name) {

    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;

            }

        }

    }

    return cookieValue;

}

let selectedRating = 0;

function initializeReviewStars() {

    selectedRating = 0;

    const stars = document.querySelectorAll(".review-star");

    stars.forEach(star => {

        star.addEventListener("click", () => {

            selectedRating = Number(star.dataset.rating);

            stars.forEach(s => {

                if (Number(s.dataset.rating) <= selectedRating) {

                    s.textContent = "★";

                }
                else {

                    s.textContent = "☆";

                }

            });

        });

    });

}

function showToast(message, isError = false) {

    const toast = document.querySelector("#toast");
    const toastText = document.querySelector("#toast-text");

    toastText.textContent = message;

    if (isError) {

        toast.classList.add("error");

    }
    else {

        toast.classList.remove("error");

    }

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);

}