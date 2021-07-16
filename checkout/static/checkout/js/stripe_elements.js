/* 
    Core logic/payment flow for this comes from:
    https://stripe.com/docs/payments/accept-a-payment

    CSS comes from:
    https://stripe.com/docs/stripe-js
*/

// Get public key and client secret
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);

// Set up Stripe
var stripe = Stripe(stripe_public_key);

// Create an instance of stripe elements
var elements = stripe.elements();

// Styling of card element
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create card element
var card = elements.create('card', {style: style});

// mount card to card div with card element in checkout.html
card.mount('#card-element')

// Handle realtime validation erros on the card element
card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

/* 
    Step 1 - When user hits checkout page: Checkout view creates Stripe paymentintent
    Step 2 - When Stripe creates paymentintent: Stripe returns client_secret, which is returned to template
    Step 3 - Call the confirm card payemnt: Use client_secret in the template to call confirmCardPayment() and verify card
*/