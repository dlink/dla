document.addEventListener('DOMContentLoaded', function () {
    const picMenuItems = document.querySelectorAll('.pic-menu-item');
    picMenuItems.forEach(item => {
	/* parse n from id in the form of pic-num-[n] */
	item.addEventListener('click', function () {
	    const idParts = this.id.split('-');
	    const pic_num = idParts[idParts.length - 1];
	    document.form1['pic_num'].value = pic_num;
	    document.form1.submit();
	});
    });
});
