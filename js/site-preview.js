// Live, non-interactive website previews in project cards. Each iframe renders
// the site at a desktop viewport width and is scaled down to fill its card.
(function () {
  var DESKTOP_WIDTH = 1280;
  var previews = document.querySelectorAll("[data-site-preview]");
  if (!previews.length) return;

  function fit(box) {
    var frame = box.querySelector("iframe");
    var scale = box.clientWidth / DESKTOP_WIDTH;
    if (!frame || !scale) return;
    frame.style.transform = "scale(" + scale + ")";
    frame.style.height = Math.ceil(box.clientHeight / scale) + "px";
  }

  if ("ResizeObserver" in window) {
    var ro = new ResizeObserver(function (entries) {
      entries.forEach(function (entry) {
        fit(entry.target);
      });
    });
    previews.forEach(function (box) {
      ro.observe(box);
    });
  } else {
    previews.forEach(fit);
    window.addEventListener("resize", function () {
      previews.forEach(fit);
    });
  }
})();
