
var CryptoJS = require("crypto-js");

// 增加了iv参数
function encrypt (message, key, iv) {
    var keyHex = CryptoJS.enc.Utf8.parse(key);
     var encrypted = CryptoJS.TripleDES.encrypt(message, keyHex, {
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
        iv: CryptoJS.enc.Utf8.parse("20200511")
    });
    return {
        key: keyHex,
        value: encrypted.toString()
    }
}

function decrypt (message, key) {
    var plaintext = CryptoJS.enc.Utf8.stringify(CryptoJS.TripleDES.decrypt(message, CryptoJS.enc.Utf8.parse(key), {
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
        iv: CryptoJS.enc.Utf8.parse("20200511")
    }))
    return plaintext.toString(CryptoJS.enc.Utf8)
}

// 第一部分 解密数据
b = "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"
c = "4ifDl8qGSz2rhVZG8pXykqrp"
var xx = decrypt(b, c);
console.log(xx)

// 第二部分 解密ciphertext参数，用于请求数据密文
function cipher() {
	var date = new Date();
	var timestamp = date.getTime().toString();
	var salt = random(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date
			.getMonth()).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate())
			.toString();
	var iv = year + month + day;
	var enc = encrypt(timestamp, salt, iv).toString();
	var str = salt + iv + enc;
	var ciphertext = strTobinary(str);
	return ciphertext;
}
function strTobinary(str) {
	var result = [];
	var list = str.split("");
	for (var i = 0; i < list.length; i++) {
		if (i != 0) {
			result.push(" ");
		}
		var item = list[i];
		var binaryStr = item.charCodeAt().toString(2);
		result.push(binaryStr);
	};
	return result.join("");
}

function random(size){
        	var str = "",
        	arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        	for(var i=0; i<size; i++){
        		str += arr[Math.round(Math.random() * (arr.length-1))];
        	}
        	return str;
        }

console.log(cipher())