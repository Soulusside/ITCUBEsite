const elts = {
    text1: document.getElementById("text1"),
    text2: document.getElementById("text2")
};

const texts = ["«Это не баг, это фича»",
"«Иногда лучшие программы создаются на бумажке. Запрограммировать их — второстепенная вещь» Max Kanat Alexander",
"«Простота — залог надежности» Edsger W. Dijkstra",
"«Если вы хотите, чтобы код было легко и быстро писать — делайте его удобным для чтения» Robert C. Martin",
"«Работает? Не трогай» Любой программист",
"«Нельзя доверять коду, который вы не написали полностью сами» Ken Thompson",
"«Программирование — это не наука, а ремесло» Richard Stallman",
"«Когда вам в голову пришла хорошая идея, действуйте незамедлительно» Билл Гейтс»",
"«Компьютер — это самый удивительный инструмент, с каким я когда-либо сталкивался. Это велосипед для нашего сознания» Стив Джобс",
];

const morphTime = 0.5;
const cooldownTime = 1;

let textIndex = texts.length - 1;
let time = new Date();
let morph = 0;
let cooldown = cooldownTime;

elts.text1.textContent = texts[textIndex % texts.length];
elts.text2.textContent = texts[(textIndex + 1) % texts.length];

function doMorph() {
    morph -= cooldown;
    cooldown = 0;

    let fraction = morph / morphTime;

    if (fraction > 1) {
        cooldown = cooldownTime;
        fraction = 1;
    }

    setMorph(fraction);
}

function setMorph(fraction) {
    elts.text2.style.filter = `blur(${Math.min(8 / fraction - 8, 100)}px)`;
    elts.text2.style.opacity = `${Math.pow(fraction, 0.4) * 100}%`;

    fraction = 1 - fraction;
    elts.text1.style.filter = `blur(${Math.min(8 / fraction - 8, 100)}px)`;
    elts.text1.style.opacity = `${Math.pow(fraction, 0.4) * 100}%`;

    elts.text1.textContent = texts[textIndex % texts.length];
    elts.text2.textContent = texts[(textIndex + 1) % texts.length];
}

function doCooldown() {
    morph = 0;

    elts.text2.style.filter = "";
    elts.text2.style.opacity = "100%";

    elts.text1.style.filter = "";
    elts.text1.style.opacity = "0%";
}

function animate() {
    requestAnimationFrame(animate);

    let newTime = new Date();
    let shouldIncrementIndex = cooldown > 0;
    let dt = (newTime - time) / 5000;
    time = newTime;

    cooldown -= dt;

    if (cooldown <= 0) {
        if (shouldIncrementIndex) {
            textIndex++;
        }

        doMorph();
    } else {
        doCooldown();
    }
}

animate();
