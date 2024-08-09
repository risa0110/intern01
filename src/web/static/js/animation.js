document.addEventListener('DOMContentLoaded', function() {
      const loginElement = document.querySelector('.login');
      const boxElement = document.querySelector('.box');
      loginElement.addEventListener('click', function() {
        if (boxElement.style.display === 'none' || boxElement.style.display === '') {
          boxElement.style.display = 'block';
        } else {
          boxElement.style.display = 'none';
        }
      });
    });