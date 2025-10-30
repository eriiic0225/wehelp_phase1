/* week 1 範圍 */
// const burger = document.querySelector("#button");
// const menu = document.querySelector(".menu");
// const X = document.querySelector(".closeButton");

// burger.addEventListener("click", () => {
//     menu.classList.toggle("active");
// })

// X.addEventListener("click", () => {
//     menu.classList.toggle("active");
// })

/* week 3 範圍 */
const informationURL = "https://cwpeng.github.io/test/assignment-3-1"
const photoURL = "https://cwpeng.github.io/test/assignment-3-2"

async function fetchJSON(url){
    const response = await fetch(url)
    if (!response.ok){
        throw new Error('HTTP'+response.status)
    }
    return response.json()
}

async function init(){
    const [info, photos] = await Promise.all([
        fetchJSON(informationURL),
        fetchJSON(photoURL)
    ])

    const cleanInfo = info.rows.map(({ serial, sname }) => ({ serial, name: sname }))
    //console.log(cleanInfo)
    const regex = /^\/d_upload_ttn\/sceneadmin\/(pic|image)\/(\d{8}|.{58,60})\.jpg/
    const host = "https://www.travel.taipei"
    const cleanPhotos = photos.rows.map(({serial, pics}) => ({serial, url: host+pics.match(regex)[0]}))
    //console.log(cleanPhotos)
    const urlBySerial = {}
    for (const item of cleanPhotos){
        const serial = item.serial
        const url = item.url
        urlBySerial[serial] = url
    }
    //console.log(urlBySerial)

    const merge = cleanInfo.map(infoItem => {
        const name = infoItem.name
        const serial = infoItem.serial
        const url = urlBySerial[serial]
        return {name, url}
    })
    //console.log(store.merge)
    return merge
}

const loadingData = init()

document.addEventListener('DOMContentLoaded', async () => {
    try{
        const merged = await loadingData
        console.log(merged)
        //TODO: 之後在這裡跑寫好的渲染用function
        renderPromo(merged)
        renderCards(merged)
    }
    catch(error){
        console.error(error)
    }
})

function renderPromo(arr){
    const bars = document.getElementById("bars")

    arr.slice(0,3).forEach(item => {
        const frame = document.createElement("div")
        frame.className = "promoFrame"
        const promoPic = document.createElement("img")
        promoPic.className = "promoPic"
        promoPic.src = item.url
        const promo = document.createElement("div")
        promo.className = "promo"
        promo.textContent = item.name
        frame.appendChild(promoPic)
        frame.appendChild(promo)
        bars.appendChild(frame)
    });
}

function renderCards(arr){
    const cardBox = document.getElementById("cards")

    arr.slice(3,13).forEach(item =>{
        const card = document.createElement("div")
        card.className = "card"
        const cover = document.createElement("img")
        cover.className = "cover"
        cover.src = item.url
        cover.alt = "景點照片"
        const title = document.createElement("div")
        title.className = "title"
        title.textContent = item.name
        const star = document.createElement("img")
        star.className = "star"
        star.src = "./img/star.png"
        card.appendChild(cover)
        card.appendChild(title)
        card.appendChild(star)
        cardBox.appendChild(card)
    })

}


let totalCount = 13
function loadMoreCards(arr){
    const cardBox = document.getElementById("cards")
    if (totalCount <= 52){
        arr.slice(totalCount, totalCount+10).forEach(item =>{
            const card = document.createElement("div")
            card.className = "card"
            const cover = document.createElement("img")
            cover.className = "cover"
            cover.src = item.url
            cover.alt = "景點照片"
            const title = document.createElement("div")
            title.className = "title"
            title.textContent = item.name
            const star = document.createElement("img")
            star.className = "star"
            star.src = "./img/star.png"
            card.appendChild(cover)
            card.appendChild(title)
            card.appendChild(star)
            cardBox.appendChild(card)
        })
        totalCount += 10
        console.log(totalCount)
    }else{
        arr.slice(totalCount).forEach(item =>{
            const card = document.createElement("div")
            card.className = "card"
            const cover = document.createElement("img")
            cover.className = "cover"
            cover.src = item.url
            cover.alt = "景點照片"
            const title = document.createElement("div")
            title.className = "title"
            title.textContent = item.name
            const star = document.createElement("img")
            star.className = "star"
            star.src = "./img/star.png"
            card.appendChild(cover)
            card.appendChild(title)
            card.appendChild(star)
            cardBox.appendChild(card)
        })
        //const btn = document.querySelector(".load-more")
        loadBtn.style.display = "none"
    }
}//end

const loadBtn = document.querySelector(".load-more")
loadBtn.addEventListener('click', async () => {
    try{
        const merged = await loadingData
        loadMoreCards(merged)
    }
    catch(error){
        console.error(error)
    }
})