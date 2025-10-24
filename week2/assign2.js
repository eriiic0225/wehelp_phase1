// task 1
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

//算原距離，參數必須是座標陣列
function disCount([x,y]){
    let result = []
    for (let i=0; i < location.length; i++){
        result.push(Math.abs(x-location[i][0])+Math.abs(y-location[i][1]))
    }
    return result
}

//求最終距離，參數是布林值
function sameSide(boolean, arr){
    for (let i=0; i<leftRight.length; i++){
        if (boolean !== leftRight[i]){
            arr[i] += 2 
        }
    }
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
    let side = leftRight[num] //布林值，看本輪是在斜線哪一側
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

// task 2
let occupied = {
    "S1" : [],
    "S2" : [],
    "S3" : [],
}

function checkTime(name, start, end){
    const schedule = occupied[name];
    for (let i=0; i < schedule.length; i++){
        const [min, max] = schedule[i]
        if (start <= max && end >= min){
            return false
        }        
    }
    return true
}

function func2(ss, start, end, criteria){
    const operator = [">=", "<=", "="]
    let factor, range, opUsed;
    for (const op of operator){
        if (criteria.includes(op)){
            [factor, range] = criteria.split(op)
            opUsed = op
            break
        }
    }
    // console.log(factor, range, opUsed)
    if (range === "name"){
        const name = range
        if (checkTime(name, start, end)){
            occupied[name].push([start, end])
            console.log(name)
        }else{
            console.log("Sorry")
        }
        return
    }

    range = parseFloat(range)
    let bestFit = null
    
    if (opUsed === ">="){
        let bestVal = Infinity
        for (let i=0; i < ss.length; i++){
            const s = ss[i]
            const val = s[factor]
            if (val >= range && checkTime(s.name, start, end)){
                if (val < bestVal){
                    bestVal = val
                    bestFit = s.name
                }
            }
        }
    }else if (opUsed === "<="){
        let bestVal = -Infinity
        for (let i=0; i < ss.length; i++){
            const s = ss[i]
            const val = s[factor]
            if (val <= range && checkTime(s.name, start, end)){
                if (val > bestVal){
                    bestVal = val
                    bestFit = s.name
                }
            }
        }
    }

    if (bestFit){
        occupied[bestFit].push([start, end])
        console.log(bestFit)
    }else{
        console.log("Sorry")
    }

}//func2 main

const services=[
{"name":"S1", "r":4.5, "c":1000},
{"name":"S2", "r":3, "c":1200},
{"name":"S3", "r":3.8, "c":800}
];
func2(services, 15, 17, "c>=800"); // S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2

// task 3
function func3(index){
    const base = [25, 23, 20, 21]
    const startPoint = base[(index%4)]
    const result = startPoint - 2*Math.floor(index/4)
    console.log(result)
}
func3(1); // print 23
func3(5); // print 21
func3(10); // print 16
func3(30); // print 6

// task 4
function checkAvailable(arr, condition){
        for (let i in arr){
            if (condition[i] === '1'){
                arr[i] = 0
            }
        }
        return arr
    }

function func4(sp, stat, n){
    const statArr = Array.from(stat)
    const empty = checkAvailable(sp, statArr)
    //console.log("確認可用狀況", empty)
    let base = Infinity
    let result = -1
    for (let i=0; i < empty.length; i++){
        const v = empty[i]
        if (v === 0) continue
        const d = Math.abs(v - n)
        if (d < base){
            base = d
            result = i
        } 
    }
    console.log(result)
}
func4([3, 1, 5, 4, 3, 2], "101000", 2); // print 5
func4([1, 0, 5, 1, 3], "10100", 4); // print 4
func4([4, 6, 5, 8], "1000", 4); // print 2