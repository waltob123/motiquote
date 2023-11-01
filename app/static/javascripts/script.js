// Script for the application
// Author: Desmond Asiedu Asamoah
// Date: 1/11/2023


// All variables
const closeBtn = document.querySelector('.close-icon');
const flashMessage = document.querySelector('#flash-messages');


// All functions
// Function to close the flash message
const closeFlashMessage = () => {
    console.log('closed');
    flashMessage.style.display = 'none';
}

// All event listeners
closeBtn.addEventListener('click', closeFlashMessage);
