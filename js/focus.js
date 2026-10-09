// Shared behaviour for the role-focused pages (xr.html, software-ai.html).
(function () {
  document.documentElement.classList.add("js");

  // Scroll reveal
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("vis");
          io.unobserve(e.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );
  document.querySelectorAll(".reveal").forEach(function (el) {
    io.observe(el);
  });

  // Project previews: deferred like the home page's (js/app.js), but paused
  // while off-screen so a page full of looping clips isn't decoding them all.
  var videos = document.querySelectorAll("video[data-lazy-video]");
  var reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!videos.length || reduceMotion) return;

  function load(video) {
    video.querySelectorAll("source[data-src]").forEach(function (source) {
      source.src = source.dataset.src;
      source.removeAttribute("data-src");
    });
    video.load();
  }

  var onScreen = new Set();
  var vo = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        var video = e.target;
        if (e.isIntersecting) {
          onScreen.add(video);
          if (video.querySelector("source[data-src]")) load(video);
          video.play().catch(function () {});
        } else {
          onScreen.delete(video);
          if (!video.paused) video.pause();
        }
      });
    },
    { rootMargin: "200px 0px" }
  );
  videos.forEach(function (video) {
    vo.observe(video);
  });

  // Browsers may pause silent video while the tab is hidden, and returning to
  // the tab doesn't fire the observer again, so restart what's still on screen.
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState !== "visible") return;
    onScreen.forEach(function (video) {
      video.play().catch(function () {});
    });
  });
})();
