keyword = ["200w苦战无人岛困难版.map", "小岛登陆战.map", 
"小岛登陆战2.0.map", "苦战无人岛路人版.map", "解放战争正式版.map", "塔防", "pve"]
x=["塔防qwE", "Pve快来"]

def check_word(string, word):
    return string.find(word) != -1

for index in range(len(keyword)):
    x[1]=x[1].lower()
    if (check_word(x[1], keyword[index])):
        print("find")
    else: 
        print("not find")
