/* week 1 範圍 */
const burger = document.querySelector("#button");
const menu = document.querySelector(".nav-menu");
const X = document.querySelector(".closeButton");

burger.addEventListener("click", () => {
    menu.classList.toggle("open");
    X.classList.toggle("active")
})

X.addEventListener("click", () => {
    menu.classList.toggle("open");
    X.classList.toggle("active")
})

/* week 3 範圍 */
const informationURL = "https://cwpeng.github.io/test/assignment-3-1"
const photoURL = "https://cwpeng.github.io/test/assignment-3-2"

//抓JSON小函式
async function fetchJSON(url){
    const response = await fetch(url)
    if (!response.ok){
        throw new Error('HTTP'+response.status)
    }
    return response.json() //把抓到的資料解讀成json格式，但這邊收到的還會是promise
}

// 抓完JSON後整理 - 因為要處理的資料還是promise，所以這邊以 async 函式操作
async function init(){
    const [info, photos] = await Promise.all([
        fetchJSON(informationURL),
        fetchJSON(photoURL)
    ])//載入全部的JSON promise並await，同時利用解構分別賦值給info ＆ photo

    const cleanInfo = info.rows.map(({ serial, sname }) => ({ serial, name: sname }))
    //console.log(cleanInfo) >> 得到的資料格式為 [{"serial": "2011051800000061", name:"新北投溫泉區"}, {"serial":.....}]
    const regex = /^\/d_upload_ttn\/sceneadmin\/(pic|image)\/(\d{8}|.{58,60})\.jpg/
    const host = "https://www.travel.taipei"
    const cleanPhotos = photos.rows.map(({serial, pics}) => ({serial, url: host+pics.match(regex)[0]}))
    //console.log(cleanPhotos) >> 得到的資料格式為 [{"serial": "2011051800000061", url: "...."},{.... }]
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
//製作card區DOM的小函式
function makeCard(item){
    const card = document.createElement("div")
    card.className = "card"
    const cover = document.createElement("img")
    cover.className = "cover"
    cover.src = item.url
    cover.alt = item.name
    cover.title = item.name
    //cover.loading = "lazy"
    const title = document.createElement("div")
    title.className = "title"
    title.textContent = item.name
    const star = document.createElement("img")
    star.className = "star"
    star.src = "./img/star.png"
    card.appendChild(cover)
    card.appendChild(title)
    card.appendChild(star)
    return card //把組合好的card整個return出去給主函式用
}


//渲染上方promotion bar區
function renderPromo(arr){
    const bars = document.getElementById("bars")
    
    arr.slice(0,3).forEach(item => {
        const frame = document.createElement("div")
        frame.className = "promoFrame"
        const promoPic = document.createElement("img")
        promoPic.className = "promoPic"
        promoPic.src = item.url
        promoPic.alt = item.name
        promoPic.title = item.name
        const promo = document.createElement("div")
        promo.className = "promo"
        promo.textContent = item.name
        frame.appendChild(promoPic)
        frame.appendChild(promo)
        bars.appendChild(frame)
    });
}

//渲染下方title card區
function renderCards(arr){
    const cardBox = document.getElementById("cards")
    
    arr.slice(3,13).forEach(item =>{
        cardBox.appendChild(makeCard(item))
    })
    
}

//load more:cue額外的10個cards
//計數器在下面，totalCount初始值設為13(前13個景點一波用掉了/總共58個)
function loadMoreCards(arr){
    const cardBox = document.getElementById("cards")
    if (totalCount <= 52){
        arr.slice(totalCount, totalCount+10).forEach(item =>{
            cardBox.appendChild(makeCard(item))
        })
        totalCount += 10
        console.log(totalCount)
    }else{
        arr.slice(totalCount).forEach(item =>{
            cardBox.appendChild(makeCard(item))
        })
        //const loadBtn = document.querySelector(".load-more")
        loadBtn.style.display = "none"
    }
}//end

/* 程式啟動區 */
const loadingData = init() //預先抓下promise
let totalCount = 13 // 計數器

document.addEventListener('DOMContentLoaded', async () => { //頁面載入後自動執行
    try{
        const merged = await loadingData // await上面的promise後才開始渲染
        console.log(merged)
        //TODO:在這裡跑寫好的渲染用function
        renderPromo(merged)
        renderCards(merged)
    }
    catch(error){
        console.error(error)
    }
})

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