// document.addEventListener("DOMContentLoaded", () => {
//     getUserName()
// })

const searchMemberInfo = document.querySelector("#search-member-info")
searchMemberInfo.addEventListener("submit",(e)=>{
    e.preventDefault()
    searchMember()
})

const reviseName = document.querySelector("#revise-name")
reviseName.addEventListener("submit", (e)=>{
    e.preventDefault()
    reviseUserName()
})

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
            window.location.href = "/"  // 返回首頁
        } else {
            alert(result.msg || "登出失敗")
        }
        
    } catch (error) {
        console.error("登出出錯:", error)
        alert(`錯誤: ${error.message || "網路連線失敗，請稍後重試"}`)
    }
}

// 抓目前登入的使用者名稱並顯示於頁面
async function getUserName() {
    try {
        const userName = document.querySelector("#user_name")
        const response = await fetch("/api/member/current-user",{method: "GET"})
        if (!response.ok){
            throw new Error (`伺服器錯誤: ${response.status}`)
        }
        let result
        try{
            result = await response.json()
            //僅在開發時確認用 console.log(result)
        } catch(e) {
            throw new Error("伺服器返回了無效的 JSON")
        }
        if (result.ok){
            userName.textContent = result.username
        }
    }catch(error){
        console.error("找不到用戶名稱:", error)
    }
}
getUserName()

// 連接查詢使用者的 API
async function searchMember() {
    try{
        const id = document.querySelector("#member-id").value.trim()
        const response = await fetch(`/api/member/${id}`,{method: "GET"})
        if (!response.ok){
            throw new Error (`伺服器錯誤: ${response.status}`)
        }
        let result
        try{
            result = await response.json()
            //console.log(result)
        } catch(e) {
            throw new Error("伺服器返回了無效的 JSON")
        }
        const showResult = document.querySelector("#search-result")
        if (result.data){
            document.querySelector("#member-id").value = ""
            showResult.textContent = `ID ${id}：${result.data.name} (${result.data.email})`
        }else{
            showResult.textContent = "查詢不到相關資訊"
        }
    }catch(error){
        console.error("查詢失敗:", error)
    }
}

async function reviseUserName(){
    try {
        const newName = document.querySelector("#new-name").value.trim()
        // 基本格式檢查（未來可以自己新增更多檢查條件）
        if (newName.length > 10){
            alert("使用者名稱不能超過10個字元")
            return
        }

        if (!confirm(`確認要更新名稱為 ${newName} 嗎？`)) {
            return
        }

        const response = await fetch("/api/member",{
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"name": newName})
        })

        const revisedResult = document.querySelector("#revised-result")
        if (!response.ok){
            revisedResult.textContent = "操作失敗QQ，名稱未更新"
            throw new Error(`伺服器錯誤: ${response.status}`)
        }
        let result
        try{
            result = await response.json()
        } catch (e) {
            throw new Error("伺服器返回了無效的 JSON")
        }

        if (result.ok){
            document.querySelector("#new-name").value = ""
            revisedResult.textContent = "更新成功！"
            getUserName() // 重新去session內抓新名稱渲染到頁面
        }else{
            revisedResult.textContent = "操作失敗QQ，名稱未更新"
            alert(result.msg)
        }
    }catch (error){
        console.error("操作失敗:", error)
    }
}

// 更新查詢紀錄
async function getHistory(){
    try {
        const response = await fetch("/api/search_history", {method:"GET"})
        if (!response.ok){
            throw new Error(`伺服器錯誤: ${response.status}`)
        }
        let result
        try{
            result = await response.json()
        }catch(e){
            throw new Error("伺服器返回了無效的 JSON")
        }
        if (!result.data||result.data.length === 0){
            document.querySelector("#history-container").textContent = "沒有查詢紀錄";
            return;
        }
        const container = document.querySelector("#history-container")
        container.innerHTML = result.data.map(item => {
            const displayTime = item.time.split("T").join(" ")
            return `
                <div class="history-item">
                    <p>${item.name} 於 ${displayTime} 查詢了你</p>
                </div>`
        }).join("")
    }catch(error){
        console.error("載入搜尋紀錄失敗:", error)
        document.querySelector("#history-container").textContent = "載入失敗"
    }
}