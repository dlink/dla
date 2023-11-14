document.addEventListener('DOMContentLoaded', function () {
    const filter_desc = document.querySelectorAll('.filter_desc')
    const gallery_selector = document.querySelector('.gallery_search');
    const form = document.forms[0];
    const status_sel = document.querySelector('#status');
    const size_range_sel = document.querySelector('#size_range');
    const clear = document.querySelector('#clear')
    console.log(clear);

    filter_desc.forEach((filter_desc, index) => {
	filter_desc.addEventListener('click', openGallerySearch);
    });

    form.addEventListener('submit', closeGallerySearch);
    clear.addEventListener('click', clearGallerySearch);

    function openGallerySearch() {
	gallery_selector.style.display = 'block';
    }
    function closeGallerySearch() {
	gallery_selector.style.display = 'none';
    }
    function clearGallerySearch() {
	status_sel.value = '';
	size_range.value = '';
    }

});
