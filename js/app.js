/*--------------------------*/
/*         INDEX            */
/*###########################
 *     01.  Loader          *
 *     02.  Menu            *
 *     03.  Sticky Menu     *
 *     03.  Back to top     *
############################*/

function hidePreloader() {
  const preloader = document.getElementById("preloader");
  if (!preloader || preloader.dataset.hidden === "true") return;

  preloader.dataset.hidden = "true";
  preloader.style.visibility = "hidden";
  preloader.style.opacity = "0";
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", hidePreloader, { once: true });
} else {
  hidePreloader();
}

// Never let a slow remote asset or media request trap the page behind the loader.
setTimeout(hidePreloader, 1500);

function loadDeferredVideo(video) {
  const sources = video.querySelectorAll("source[data-src]");
  sources.forEach((source) => {
    source.src = source.dataset.src;
    source.removeAttribute("data-src");
  });
  video.load();
  video.play().catch(() => {});
}

function initDeferredVideos() {
  const videos = document.querySelectorAll("video[data-lazy-video]");
  if (!videos.length) return;

  if (!("IntersectionObserver" in window)) {
    videos.forEach(loadDeferredVideo);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        loadDeferredVideo(entry.target);
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "400px 0px" }
  );

  videos.forEach((video) => observer.observe(video));
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initDeferredVideos, { once: true });
} else {
  initDeferredVideos();
}

// Menu sticky
function windowScroll() {
  const navbar = document.getElementById("navbar");
  if (
    document.body.scrollTop >= 50 ||
    document.documentElement.scrollTop >= 50
  ) {
    navbar.classList.add("nav-sticky");
  } else {
    navbar.classList.remove("nav-sticky");
  }
}

window.addEventListener("scroll", (ev) => {
  ev.preventDefault();
  windowScroll();
});

// Back-to-top
var mybutton = document.getElementById("back-to-top");
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (mybutton != null) {
    if (
      document.body.scrollTop > 500 ||
      document.documentElement.scrollTop > 500
    ) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }
}

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

//Feather icon
feather.replace();
