// Script for the application
// Author: Desmond Asiedu Asamoah
// Date: 1/11/2023


// All variables
    const flashMessageCloseBtn = document.querySelector('#flash-messages .close-icon');
    const flashMessage = document.querySelector('#flash-messages');

    // create quote
    const createQuote = document.querySelector('#create-quote');
    const addQuoteBtn = document.querySelector('#add-quote-btn button');
    const addQuoteCloseBtn = document.querySelector('#create-quote .close-icon')

    // view quote
    const viewQuote = document.querySelector('#view-quote');
    const viewQuoteBtn = document.querySelectorAll('#view-quote-btn');
    const viewQuoteCloseBtn = document.querySelector('#view-quote .close-icon');

    // edit quote
    const editQuoteForm = document.querySelector('#view-quote form');
    const quoteEditInput = document.querySelector('#edit-quote-input');
    const authorEditInput = document.querySelector('#edit-author-input');
    const categoryEditOption = document.querySelectorAll('#edit-category-input option');
    const categoryEditInput = document.querySelector('#edit-category-input');
    const postQuoteBtn = document.querySelector('#view-quote .post-btn');
    const editQuoteBtn = document.querySelector('#view-quote .edit-btn');


    // edit profile
    const editProfileBtn = document.querySelector('#edit-profile-btn');
    const editProfileForm = document.querySelector('form#edit-profile-form');
    const editProfileGender = document.querySelector('.gender-id');
    const editProfileCountry = document.querySelector('.country-id');

    const body = document.querySelector('body');




// All functions
    // Function to close the flash message
    const closeFlashMessage = () => {
        flashMessage.style.display = 'none';
    }

    // Function to add a new quote
    const addQuote = () => {
        body.classList.add('open');
        createQuote.classList.add('open');
    }

    // Function to view a quote
    async function viewEditQuote(btn) {
        body.classList.add('open');  // add open class to body
        viewQuote.classList.add('open');  // add open class to view quote modal

        const response = await fetch(`/quotes/${btn.dataset.quoteid}`);
        if (response.ok) {
            const quote = await response.json();  // get the quote
            quoteEditInput.value = quote.quote;  // set the quote input value to the quote
            quoteEditInput.disabled = true;  // disable the quote input
            
            authorEditInput.value = quote.author;  // set the author input value to the author
            authorEditInput.disabled = true;  // disable the author input

            // select the option that matches the category id of the quote
            categoryEditOption.forEach(option => {
                if (option.value == quote.category_id) {
                    option.selected = true;
                }
            });

            // set edit quote form action to the quote id
            editQuoteForm.action = quote.quote_url;

            categoryEditInput.disabled = true;  // disable the category input
        }

        // disable post btn
        postQuoteBtn.classList.add('disabled');
        postQuoteBtn.disabled = true;
    }


    // Function to set inputs to editable when edit btn is clicked
    function editQuote() {
        quoteEditInput.disabled = false;  // enable the quote input
        authorEditInput.disabled = false;  // enable the author input
        categoryEditInput.disabled = false;  // enable the category input

        // enable post btn
        postQuoteBtn.classList.remove('disabled');
        postQuoteBtn.disabled = false;

        // disable edit btn
        editQuoteBtn.classList.add('disabled');
        editQuoteBtn.disabled = true;
    }


    // Function to close quote modal
    const closeQuote = (quoteType) => {
        body.classList.remove('open');
        quoteType.classList.remove('open');
        editQuoteBtn.classList.remove('disabled');
        editQuoteBtn.disabled = false;
    }


    // Function to edit profile
    const editProfile = (e) => {
        // select the option that matches the gender id of the user
        editProfileGender.querySelectorAll('option').forEach(option => {
            if (option.value == editProfileGender.getAttribute('gender_id')) {
                option.selected = true;
            }
        });

        // select the option that matches the country id of the user
        editProfileCountry.querySelectorAll('option').forEach(option => {
            if (option.value == editProfileCountry.getAttribute('country_id')) {
                option.selected = true;
            }
        });

        // enable all inputs
        editProfileForm.querySelectorAll('.form-input').forEach(input => {
            input.disabled = false;
            e.target.disabled = true;
        });

        editProfileForm.querySelector('.btn-primary').disabled = false;  // enable submit btn
    }

// All event listeners
    if (flashMessageCloseBtn) {
        flashMessageCloseBtn.addEventListener('click', closeFlashMessage);
    }

    if (addQuoteCloseBtn) {
        addQuoteCloseBtn.addEventListener('click', () => closeQuote(createQuote));
    }

    if (viewQuoteCloseBtn) {
        viewQuoteCloseBtn.addEventListener('click', () => closeQuote(viewQuote));
    }

    // event listener for add quote btn
    if (addQuoteBtn) {
        addQuoteBtn.addEventListener('click', addQuote);
    }
    // event listener for view btn
    if (viewQuoteBtn) {
        viewQuoteBtn.forEach(
            (btn) => btn.addEventListener('click', () => viewEditQuote(btn))
        );
    }


    // event listener for edit btn
    if (editQuoteBtn) {
        editQuoteBtn.addEventListener('click', editQuote);
    }

    // event listener for edit profile btn
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', e => {
            editProfile(e);
        });
    }
