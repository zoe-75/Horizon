
//  document.addEventListener("DOMContentLoaded", function () {
//   const items = document.querySelectorAll(".menu-item");

//   // Get last active item from localStorage
//   const activeText = localStorage.getItem("activeSidebarItem");

//   items.forEach(item => {
//     if (item.textContent === activeText) {
//       item.classList.add("active");
//     }

//     item.addEventListener("click", function () {
//       items.forEach(btn => btn.classList.remove("active"));
//       this.classList.add("active");

//       // Save clicked item
//       localStorage.setItem("activeSidebarItem", this.textContent);
//     });
//   });
// });



      // Toggle More
    document.getElementById('moreBtn').addEventListener('click', function (e) {
      e.stopPropagation();
      document.getElementById('moreMenu').classList.toggle('show');
      document.getElementById('profileMenu').classList.remove('show');
    });

    // Toggle Profile
    document.getElementById('profileBtn').addEventListener('click', function (e) {
      e.stopPropagation();
      document.getElementById('profileMenu').classList.toggle('show');
      document.getElementById('moreMenu').classList.remove('show');
    });

    // Hide dropups when clicking outside
    document.addEventListener('click', function () {
      document.getElementById('moreMenu').classList.remove('show');
      document.getElementById('profileMenu').classList.remove('show');
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
    let start = 0;
    let action = 'inactive';
    let currentCategoryId = null;

    function load_post_data(startVal, categoryId = null, append = true) {
        let url = categoryId
            ? `/blogs/${categoryId}/?limit=${limit}&start=${startVal}`
            : `/?limit=${limit}&start=${startVal}`;

        console.log("▶ loading", url);

        $.ajax({
            url: url,
            method: 'GET',
            cache: false,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function (response) {
                if ($.trim(response) === "") {
                    $('#more-data').html(`<button type='button' class='btn2 fw-bold text-white'>:( No more posts</button>`);
                    action = 'done';
                } else {
                    if (append) {
                        $('#post-container').append(response);
                    } else {
                        $('#post-container').html(response);
                    }

                    $('#post-container').css('opacity', 1);
                    $('#more-data').html('');
                    action = 'inactive';
                }
            },
            error: function () {
                $('#more-data').html(`<button type='button' class='btn2 btn-danger'>:( Error loading posts</button>`);
                action = 'inactive';
            }
        });
    }

    // 🔁 Initial load
    load_post_data(start);

    // 🔁 Infinite scroll
$('.main-content').on('scroll', function () {
    if (
        $(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight - 100 &&
        action === 'inactive'
    ) {
        action = 'active';
        start += limit;

        setTimeout(() => {
            load_post_data(start, currentCategoryId, true);
        }, 1000); // 1000ms delay
    }
});
    // ✅ Category click handler
    $(document).on('click', '.category-link', function (e) {
        e.preventDefault();

        $('.category-link').removeClass('active');
        $(this).addClass('active');

        let categoryId = $(this).data('id');
        currentCategoryId = categoryId === 'all' ? null : categoryId;

        // Reset everything
        start = 0;
        action = 'active';

        $('#post-container').fadeOut(200, function () {
            $(this).empty();
            $('#more-data').empty();

            load_post_data(start, currentCategoryId, false); // clear and reload
            $('#post-container').fadeIn(300);

            // Wait and check scroll fill
            setTimeout(() => {
                const el = $('.main-content')[0];
                if (el.scrollHeight <= el.clientHeight + 100 && action === 'inactive') {
                    action = 'active';
                    start += limit;
                    load_post_data(start, currentCategoryId, true);
                }
            }, 500);
        });
    });
});



// const links = document.querySelectorAll('.nav-item');
// links.forEach(link => {
//   link.addEventListener('click', function (e) {
//     e.preventDefault(); // prevent jumping to `#`
//     links.forEach(l => l.classList.remove('active'));
//     this.classList.add('active');
//   });
// });


document.addEventListener("DOMContentLoaded", () => {
  const contentDiv = document.getElementById("content");
  const spinner = document.getElementById("loading-spinner");

  async function loadContent(url, pushToHistory = true) {
    try {
  
    //   spinner.style.display = "block";
    //   contentDiv.classList.add("fade-out");

      setTimeout(async () => {
        const response = await fetch(url, {
          headers: {
            "X-Requested-With": "XMLHttpRequest"
          }
        });

        if (!response.ok) throw new Error("Request failed");

        const html = await response.text();
        contentDiv.innerHTML = html;
        contentDiv.classList.remove("fade-out");
        contentDiv.classList.add("fade-in");

        setTimeout(() => {
          contentDiv.classList.remove("fade-in");
        }, 500); 

        // spinner.style.display = "none";

        if (pushToHistory) {
          window.history.pushState({ url: url }, "", url);
        }
      }, 400); 
    } catch (err) {
      spinner.style.display = "none";
      contentDiv.classList.remove("fade-out");
      console.error("AJAX Load Error:", err);
    }
  }

 
  document.body.addEventListener("click", (e) => {
    const link = e.target.closest(".ajax-link");
    if (!link) return;

    e.preventDefault();
    const url = link.getAttribute("href");
    loadContent(url);
  });


  window.addEventListener("popstate", (e) => {
    if (e.state && e.state.url) {
      loadContent(e.state.url, false);
    }
  });
  document.body.addEventListener("click", (e) => {
  const homeBtn = e.target.closest("#ajax-home-button");
  if (homeBtn) {
    e.preventDefault();
    loadContent("/", true); 
  }
});
});
