import { initializeApp } from "https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js";
import {
    getDatabase,
    ref,
    get,
    set
} from "https://www.gstatic.com/firebasejs/12.19.0/firebase-database.js";

const firebaseConfig = {
    apiKey: "AIzaSyDygLhX_y1KhwLmjVV_HHBxlP2diRIXik8",
    authDomain: "takken-checklist.firebaseapp.com",
    databaseURL: "https://takken-checklist-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "takken-checklist",
    storageBucket: "takken-checklist.firebasestorage.app",
    messagingSenderId: "968930545116",
    appId: "1:968930545116:web:c61d3de1a7064ff1099319",
    measurementId: "G-R0GXTRQB3Y"
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

document.addEventListener("DOMContentLoaded", async function () {

    // 从 Firebase 读取已经保存的勾选状态
    const snapshot = await get(ref(database, "checked"));
    const data = snapshot.exists() ? snapshot.val() : {};

    document.querySelectorAll(".item").forEach(function (item) {

        const id = item.dataset.id;
        const checkbox = item.querySelector(".item-check");
        const answer = item.querySelector(".answer");

        // 恢复勾选状态
        if (data[id] === true) {
            checkbox.checked = true;
        }

        // 勾选时保存到 Firebase
        checkbox.addEventListener("change", function () {
            set(
                ref(database, "checked/" + id),
                checkbox.checked
            );
        });

        // 点击答案显示/隐藏
        answer.addEventListener("click", function () {
            answer.classList.toggle("show");
        });

        // 键盘 Enter / Space
        answer.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                answer.classList.toggle("show");
            }
        });
    });
});
