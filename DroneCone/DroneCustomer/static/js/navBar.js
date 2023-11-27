function initializeAvatarMenu(buttonSelector, menuSelector) {
    let avatarButton = document.querySelector(buttonSelector);
    let avatarMenu = document.querySelector(menuSelector);

    avatarButton.addEventListener("click", (event) => {
        event.stopPropagation();
        if (avatarMenu.getAttribute("data-expanded") === "false") {
            avatarMenu.classList.add("[&&]:block");
            setTimeout(function () {
                avatarMenu.setAttribute("data-expanded", "true");
            }, 1);
        } else {
            avatarMenu.setAttribute("data-expanded", "false");
        }
    });

    avatarMenu.addEventListener("transitionend", () => {
        if (avatarMenu.getAttribute("data-expanded") === "false") {
            avatarMenu.classList.remove("[&&]:block");
        }
    });

    document.addEventListener("click", (event) => {
        if (!avatarMenu.contains(event.target)) {
            if (avatarMenu.getAttribute("data-expanded") === "true") {
                avatarMenu.setAttribute("data-expanded", "false");
                event.stopPropagation();
            }
        }
    });
}

window.addEventListener("load", function () {
    initializeAvatarMenu('[id="nav-avatar-button"]', '[id="nav-avatar-popup"]');
    const navHamburger = document.querySelector('[id="nav-hamburger"]');
    const navDropdown = document.querySelector('[id="nav-links"]');

    navHamburger.addEventListener("click", () => {
        navHamburger.classList.toggle("ring-2");
        navDropdown.classList.toggle("hidden");
    });

     // Highlight current tab.
     /*
     document.querySelectorAll("a.nav-li").forEach(link => {
        if (link.href.includes(`${window.location.pathname}`)) {
            link.setAttribute('aria-current', 'page');
        }
     })
     */

    // Dismiss Alert
    let dismissible = document.querySelectorAll("[data-dismissible]");
    let targets = document.querySelectorAll("[data-dismissible-target]");
    if (dismissible && targets) {
        dismissible.forEach(function (dismiss) {
            return targets.forEach(function (target) {
                if (dismiss.dataset.dismissible === target.dataset.dismissibleTarget) {
                    target.addEventListener("click", function () {
                        dismiss.classList.toggle("hidden");
                    });
                }
            });
        });
    }
});
