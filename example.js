function capture() {
    const v = document.querySelector("video"), c = document.querySelector("#canvas");
    c.width = v.videoWidth; c.height = v.videoHeight;
    c.getContext("2d").drawImage(v, 0, 0, c.width, c.height);
}
