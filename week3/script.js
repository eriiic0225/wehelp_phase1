// const burger = document.querySelector("#button");
// const menu = document.querySelector(".menu");
// const X = document.querySelector(".closeButton");

// burger.addEventListener("click", () => {
//     menu.classList.toggle("active");
// })

// X.addEventListener("click", () => {
//     menu.classList.toggle("active");
// })

const informationURL = "https://cwpeng.github.io/test/assignment-3-1"
const photoURL = "https://cwpeng.github.io/test/assignment-3-2"

const store = {
    information: null,
    photos: null,
    merge: null
}

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
    // store.information = info
    // store.photos = photos
    //console.log(store.information)
    //console.log(store.photos)
    // let info = store.information.rows
    // let photos = store.photos.rows

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
    console.log(urlBySerial)

    const merge = cleanInfo.map(infoItem => {
        const name = infoItem.name
        const serial = infoItem.serial
        const url = urlBySerial[serial]
        return {name, url}
    })
    store.merge = merge
    //console.log(store.merge)
    return merge
}

const loadingData = init()

document.addEventListener('DOMContentLoaded', async () => {
  const merged = await loadingData
  console.log(merged)
  //在這裡跑渲染的程式
})

// async function main1(){
//     await loading
//     let info = store.information.rows
//     let photos = store.photos.rows

//     const cleanInfo = info.map(({ serial, sname }) => ({ serial, name: sname }))
//     //console.log(cleanInfo)
//     const regex = /^\/d_upload_ttn\/sceneadmin\/(pic|image)\/(\d{8}|.{58,60})\.jpg/
//     const host = "https://www.travel.taipei"
//     const cleanPhotos = photos.map(({serial, pics}) => ({serial, url: host+pics.match(regex)[0]}))
//     //console.log(cleanPhotos)
//     const urlBySerial = {}
//     for (const item of cleanPhotos){
//         const serial = item.serial
//         const url = item.url
//         urlBySerial[serial] = url
//     }
//     console.log(urlBySerial)

//     const merge = cleanInfo.map(infoItem => {
//         const name = infoItem.name
//         const serial = infoItem.serial
//         const url = urlBySerial[serial]
//         return {name, url}
//     })
//     store.merge = merge
//     console.log(store.merge)
// }
// main1()