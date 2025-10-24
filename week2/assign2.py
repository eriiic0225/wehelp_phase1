# task 1
position = {
    "悟空": [0, 0],
    "丁滿": [-1, 4],
    "辛巴": [-3, 3],
    "貝吉塔":[-4, -1],
    "弗利沙":[4, -1],
    "特南克斯":[1, -2]
}

def func1(name):
    baseX, baseY = position.get(name) #得到要比較的座標
    distance = {} #算未跨線前的距離
    for target, (x2,y2) in position.items():
        distance[target] = (abs(baseX - x2)+abs(baseY-y2))
    whichSide = {} #算所有人分別是哪一邊
    for who, (x, y) in position.items():
        whichSide[who] = (5 * x + 4 * y ) < 7
    #print(whichSide)
    for person, side in whichSide.items(): #把不同邊的距離+2
        if side != whichSide.get(name):
            distance[person] += 2
    #print(distance)
    far = float('-inf')
    near = float('inf')
    farName = []
    nearName = []
    for name, finalDis in distance.items():
        if finalDis == 0: continue #跳過自己
        if finalDis > far: #取遠的最大值跟人名
            far = finalDis
            farName = [name]
        elif finalDis == far: #如果碰到一樣大的就加進名單
            farName.append(name)
        if finalDis < near:
            near = finalDis
            nearName = [name]
        elif finalDis == near:
            nearName.append(name)
    #print(far, farName, near, nearName)
    symbol = "、"
    print(f"最遠{symbol.join(farName)}；最近{symbol.join(nearName)}")

func1("辛巴") # print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空") # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙") # print 最遠辛巴，最近特南克斯
func1("特南克斯") # print 最遠丁滿，最近悟空

# task 2
occupied = {"S1" : [],"S2" : [],"S3" : [],}

def checkTime(ssname, start, end):
    schedule = occupied.get(ssname)
    for time_min , time_max in schedule:
        if start <= time_max and end >= time_min:
            return False
    return True

def func2(ss, start, end, criteria):
    operators = [">=", "<=", "="]
    factor, rate, opUsed = [None, None, None]
    for op in operators:
        if op in criteria:
            factor, rate = criteria.split(op)
            opUsed = op
            break
    
    if factor == "name":
        best = rate
        if checkTime(best, start, end):
            occupied.get(best).append((start, end))
            print(best)
            return
        else:
            print("Sorry")
            return

    rate = float(rate)
    bestFit = None

    if opUsed == ">=":
        bestVal = float('inf') #基準
        for index in range(len(ss)):
            s = ss[index]
            val = s.get(factor) #每個服務的值
            if val >= rate and checkTime(s.get('name'), start, end):
                if val < bestVal: #滿足標準(val >= rate，但更接近)
                    bestVal = val
                    bestFit = s.get('name')
    elif opUsed == "<=":
        bestVal = float('-inf')
        for index in range(len(ss)):
            s = ss[index]
            val = s.get(factor)
            if val <= rate and checkTime(s.get('name'), start, end):
                if val > bestVal:
                    bestVal = val
                    bestFit = s.get('name')

    if bestFit:
        occupied.get(bestFit).append((start, end))
        print(bestFit)
    else:
        print("Sorry")

services=[
{"name":"S1", "r":4.5, "c":1000},
{"name":"S2", "r":3, "c":1200},
{"name":"S3", "r":3.8, "c":800}
]
func2(services, 15, 17, "c>=800") # S3
func2(services, 11, 13, "r<=4") # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5") # S1
func2(services, 16, 18, "r>=4") # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500") # S2
func2(services, 8, 9, "c<=1500") # S1

# task 3
def func3(index):
    base = [25, 23, 20,21]
    startPoint = base[(index%4)]
    print(startPoint - 2*(index//4))

func3(1) # print 23
func3(5) # print 21
func3(10) # print 16
func3(30) # print 6

# task 4
def checkAvailible(Li, condition): #把不能用的車廂空位數設為0
    for i, num in enumerate(Li):
        if condition[i] == "1":
            Li[i] = 0    
    return Li

def func4(sp, stat, n):
    states = list(stat) #轉換成清單
    empty = checkAvailible(sp, states) #看實際可用座位數
    base = float('inf')
    result = None
    for i, seat in enumerate(empty):
        if seat == 0: continue
        d = abs(seat - n)
        if d < base:
            base = d
            result = i
    print(result)

func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5
func4([1, 0, 5, 1, 3], "10100", 4) # print 4
func4([4, 6, 5, 8], "1000", 4) # print 2