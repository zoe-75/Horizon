
 document.addEventListener("DOMContentLoaded", function () {
  const items = document.querySelectorAll(".menu-item");

  // Get last active item from localStorage
  const activeText = localStorage.getItem("activeSidebarItem");

  items.forEach(item => {
    if (item.textContent === activeText) {
      item.classList.add("active");
    }

    item.addEventListener("click", function () {
      items.forEach(btn => btn.classList.remove("active"));
      this.classList.add("active");

      // Save clicked item
      localStorage.setItem("activeSidebarItem", this.textContent);
    });
  });
});







// Clone the header
document.addEventListener('DOMContentLoaded', () => {

  // Scroll handler to toggle "down" class
  window.addEventListener('scroll', () => {
    const fromTop = window.scrollY;
    document.body.classList.toggle('up', fromTop > 1);
  });

  // Enable search behavior in both headers
  document.querySelectorAll('.header-default, .header-default.clone').forEach(header => {
    const searchToggle = header.querySelector('.searchToggle');
    const searchForm = header.querySelector('.searchForm');
    const navLinks = header.querySelector('.navLinks');
    const closeSearch = header.querySelector('.closeSearch');
    const searchInput = searchForm?.querySelector('input');

    if (searchToggle && searchForm && navLinks &&  searchInput) {
      searchToggle.addEventListener('click', () => {
        searchToggle.style.display = 'none';
        searchForm.classList.add('active');
        setTimeout(() => searchInput.focus(), 50);
      });

 
    }
  });
});






const tabsBox = document.querySelector(".tabs-box"),
allTabs = tabsBox.querySelectorAll(".tab"),
arrowIcons = document.querySelectorAll(".icon i");

let isDragging = false;

const handleIcons = (scrollVal) => {
    let maxScrollableWidth = tabsBox.scrollWidth - tabsBox.clientWidth;
    arrowIcons[0].parentElement.style.display = scrollVal <= 0 ? "none" : "flex";
    arrowIcons[1].parentElement.style.display = maxScrollableWidth - scrollVal <= 1 ? "none" : "flex";
}

// Arrow click (left/right)
arrowIcons.forEach(icon => {
    icon.addEventListener("click", () => {
        let scrollWidth = tabsBox.scrollLeft += icon.id === "left" ? -340 : 340;
        handleIcons(scrollWidth);
    });
});

allTabs.forEach(tab => {
    tab.addEventListener("click", () => {
        tabsBox.querySelector(".active").classList.remove("active");
        tab.classList.add("active");
    });
});

    allTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabsBox.querySelector(".active").classList.remove("active");
            tab.classList.add("active");
        });
    });


// Dragging by mouse
const dragging = (e) => {
    if(!isDragging) return;
    tabsBox.classList.add("dragging");
    tabsBox.scrollLeft -= e.movementX;
    handleIcons(tabsBox.scrollLeft);
}

const dragStop = () => {
    isDragging = false;
    tabsBox.classList.remove("dragging");
}

tabsBox.addEventListener("mousedown", () => isDragging = true);
tabsBox.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);

// ✅ Mouse Wheel Scroll Handling

tabsBox.addEventListener('wheel', (e) => {
    e.preventDefault();
    tabsBox.scrollLeft += e.deltaY * 1.2; 
    handleIcons(tabsBox.scrollLeft);
});




$(document).ready(function () {
    let limit = 3;
    let start = 3;
    let action = 'inactive';
    let currentCategoryId = null;

    function load_post_data(limit, start, categoryId = null) {
        let url = categoryId ? `/blogs/${categoryId}/` : '/';

        $.ajax({
            url: url,
            method: 'GET',
            data: {
                limit: limit,
                start: start
            },
            cache: false,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function (response) {
                if ($.trim(response) === "") {
                    $('#more-data').html("<button type='button' class='btn btn-info bg-danger bg-opacity-10  text-danger '> :( no post found</button>");
                    action = 'done'; 
                } else {
                    $("#post-container").append(response);
                    $('#more-data').html(`
                        <div class="content-spacer d-flex justify-content-center align-items-center">
                            <div class="spinner-border text-info" role="status"></div>
                        </div>
                    `);
                    action = 'inactive';
                }
            },
            error: function () {
                $('#more-data').html(
                    "<button type='button' class='btn btn-danger'>Error loading posts</button>"
                );
                action = 'inactive';
            }
        });
    }

    // Initial load
    if (action === 'inactive') {
        action = 'active';
        load_post_data(limit, 0);
    }

    // Infinite scroll trigger
    $('.main-content').on('scroll', function () {
        if (
            $(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight - 100 &&
            action === 'inactive'
        ) {
            action = 'active';
            start += limit;
            setTimeout(function () {
                load_post_data(limit, start, currentCategoryId);
            }, 600);
        }
    });

    // Category filter click handler
    $(document).on('click', '.category-btn', function (e) {
        e.preventDefault();
        let categoryId = $(this).data('id');
        currentCategoryId = categoryId;
        start = 0;
        action = 'inactive'; // Reset action to allow loading on new category
        $('#post-container').css('opacity', 0.2);

        $.ajax({
            url: `/blogs/${categoryId}/`,
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function (response) {
                setTimeout(() => {
                    $('#post-container').html(response).css('opacity', 1);
                    action = 'inactive';
                    start = limit; // reset start for infinite scroll after filter
                    $('#more-data').html(''); // clear "no posts" or spinner message
                }, 500);
            },
            error: function () {
                $('#post-container').css('opacity', 1);
            }
        });
    });
});




document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.category-btn');
    const container = document.getElementById('post-container');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const categoryId = this.getAttribute('data-id');

            // Fade out
            container.style.transition = 'opacity 300ms ease';
            container.style.opacity = '0.2';

            fetch(`/blogs/${categoryId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                setTimeout(() => {
                    container.innerHTML = html;
                    container.style.opacity = '1';
                }, 300);
            })
            .catch(err => {
                console.error(err);
                container.style.opacity = '1';
            });
        });
    });
});




