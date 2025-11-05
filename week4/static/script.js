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
        "http://127.0.0.1:8000/login",
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
        window.location.assign("http://127.0.0.1:8000/member")
    }else{
        const message = result.msg
        window.location.assign(`http://127.0.0.1:8000/ohoh?msg=${message}`)
    }
}

const search = document.querySelector(".get-hotel")
search.addEventListener("submit", (e)=>{
    e.preventDefault()
    const id = document.querySelector("#hid").value
    if (!isPureNumber(id)){
        alert("請輸入正整數")
        return
    }
    window.location.assign(`http://127.0.0.1:8000/hotel/${id}`)
})

// 判斷使用者輸入是否為正整數
function isPureNumber(value){
    return /^\d+$/.test(value);
}

async function fetchJSON(url){
    const response = await fetch(url)
    if (!response.ok){
        throw new Error('HTTP'+response.status)
    }
    return response.json() //把抓到的資料解讀成json格式，但這邊收到的還會是promise
}