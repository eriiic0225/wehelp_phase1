// 連接登出 API
async function logout(){
    let response = await fetch("/logout",{method:"GET"})
    let result = await response.json()
    console.log(result)
}

// 送出留言事件監聽
const sending = document.querySelector(".leave-message")
sending.addEventListener("submit", (e) => {
    e.preventDefault()
    comment()
    })

// 送出留言 API
async function comment() {
    const content = document.querySelector("#message").value
    let response = await fetch(
        "/createMessage",
        {
            method: "POST",
            body: JSON.stringify({"content": content})
        }
    )
    let result = await response.json()
    if (result.ok) {
        location.reload()
        // window.location.assign("/member")
    }
}

// 刪除留言的onclick func ＆ 彈出式確認視窗
async function deleteMessage(id) {
    // confirm("確認刪除此留言嗎？")
    if (confirm("確認刪除此留言嗎？") == true){
        let response = await fetch(
            "/deleteMessage",
            {method: "POST", body: JSON.stringify({"id": id})}
        )
        let result = await response.json()
        if (result.ok) location.reload()
    }
}