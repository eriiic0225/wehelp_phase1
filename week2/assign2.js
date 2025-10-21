const position = {
    "悟空": [0, 0],
    "丁滿": [-1, 4],
    "辛巴": [-3, 3],
    "貝吉塔":[-4, -1],
    "弗利沙":[4, -1],
    "特南克斯":[1, -2]
}

const nameList = Object.keys(position)
const location = Object.values(position)
const information = Object.entries(position)
const leftRight = location.map(([x, y]) => 5 * x + 4 * y < 7)


//求最終距離，參數是布林值
function sameSide(boolean, arr){
    for (let i=0; i<leftRight.length; i++){
        if (boolean !== leftRight[i]){
            arr[i] += 2 
        }
    }
}

//參數必須是座標陣列
function disCount([x,y]){
    let result = []
    for (let i=0; i < location.length; i++){
        result.push(Math.abs(x-location[i][0])+Math.abs(y-location[i][1]))
    }
    return result
}

//找陣列中重複的數字的index
function moreThanOne(number, arr){
    let allIndex = []
    arr.forEach((x, index) => {  
        if (x === number){
            allIndex.push(index)
        }
    });
    return allIndex
}

//字串配索引拼接
function textCombine(arr, arr2, str){
    for(let i=0; i < arr.length; i++){
        str += `${arr2[arr[i]]}、`
    }
    return str
}


function func1(name){
    let num = nameList.indexOf(name)
    let distance = disCount(location[num]) //未計算跨線前的距離
    let side = leftRight[num] //看本輪是在斜線哪一側
    let farCount = -Infinity//比較用的數字
    let nearCount = Infinity
    sameSide(side, distance) //理想中這時包含跨線的距離已經算完了，distance成為新數據
    for (let i=0; i<distance.length; i++){ 
        if (distance[i] == 0) continue
        if (distance[i] > farCount){
            farCount = distance[i]
        }
        if (distance[i] < nearCount){
            nearCount = distance[i]
        }
    }
    let finalText = `最遠`
    let farIndex = moreThanOne(farCount, distance) //記錄所有最遠的索引
    let nearIndex = moreThanOne(nearCount, distance) //記錄所有最近的索引
    finalText = textCombine(farIndex, nameList, finalText).slice(0, -1)
    finalText += ` ; 最近`
    finalText = textCombine(nearIndex, nameList, finalText).slice(0, -1)
    console.log(finalText)
}



func1("辛巴"); // print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空"); // print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙"); // print 最遠辛巴，最近特南克斯
func1("特南克斯"); // print 最遠丁滿，最近悟空