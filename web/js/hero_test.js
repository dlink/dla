document.addEventListener('DOMContentLoaded', function () {
    console.log('started');
  const slides = document.querySelectorAll('.slide');
  let currentSlide = 0;

  // Show the first slide initially
  slides[currentSlide].style.display = 'block';

  // Set an interval to switch slides (adjust the duration as needed)
  setInterval(function () {
    slides[currentSlide].style.display = 'none';
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].style.display = 'block';
  }, 5000); // Switch slides every 5 seconds (adjust as needed)
});
