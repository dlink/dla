document.addEventListener('DOMContentLoaded', function () {
    
    /* pic-menu display-pic chooser */
    const picMenuItems = document.querySelectorAll('.pic-menu-item');
    picMenuItems.forEach(item => {
	item.addEventListener('click', function () {
	    const idParts = this.id.split('-');
	    /* parse n from id in the form of pic-num-[n] */
	    const pic_num = idParts[idParts.length - 1];
	    var mainPics = document.querySelectorAll('img.main-pic');
	    mainPics.forEach(function (pic, index) {
		if (index == pic_num) {
		    pic.classList.add('selected');
		} else {
		    pic.classList.remove('selected');
		}
	    });
	});
    });

});
