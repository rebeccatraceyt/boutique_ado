/* 
    Core logic/payment flow for this comes from:
    https://stripe.com/docs/payments/accept-a-payment

    CSS comes from:
    https://stripe.com/docs/stripe-js
*/

/* 
    Step 1 - When user hits checkout page: Checkout view creates Stripe paymentintent
    Step 2 - When Stripe creates paymentintent: Stripe returns client_secret, which is returned to template
    Step 3 - Call the confirm card payemnt: Use client_secret in the template to call confirmCardPayment() and verify card
*/

// Get public key and client secret
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

// Set up Stripe
var stripe = Stripe(stripePublicKey);

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

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // Prevents default POST action
    ev.preventDefault();

    // disable card element and submit to prevent multilple submissions
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    // Call Confirm Card method
    stripe.confirmCardPayment(clientSecret, {
        // provide card to stripe
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        // Then execute this function
        if (result.error) {
            // put error message in card-error div
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;

            // if there is an error, re-enable card element and submit button
            $(errorDiv).html(html);
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            // if status of payment intent is succeeded, submit form
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});
