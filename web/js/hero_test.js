document.addEventListener('DOMContentLoaded', function () {
  const slides = document.querySelectorAll('.slide');
  const dotsContainer = document.querySelector('.slider-dots');
  const arrows = document.querySelector('.slider-arrows');
  let currentSlide = 0;
  let intervalId;

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
  intervalId = setInterval(nextSlide, 5000);

  // Show a specific slide
  function showSlide(index) {
    clearInterval(intervalId);
    slides[currentSlide].style.display = 'none';
    currentSlide = index;
    slides[currentSlide].style.display = 'block';
    updateDots();
    intervalId = setInterval(nextSlide, 5000);
  }

  // Move to the next slide
  function nextSlide() {
    clearInterval(intervalId);
    slides[currentSlide].style.display = 'none';
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].style.display = 'block';
    updateDots();
    intervalId = setInterval(nextSlide, 5000);
  }

  // Move to the previous slide
  function prevSlide() {
    clearInterval(intervalId);
    slides[currentSlide].style.display = 'none';
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    slides[currentSlide].style.display = 'block';
    updateDots();
    intervalId = setInterval(nextSlide, 5000);
  }

  // Attach arrow click events
  arrows.querySelector('.left').addEventListener('click', prevSlide);
  arrows.querySelector('.right').addEventListener('click', nextSlide);
});
