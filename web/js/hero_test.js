document.addEventListener('DOMContentLoaded', function () {
  const slides = document.querySelectorAll('.slide');
  const dotsContainer = document.querySelector('.slider-dots');
  const arrows = document.querySelector('.slider-arrows');
  let currentSlide = 0;

  // Show the first slide initially
  slides[currentSlide].style.display = 'block';

  // Create dots dynamically based on the number of slides
  slides.forEach((slide, index) => {
    const dot = document.createElement('div');
    dot.classList.add('dot');
    dot.addEventListener('click', () => showSlide(index));
    dotsContainer.appendChild(dot);
  });

  // Highlight the active dot
  function updateDots() {
    const dots = dotsContainer.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
      if (index === currentSlide) {
        dot.style.backgroundColor = '#333';
      } else {
        dot.style.backgroundColor = '#aaa';
      }
    });
  }

  // Set an interval to switch slides (adjust the duration as needed)
  const intervalId = setInterval(nextSlide, 5000);

  // Show a specific slide
  function showSlide(index) {
    clearInterval(intervalId); // Stop the automatic slide change
    slides[currentSlide].style.display = 'none';
    currentSlide = index;
    slides[currentSlide].style.display = 'block';
    updateDots();
    // Restart the interval
    intervalId = setInterval(nextSlide, 5000);
  }

  // Move to the next slide
  function nextSlide() {
    slides[currentSlide].style.display = 'none';
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].style.display = 'block';
    updateDots();
  }

  // Move to the previous slide
  function prevSlide() {
    slides[currentSlide].style.display = 'none';
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    slides[currentSlide].style.display = 'block';
    updateDots();
  }

  // Attach arrow click events
  arrows.querySelector('.left').addEventListener('click', prevSlide);
  arrows.querySelector('.right').addEventListener('click', nextSlide);
});
