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
    const name = document.querySelector("#member-name").value
    const email = document.querySelector("#sign-up-email").value.toLowerCase()
    const pwd = document.querySelector("#sign-up-pwd").value
    let response = await fetch(
        "/signup",
        {
            method:"POST",
            body:JSON.stringify({
                "name": name,
                "email": email,
                "password": pwd,
            })
        }
    )
    let result = await response.json()
    if (result.ok){
        alert("註冊成功!")
        document.querySelector("#sign-up").reset() //清空表單內input內容
    }else{
        const message = result.msg
        window.location.assign(`/ohoh?msg=${message}`)
    }
}

async function login() {
    const loginEmail = document.querySelector("#email").value.toLowerCase()
    const loginPassword = document.querySelector("#pwd").value
    let response = await fetch(
        "/login",
        {
            method:"POST",
            body:JSON.stringify({
                "email": loginEmail,
                "password": loginPassword,
            })
        }
    )
    let result = await response.json()
    if (result.ok){
        //console.log(result)
        window.location.assign("/member")
    }else{
        const message = result.msg
        window.location.assign(`/ohoh?msg=${message}`)
    }
}