async function fetchItems() {
    const response = await fetch(window.location.href);
    const data = await response.json();
    const result_txt = document.getElementById("result_txt");
    result_txt.textContent = data["endresult"];
}
fetchItems();
document.addEventListener('DOMContentLoaded', function () {
    fetchItems();
    // 5초마다 페이지 새로고침
    setInterval(fetchItems, 5000);
});

let position = 0;
let prev = 0;
let list = [
    { menu: '돼지국밥', img: photo, des1: '따끈하게 속을 채워주는', des2: ': 국밥은 언제나 맛있다' },
    { menu: '돼지국밥2', img: qr, des1: '따끈하게 속을 채워주는', des2: ': 국밥은 언제나 맛있다22' },
    { menu: '돼지국밥3', img: photo, des1: '따끈하게 속을 채워주는', des2: ': 국밥은 언제나 맛있다333' }
];
let fade = "";
let rotatefade = "";

function handleLeftArrowClick() {
    position = position === 0 ? 0 : position - 1;
}

function handleRightArrowClick() {
    position = position === 2 ? 2 : position + 1;
}

let opacityLeft;
let opacityRight;

if (position === 0) {
    opacityLeft = 0.3;
    opacityRight = 1;
} else if (position === list.length - 1) {
    opacityLeft = 1;
    opacityRight = 0.3;
} else {
    opacityLeft = 1;
    opacityRight = 1;
}