const cartCards = document.querySelectorAll(".cart-card");

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

const csrftoken = getCookie("csrftoken");

document.addEventListener("click", function(event) {

    const quantityButton = event.target.closest(".quantity-btn");

    const removeButton = event.target.closest(".remove-btn");

    if (!quantityButton && !removeButton) {

        return;

    }

    const cartCard = event.target.closest(".cart-card");

    const productId = cartCard.dataset.productId;

    let action;

    if (removeButton) {

        action = 'remove';

    }
    else if (quantityButton.classList.contains("plus-btn")) {

        action = 'increase';

    }
    else {

        action = 'decrease';

    }

    updateCart(productId, action, cartCard);

});

function updateCart(productId, action, cartCard) {

    fetch('/cart/update/', {

        method: 'POST',

        headers: {

            'X-CSRFToken': csrftoken,

            'Content-Type': 'application/x-www-form-urlencoded',

        },

        body: new URLSearchParams({

            product_id: productId,

            action: action

        })

    })

    .then(response => response.json())

    .then(data => {

        if (!data.success) {

            showToast(data.message, true);

            return;

        }

        if (data.removed) {

            cartCard.remove();

            if (document.querySelectorAll(".cart-card").length === 0) {

                document.querySelector("#cart-content").style.display = "none";

                document.querySelector("#empty-cart").style.display = "block";

            }

        }
        else {

            cartCard.querySelector(".quantity-value").textContent = data.quantity;

            cartCard.querySelector(".subtotal-value").textContent = Number(data.subtotal).toFixed(2);

        }

        document.querySelector("#cart-total").textContent = Number(data.cart_total).toFixed(2);

        document.querySelector("#cart-count").textContent = data.cart_count;

    })

    .catch(error => {

        console.error(error);

    });

}