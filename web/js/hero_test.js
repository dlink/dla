document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.slide');
    const dotsContainer = document.querySelector('.slider-dots');
    const arrows = document.querySelector('.slider-arrows');
    const play_btn = document.querySelector('.play-btn');
    let currentSlide = 0;
    let play = 1;
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

    // Start slide show
    startSlideShow();

    // Show a specific slide
    function showSlide(index) {
	clearInterval(intervalId);
	slides[currentSlide].style.display = 'none';
	currentSlide = index;
	slides[currentSlide].style.display = 'block';
	togglePlay();
    }

    // Move to the next slide
    function nextSlide() {
	clearInterval(intervalId);
	slides[currentSlide].style.display = 'none';
	currentSlide = (currentSlide + 1) % slides.length;
	slides[currentSlide].style.display = 'block';
	startSlideShow();
    }

    // Move to the previous slide
    function prevSlide() {
	clearInterval(intervalId);
	slides[currentSlide].style.display = 'none';
	currentSlide = (currentSlide - 1 + slides.length) % slides.length;
	slides[currentSlide].style.display = 'block';
	startSlideShow();
    }

    // set slide interval update dots
    function startSlideShow() {
	if(play) {
	    intervalId = setInterval(nextSlide, 5000);
	    updateDots();
	}
    }

    // turn on/off slide show
    function togglePlay() {
	play = !play;
	if(play) {
	    play_btn.innerHTML = '×';
	    nextSlide();
	} else {
	    play_btn.innerHTML = '▸';
	    clearInterval(intervalId);
	}
    }

    // Attach arrow and play click events
    arrows.querySelector('.left').addEventListener('click', prevSlide);
    arrows.querySelector('.right').addEventListener('click', nextSlide);
    play_btn.addEventListener('click', togglePlay);
});
