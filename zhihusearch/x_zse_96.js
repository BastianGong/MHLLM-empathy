const CryptoJS = require("crypto-js");
let h = {
    "zk": [
        1170614578,
        1024848638,
        1413669199,
        -343334464,
        -766094290,
        -1373058082,
        -143119608,
        -297228157,
        1933479194,
        -971186181,
        -406453910,
        460404854,
        -547427574,
        -1891326262,
        -1679095901,
        2119585428,
        -2029270069,
        2035090028,
        -1521520070,
        -5587175,
        -77751101,
        -2094365853,
        -1243052806,
        1579901135,
        1321810770,
        456816404,
        -1391643889,
        -229302305,
        330002838,
        -788960546,
        363569021,
        -1947871109
    ],
    "zb": [
        20,
        223,
        245,
        7,
        248,
        2,
        194,
        209,
        87,
        6,
        227,
        253,
        240,
        128,
        222,
        91,
        237,
        9,
        125,
        157,
        230,
        93,
        252,
        205,
        90,
        79,
        144,
        199,
        159,
        197,
        186,
        167,
        39,
        37,
        156,
        198,
        38,
        42,
        43,
        168,
        217,
        153,
        15,
        103,
        80,
        189,
        71,
        191,
        97,
        84,
        247,
        95,
        36,
        69,
        14,
        35,
        12,
        171,
        28,
        114,
        178,
        148,
        86,
        182,
        32,
        83,
        158,
        109,
        22,
        255,
        94,
        238,
        151,
        85,
        77,
        124,
        254,
        18,
        4,
        26,
        123,
        176,
        232,
        193,
        131,
        172,
        143,
        142,
        150,
        30,
        10,
        146,
        162,
        62,
        224,
        218,
        196,
        229,
        1,
        192,
        213,
        27,
        110,
        56,
        231,
        180,
        138,
        107,
        242,
        187,
        54,
        120,
        19,
        44,
        117,
        228,
        215,
        203,
        53,
        239,
        251,
        127,
        81,
        11,
        133,
        96,
        204,
        132,
        41,
        115,
        73,
        55,
        249,
        147,
        102,
        48,
        122,
        145,
        106,
        118,
        74,
        190,
        29,
        16,
        174,
        5,
        177,
        129,
        63,
        113,
        99,
        31,
        161,
        76,
        246,
        34,
        211,
        13,
        60,
        68,
        207,
        160,
        65,
        111,
        82,
        165,
        67,
        169,
        225,
        57,
        112,
        244,
        155,
        51,
        236,
        200,
        233,
        58,
        61,
        47,
        100,
        137,
        185,
        64,
        17,
        70,
        234,
        163,
        219,
        108,
        170,
        166,
        59,
        149,
        52,
        105,
        24,
        212,
        78,
        173,
        45,
        0,
        116,
        226,
        119,
        136,
        206,
        135,
        175,
        195,
        25,
        92,
        121,
        208,
        126,
        139,
        3,
        75,
        141,
        21,
        130,
        98,
        241,
        40,
        154,
        66,
        184,
        49,
        181,
        46,
        243,
        88,
        101,
        183,
        8,
        23,
        72,
        188,
        104,
        179,
        210,
        134,
        250,
        201,
        164,
        89,
        216,
        202,
        220,
        50,
        221,
        152,
        140,
        33,
        235,
        214
    ],
    "zm": [
        120,
        50,
        98,
        101,
        99,
        98,
        119,
        100,
        103,
        107,
        99,
        119,
        97,
        99,
        110,
        111
    ]
}

function B(tt, te) {
    return (255 & tt[te]) << 24 | (255 & tt[te + 1]) << 16 | (255 & tt[te + 2]) << 8 | 255 & tt[te + 3]
}

function i(tt, te, tr) {
    te[tr] = 255 & tt >>> 24,
        te[tr + 1] = 255 & tt >>> 16,
        te[tr + 2] = 255 & tt >>> 8,
        te[tr + 3] = 255 & tt
}

function Q(tt, te) {
    return (4294967295 & tt) << te | tt >>> 32 - te
}

function G(tt) {
    var te = [, , , ,]
        , tr = [, , , ,];
    i(tt, te, 0),
        tr[0] = h.zb[255 & te[0]],
        tr[1] = h.zb[255 & te[1]],
        tr[2] = h.zb[255 & te[2]],
        tr[3] = h.zb[255 & te[3]];
    var ti = B(tr, 0);
    return ti ^ Q(ti, 2) ^ Q(ti, 10) ^ Q(ti, 18) ^ Q(ti, 24)
}

const __g = {
    x: function (tt, te) {
        for (var tr = [], ti = tt.length, ta = 0; 0 < ti; ti -= 16) {
            for (var tu = tt.slice(16 * ta, 16 * (ta + 1)), tc = Array(16), tf = 0; tf < 16; tf++)
                tc[tf] = tu[tf] ^ te[tf];
            te = __g.r(tc),
                tr = tr.concat(te),
                ta++
        }
        return tr
    },
    r: function (tt) {
        var te = Array(16)
            , tr = Array(36);
        tr[0] = B(tt, 0),
            tr[1] = B(tt, 4),
            tr[2] = B(tt, 8),
            tr[3] = B(tt, 12);
        for (var ti = 0; ti < 32; ti++) {
            var ta = G(tr[ti + 1] ^ tr[ti + 2] ^ tr[ti + 3] ^ h.zk[ti]);
            tr[ti + 4] = tr[ti] ^ ta
        }
        return i(tr[35], te, 0),
            i(tr[34], te, 4),
            i(tr[33], te, 8),
            i(tr[32], te, 12),
            te
    }
};

t3 = function (tt) {
    var te = new URL(tt, "https://www.zhihu.com");
    return "" + te.pathname + te.search
}
t6 = function (tt) {
    return null == tt ? "" : "string" == typeof tt ? tt : "undefined" != typeof URLSearchParams && (0,
        tc._)(tt, URLSearchParams) ? tt.toString() : tA()(tt) ? JSON.stringify(tt) : t4(tt) ? String(tt) : ""
}

t8 = function (tt, te) {
    return void 0 === te && (te = 4096),
    !!tt && t7(tt) <= te
}

const fixedStr = "6fpLRqJO8M/c3jnYxFkUVC4ZIG12SiH=5v0mXDazWBTsuw7QetbKdoPyAl+hN9rgE";

function processChunk(arr, start, end, xorValue = 58, shiftValue = 16) {
    const [a, b, c] = arr.slice(start, end).reverse();
    let step1, step2, step3, step4, step5;

    if (start === -3) {
        step1 = a ^ xorValue;
        step2 = b << 8;
        step3 = step1 | step2;
        step4 = c << shiftValue;
        step5 = step3 | step4;
    } else if (start === -6) {
        step1 = b ^ xorValue;
        step2 = step1 << 8;
        step3 = a | step2;
        step4 = c << shiftValue;
        step5 = step3 | step4;
    } else if (start === -9) {
        step1 = a >>> xorValue;
        step2 = b ^ 0;
        step3 = step2 << 8;
        step4 = a | step3;
        step5 = step4 | ((c ^ xorValue) << shiftValue);
    } else if (start === -12 || start === -24 || start === -36 || start === -48) {
        step1 = b << 8;
        step2 = a | step1;
        step3 = c << shiftValue;
        step5 = step2 | step3;
    } else if (start === -15 || start === -27 || start === -39) {
        step1 = a ^ xorValue;
        step2 = b << 8;
        step3 = step1 | step2;
        step4 = c << shiftValue;
        step5 = step3 | step4;
    } else if (start === -18 || start === -30 || start === -42) {
        step1 = b ^ xorValue;
        step2 = step1 << 8;
        step3 = a | step2;
        step4 = c << shiftValue;
        step5 = step3 | step4;
    } else if (start === -21 || start === -33 || start === -45) {
        step1 = b << 8;
        step2 = a | step1;
        step3 = c ^ xorValue;
        step4 = step3 << shiftValue;
        step5 = step2 | step4;
    }

    const step6 = step5 & 63;
    const step7 = step5 >>> 6 & 63;
    const step8 = step5 >>> 12 & 63;
    const step9 = step5 >>> 18 & 63;

    return [
        fixedStr.charAt(step6),
        fixedStr.charAt(step7),
        fixedStr.charAt(step8),
        fixedStr.charAt(step9)
    ].join('');
}

function encrypt(tt, cookie, x_81) {
    const chunkConfigs = [
        {start: -3, end: undefined},
        {start: -6, end: -3},
        {start: -9, end: -6},
        {start: -12, end: -9},
        {start: -15, end: -12},
        {start: -18, end: -15},
        {start: -21, end: -18},
        {start: -24, end: -21},
        {start: -27, end: -24},
        {start: -30, end: -27},
        {start: -33, end: -30},
        {start: -36, end: -33},
        {start: -39, end: -36},
        {start: -42, end: -39},
        {start: -45, end: -42},
        {start: -48, end: -45}
    ];
    var ta = "101_3_3.0"
        , tu = cookie
        , tc = x_81
        , tf = t3(tt)
        , td = t6(undefined)
        , tp = [ta, tf, tu, t8(td) && td, tc].filter(Boolean).join("+");
    const md5Str = CryptoJS.MD5(tp).toString();
    const charCodes = [
        Math.ceil(Math.random() * 127), 0,
        ...Array.from(md5Str).map(c => c.charCodeAt(0)),
        14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14
    ];

    const last_32 = charCodes.slice(-32);
    const arr_1 = charCodes.slice(0, 16)
    const base_arr = [48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
    const XOR_16 = arr_1.map((value, index) => value ^ base_arr[index] ^ 42)
    const before_16 = __g.r(XOR_16);
    const result_arr = __g.x(last_32, before_16);
    const concat_arr = before_16.concat(result_arr);
    const results = chunkConfigs.map(config => {
        return processChunk(concat_arr, config.start, config.end);
    });

    var x_96 = ''
    results.forEach((result, index) => {
        x_96 += result;
    });
    return "2.0_" + x_96;
}

// console.log(encrypt("/api/v4/answers/3485430733/relationship?desktop=true", "ATASvLqKZhmPTouuveYJW_-taxM3otMGGVI=|1729158200"));
