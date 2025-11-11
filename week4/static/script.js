const check = document.querySelector(".login")
const agree = document.querySelector("#agree")
check.addEventListener("submit", (e)=>{
    e.preventDefault()
    if (!agree.checked){
        alert("請勾選同意條款")
        return
    }else{
        login()
    }
})

async function login() {
    const email = document.querySelector("#email").value
    const pwd = document.querySelector("#pwd").value
    let response = await fetch(
        "/login",
        {
            method:"POST",
            body:JSON.stringify({
                "email": email,
                "password": pwd,
            })
        }
    )
    let result = await response.json()
    if (result.ok){
        console.log(result)
        window.location.assign("/member")
    }else{
        const message = result.msg
        window.location.assign(`/ohoh?msg=${message}`)
    }
}

const searchForm = document.querySelector(".get-hotel")
searchForm.addEventListener("submit", (e)=>{
    e.preventDefault()
    const id = document.querySelector("#hid").value
    if (!isPureNumber(id)){
        alert("請輸入正整數")
        return
    }
    window.location.assign(`/hotel/${id}`)
})

// 判斷使用者輸入是否為正整數
function isPureNumber(value){
    return /^\d+$/.test(value);
}