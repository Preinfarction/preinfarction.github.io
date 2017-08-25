var homoglyphs = {
    "a": ["α", "а", "𝛂", "𝛼", "𝜶", "𝝰", "𝞪"],
    "b": ["β", "Ъ", "Ь", "ь", "ߕ", "ხ", "Ꮟ", "ᑲ", "ᕊ", "ᖯ", "♭", "𐌁", "𐌜"],
    "c": ["©", "С", "с", "ᑕ", "ꮯ", "𐐽"],
    "d": ["ժ", "߄", "ძ", "Ꮷ", "ᑯ", "ᑰ", "ᕍ", "∂̵", "ꓒ"],
    "e": ["Є", "е", "ҽ", "ᘓ", "€", "℮", "𐌴"],
    "f": ["ſ", "ƒ", "ғ", "բ", "ߓ", "𐌅", "𝟋"],
    "g": ["ց", "ٶ", "Ⴚ", "Ꮐ", "𝟿", "9"],
    "h": ["Η", "Н", "һ", "ի", "հ", "Ⴙ", "ከ", "ዣ", "Ꮋ", "Ꮒ"],
    "i": ["¡", "¦", "ı", "Ι", "ι", "І", "і", "أ", "ا", "Ꭵ", "ᛁ", "ꜟ", "ꭵ", "𐒃", "𝔧", "𝚤", "𝛊", "𝜄", "𝜾", "𝝸", "𝞲"],
    "j": ["Ј", "ј", "յ", "ل", "ݪ", "Ꭻ", "ᒍ", "ᒎ", "ᒙ", "ᒨ"],
    "k": ["ĸ", "Κ", "κ", "К", "қ", "Ꮶ", "ᛕ"],
    "l": ["ι", "׀", "ו", "ן", "ا", "١", "۱", "ߊ", "Ꮮ", "ᛁ", "ⵏ", "ꓲ", "￨", "𐌉", "𐌠", "𝐈", "𝐼", "𝑰", "𝖨", "𝗜", "𝘐", "𝙄", "𝚰", "𝛪", "𝜤", "𝝞", "𝞘", "𝟷", "1", "|"],
    "m": ["Μ", "М", "м", "ጣ", "Ꮇ", "ᘻ", "ᙏ", "ᛖ", "₥", "𐌑"],
    "n": ["Ν", "η", "п", "ո", "ռ", "ᑎ"],
    "o": ["ο", "σ", "о", "օ", "ס", "٥", "ߋ", "०", "৹", "੦", "૦", "௦", "౦", "೦", "ഠ", "൦", "๐", "໐", "ဝ", "၀", "ჿ", "₀", "◦", "𐐬", "𝛐", "𝛔", "𝜊", "𝜎", "𝝄", "𝝈", "𝝾", "𝞂", "𝞸", "𝞼", "0"],
    "p": ["Þ", "þ", "Ρ", "ρ", "Р", "р", "Ꮲ", "ᑭ", "ᕈ", "𐌓", "𝛒", "𝛠", "𝜌", "𝝆", "𝞀", "𝞺"],
    "q": ["ԛ", "գ", "զ", "Ⴍ", "Ⴓ", "ჹ"],
    "r": ["ſ", "г", "Ի", "Ꮢ", "ᚱ", "ꮁ"],
    "s": ["ѕ", "Տ", "Ⴝ", "Ꭶ", "Ꮪ", "ꕶ", "ꮪ", "𐑈"],
    "t": ["ŧ", "Τ", "τ", "Т", "ߙ", "Ꭲ", "†", "✝", "+"],
    "u": ["µ", "μ", "υ", "Ա", "Մ", "Ս", "ս", "ߎ", "ປ", "ᑌ", "ᙀ", "∪", "ⵡ", "𝛖", "𝜐", "𝝊", "𝞄", "𝞾"],
    "v": ["˅", "ν", "Ꮩ", "ᐯ", "∨", "ⴸ", "ꮩ", "𝛎", "𝜈", "𝝂", "𝝼", "𝞶"],
    "w": ["Ԝ", "ԝ", "ա", "Ꮃ", "ꮃ", "🝃"],
    "x": ["×", "Χ", "χ", "Х", "ж", "х", "ᕁ", "᙭", "᙮", "ⵋ", "ⵝ"],
    "y": ["Υ", "γ", "у", "Ү", "ү", "Ұ", "ݍ", "Ⴘ", "ყ", "Ꭹ", "𝛄", "𝛾", "𝜸", "𝝲", "𝞬"],
    "z": ["Ζ", "Ꮓ", "☡", "ꮓ", "𝛧", "𝜁"]
};

function pick(array) {
    return array[Math.floor(Math.random(0, 1) * array.length)];
}

function spoof(text) {
    var spoofed = "", i, homoglyph_array;
    for (i = 0; i < text.length; i++) {
        homoglyph_array = homoglyphs[text[i].toLowerCase()];
        if (homoglyph_array == undefined) {
            spoofed += text[i];
        }
        else {
            spoofed += pick(homoglyphs[text[i].toLowerCase()]);
        }
    }
    return spoofed;
}

function show_spoof() {
    var text = document.getElementById("input").value;
    var spoofed = spoof(text);
    document.getElementById("output").value = spoofed;
}

function init() {
    var input = document.getElementById("input");
    input.value = "Fakey Fakeson‏ @admittedlyhuman 12 Jul 2015\r\ntwitter is basically a teleportation device. you read my tweets and become more similar to me, while on the other end I grow closer to death";
    show_spoof();

    input.addEventListener("input", show_spoof);
}

window.onload = init;
