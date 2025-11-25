// 連接登出 API
async function logout(){
    try {
        // ============ 第 1 步：確認登出 ============
        if (!confirm("確認要登出嗎？")) {
            return
        }
        
        // ============ 第 2 步：發送請求 ============
        const response = await fetch("/logout", {
            method: "GET"
        })
        
        // 檢查 HTTP 狀態碼
        if (!response.ok) {
            throw new Error(`伺服器錯誤: ${response.status}`)
        }
        
        // ============ 第 3 步：解析 JSON ============
        let result
        try {
            result = await response.json()
        } catch (e) {
            throw new Error("伺服器返回了無效的 JSON")
        }
        
        // ============ 第 4 步：處理結果 ============
        if (result.ok) {
            alert(result.msg || "已登出")
            window.location.assign("/")  // 返回首頁
        } else {
            alert(result.msg || "登出失敗")
        }
        
    } catch (error) {
        console.error("登出出錯:", error)
        alert(`錯誤: ${error.message || "網路連線失敗，請稍後重試"}`)
    }
}

// 送出留言事件監聽
const sending = document.querySelector(".leave-message")
sending.addEventListener("submit", (e) => {
    e.preventDefault()
    comment()
    })

// 送出留言 API
async function comment() {
    try{
        // ============ 第 1 步：驗證輸入 ============
        const messageInput = document.querySelector("#message")
        if (!messageInput){
            alert("找不到留言輸入框")
            return
        }
        
        const content = document.querySelector("#message").value.trim()

        if (!content){
            alert("留言不能為空")
            return
        }

        if (content.length > 200){
            alert("留言內容不能超過 200 字")
            return
        }

        // ============ 第 2 步：發送請求 ============
        const response = await fetch(
            "/createMessage",
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"content": content})
            })
        
        // 檢查 HTTP 狀態碼
        if (!response.ok){
            throw new Error(`伺服器錯誤: ${response.status}`)
        }

        // ============ 第 3 步：解析 JSON ============
        let result
        try{
            result = await response.json()
        }catch(e){
            throw new Error("伺服器返回了無效的 JSON")
        }
        if (result.ok){
            alert(result.msg || "留言已發布")
            messageInput.value = ""  // 清空輸入框
            location.reload()
        }else{
            alert(result.msg || "留言發布失敗")
        }

    } catch (error){
        console.error("發送留言出錯:", error)
        alert(`錯誤: ${error.message || "網路連線失敗，請稍後重試"}`)
    }
}


// 刪除留言的onclick func ＆ 彈出式確認視窗
async function deleteMessage(id) {
    try {
        // ============ 第 1 步：驗證參數 ============
        if (!id) {
            alert("留言 ID 不能為空")
            return
        }
        
        // ============ 第 2 步：確認刪除 ============
        if (!confirm("確認要刪除此留言嗎？")) {
            return  // 使用者取消
        }
        
        // ============ 第 3 步：發送請求 ============
        const response = await fetch("/deleteMessage", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "id": id
            })
        })
        
        // 檢查 HTTP 狀態碼
        if (!response.ok) {
            throw new Error(`伺服器錯誤: ${response.status}`)
        }
        
        // ============ 第 4 步：解析 JSON ============
        let result
        try {
            result = await response.json()
        } catch (e) {
            throw new Error("伺服器返回了無效的 JSON")
        }
        
        // ============ 第 5 步：處理結果 ============
        if (result.ok) {
            alert(result.msg || "留言已刪除")
            location.reload()
        } else {
            alert(result.msg || "刪除失敗")
        }
        
    } catch (error) {
        console.error("刪除留言出錯:", error)
        alert(`錯誤: ${error.message || "網路連線失敗，請稍後重試"}`)
    }
}