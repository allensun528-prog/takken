// Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDygLh_xY1KhwLmjVV_HHBxlP2diRIXik8",
    authDomain: "takken-checklist.firebaseapp.com",
    databaseURL: "https://takken-checklist-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "takken-checklist",
    storageBucket: "takken-checklist.firebasestorage.app",
    messagingSenderId: "968930545116",
    appId: "1:968930545116:web:c61d3de1a7064ff1099319"
};

// 初始化 Firebase
firebase.initializeApp(firebaseConfig);

const database = firebase.database();


// ========================================
// 页面加载
// ========================================

document.addEventListener("DOMContentLoaded", function () {

    // ------------------------------------
    // 先从 Firebase 读取所有勾选状态
    // ------------------------------------

    database.ref("checked").once("value").then(function (snapshot) {

        const data = snapshot.val() || {};

        document.querySelectorAll(".item").forEach(function (item) {

            const id = item.dataset.id;
            const checkbox = item.querySelector(".item-check");
            const answer = item.querySelector(".answer");

            // 恢复勾选状态
            if (data[id] === true) {
                checkbox.checked = true;
            }

            // --------------------------------
            // 勾选 → 保存到 Firebase
            // --------------------------------

            checkbox.addEventListener("change", function () {

                database.ref("checked/" + id).set(
                    checkbox.checked
                );

            });

            // --------------------------------
            // 点击答案 → 显示 / 隐藏
            // --------------------------------

            answer.addEventListener("click", function () {
                answer.classList.toggle("show");
            });

            // --------------------------------
            // Enter / 空格显示答案
            // --------------------------------

            answer.addEventListener("keydown", function (event) {

                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {
                    event.preventDefault();
                    answer.classList.toggle("show");
                }

            });

        });

    }).catch(function (error) {

        console.error(
            "Firebase 读取失败：",
            error
        );

    });

});
