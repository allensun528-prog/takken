document.addEventListener("DOMContentLoaded", () => {

    const checkboxes = document.querySelectorAll(
        'input[type="checkbox"]'
    );

    checkboxes.forEach((checkbox, index) => {

        const key = "takken_checkbox_" + index;

        // 恢复之前的状态
        const saved = localStorage.getItem(key);

        if (saved !== null) {
            checkbox.checked = saved === "true";
        }

        // 勾选时保存
        checkbox.addEventListener("change", () => {
            localStorage.setItem(
                key,
                checkbox.checked
            );
        });

    });

});