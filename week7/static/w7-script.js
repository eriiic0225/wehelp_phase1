const loginForm = document.querySelector("#login")
loginForm.addEventListener("submit", (e)=>{
    e.preventDefault()
    login()
})

const signUpForm = document.querySelector("#sign-up")
signUpForm.addEventListener("submit", (e)=>{
    e.preventDefault()
    signUp()
})

async function signUp() {
    try{
        // ============ 第 1 步：驗證輸入 ============
        const name = document.querySelector("#member-name").value.trim()
        const email = document.querySelector("#sign-up-email").value.toLowerCase().trim()
        const pwd = document.querySelector("#sign-up-pwd").value.trim()

        // 檢查欄位是否為空
        if (!name || !email || !pwd){
            alert("所有欄位都必須填寫")
            return
        }

        // 基本格式檢查
        if (!email.includes("@")) {
            alert("電子郵件格式不正確")
            return
        }

        // if (pwd.length < 6) {
        //     alert("密碼至少 6 個字元")
        //     return
        // }

        // ============ 第 2 步：發送請求 ============
        const response = await fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "name": name,
                "email": email,
                "password": pwd,
            })
        })

        // 檢查 HTTP 狀態碼
        if (!response.ok) {
            throw new Error(`伺服器錯誤: ${response.status}`)
        }

        // ============ 第 3 步：解析 JSON ============
        let result //先在try的外層宣告result，避免被區塊作用域影響，後續catch才拿得到
        try {
            result = await response.json()
        } catch (e) {
            throw new Error("伺服器返回了無效的 JSON")
        }

        // ============ 第 4 步：處理結果 ============
        if (result.ok) {
            alert("註冊成功!")
            document.querySelector("#sign-up").reset()
            // 清空輸入框
            document.querySelector("#member-name").value = ""
            document.querySelector("#sign-up-email").value = ""
            document.querySelector("#sign-up-pwd").value = ""
        } else {
            // 後端返回的錯誤訊息
            const message = result.msg
            window.location.assign(`/ohoh?msg=${message}`)
        }
    } catch (error) {
        console.error("註冊出錯:", error)
        alert(`錯誤: ${error.message || "網路連線失敗，請稍後重試"}`)
    }
}

async function login() {
    try{
        // ============ 第 1 步：驗證輸入 ============
        const loginEmail = document.querySelector("#email").value.trim().toLowerCase()
        const loginPassword = document.querySelector("#pwd").value.trim()

        if (!loginEmail||!loginPassword){
            alert("電子郵件和密碼不能為空")
            return
        }

        if (!loginEmail.includes("@")){
            alert("電子郵件格式不正確")
            return
        }

        // ============ 第 2 步：發送請求 ============
        const response = await fetch(
            "/login",
            {
                method:"POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body:JSON.stringify({
                    "email": loginEmail,
                    "password": loginPassword,
                })
            })

        // 檢查 HTTP 狀態碼
        if (!response.ok) {
            throw new Error(`伺服器錯誤: ${response.status}`)
        }

        // ============ 第 3 步：解析 JSON ============
        let result
        try{
            result = await response.json()
        } catch(e) {
            throw new Error("伺服器返為了無效的 JSON")
        }

        // ============ 第 4 步：處理結果 ============
        if (result.ok){
            // alert("登入成功")
            window.location.assign("/member")
        }else{
            const message = result.msg
            window.location.assign(`/ohoh?msg=${message}`)
        }

    }catch(error){
        console.error("登入出錯:", error)
        alert(`錯誤: ${error.message || "網路連線失敗，請稍後重試"}`)
    }
}