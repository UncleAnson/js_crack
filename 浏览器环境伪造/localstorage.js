localStorage = {
    removeItem: function (key) {
        delete this[key]
    },
    getItem: function (key) {
        return this[key] ? this[key]: null;
    },
    setItem: function (key, value) {
        this[key] = "" + value;  // 将数字转为字符串
    },
};


console.log(localStorage)
localStorage.setItem("abc", 123)
console.log(localStorage)