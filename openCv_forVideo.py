from selenium import webdriver
import time
import os
import requests
import urllib
from bs4 import BeautifulSoup
import cv2
from PIL import Image

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

def downInDesktop(fileFolderName,urlList):
    src = GetDesktopPath()+'/'+fileFolderName
    mkdir(src)
    print('开始下载')
    # print(urlList)
    for x in range(len(urlList)):
        clearShell()
        print('（0/3）下载进度   :   '+str(x/len(urlList)*100)+'%')
        noobSrc =urlList[x].split('/')[len(urlList[x].split('/'))-1].split('.')
        try:
            down(urlList[x],src+'/'+noobSrc[0]+'.'+noobSrc[1])
        except:
            print('Warning:down fail')
    print('结束下载')

def down(url,src):
    urllib.request.urlretrieve(url,src)

# down('http://img.soogif.com/c8Qlxig7tPc6IDWcDcgiffiwHPp8BIxV.mp4',GetDesktopPath()+'/an.mp4')

def clearShell():
    os.system('cls')



def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def get(url,className):
    re = requests.get(url)
    re.encoding = 'utf-8'
    soup = BeautifulSoup(re.text,'lxml')
    arr = soup.select(className)
    return arr

def PrintList(List):
    for x in range(len(List)):
        print(str(x)+'||'+List[x])

def OpenUrlInChrome(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def UseJsInChrome(driver,js):
    try:
        driver.execute_script(js)
    except:
        print('Warning')

def GetSoupByChromeDriver(driver):
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    return soup

def MadeVideoByVideo(VideoSrcList):
    return 0

def getUrlText(text):
    return text.split('src="')[1].split('" alt="')[0]


# 视频处理

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        print('filelistMaker:'+dir)
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            if s == '.DS_Store':
                continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

# List1 = []
# LIst = GetFileList(GetDesktopPath()+'/'+'video/',List1)
# PrintList(List)

class VideoMode():
    def __init__(self,motherPath):
        import cv2
        import os
        from PIL import Image
        self.fps = 30
        self.count = 30
        self.ImageList = []
        self.motherPath = motherPath
        self.video = ''
        self.width = 640
        self.height = 480

    def start(self):
        list = self.unCodeVideo()
        deletelist = self.resizeImage(list)
        self.makeVideo(list)
        print(list)
        self.deleteMaker(deletelist)
        print("delete1")
        for x in deletelist:
            print('有意思',x)
        # self.CEF(self.motherPath)
        print('结束')

    def CEF(self,path):
        """
        CLean empty files, 清理空文件夹和空文件
        :param path: 文件路径，检查此文件路径下的子文件
        :return: None
        """
        print(path)
        files = os.listdir(path)  # 获取路径下的子文件(夹)列表
        for file in files:
            clearShell()
            print('Traversal at  :  '+file)
            if os.path.isdir(path+'/'+file):  # 如果是文件夹
                if os.path.isdir(path+'/'+file):  # 如果子文件为空
                    os.rmdir(path+'/'+file)  # 删除这个空文件夹
                    print('Traversal at  :  ' + file+' | \ 删除成功 \ | ')
            elif os.path.isfile(path+'/'+file):  # 如果是文件
                if os.path.getsize(path+'/'+file) == 0:  # 文件大小为0
                    os.remove(path+'/'+file)  # 删除这个文件
        print(path+' Dispose over!')

    def deleteMaker(self,pathList):
        for x in pathList:
            try:
                os.remove(x)
            except:
                print('Warning:delete false')

    def del_file(self,path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)

    def unCodeVideo(self):
        List = GetFileList(self.motherPath,[])
        list1 = []
        for x in range(len(List)):
            clearShell()
            print('（0/3）下载进度   :   100%')
            print('（1/3）视频拆分   :   '+str(x+1)+'/'+str(len(List)))
            print('pathuncode'+List[x])
            self.getVideo(List[x].split('\\')[len(List[x].split('\\'))-1])
            list1.append(List[x].split('.')[0]+'/')
        print("视频切片完成")
        self.deleteMaker(List)
        return list1

    def resizeImage(self,srcList):
        item = []
        for x in srcList:
            APP = GetFileList(x,[])
            for z in range(len(APP)):
                item.append(x+str(z+1)+'.jpg')
        for x in range(len(item)):
            clearShell()
            print('（0/3）下载进度   :   100%')
            print('（1/3）视频拆分   :   100%')
            print('（2/3）图片转换   :   '+str(x/len(item)*100)+' %')
            img = Image.open(item[x])
            out = img.resize((self.width,self.height),Image.ANTIALIAS)
            out.save(item[x].split('.')[0]+'.jpeg','jpeg')
        self.deleteMaker(item)
        for x in range(len(item)):
            item[x] = item[x].split('.')[0]+'.jpeg'
        return item

    def getVideo(self,filename):
        filename = filename
        path = self.motherPath + '/' + filename.split('.')[0] + '/'
        videoCapture = cv2.VideoCapture(self.motherPath+'/'+filename)
        step = 0
        i=0
        print(videoCapture.read())
        key,frame = videoCapture.read()
        if key:
            mkdir(path)
        else:
            return False
        while(True):
            i = 1 + i
            videoCapture.set(1,i)
            key, frame = videoCapture.read()
            if key!=True:
                break
            cv2.imwrite(path+str(i)+'.jpg',frame)


    def makeVideo(self,srcList):
        print('222')
        fps = 24  # 视频每秒24帧
        size = (self.width, self.height)  # 需要转为视频的图片的尺寸
        video = cv2.VideoWriter(self.motherPath+"/Output_video.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'),fps,size)
        item = []
        for x in srcList:
            APP = GetFileList(x,[])
            for z in range(len(APP)):
                item.append(x+str(z+1)+'.jpeg')
        for x in range(len(item)):
            clearShell()
            print('（0/3）下载进度   :   100%')
            print('（1/3）视频拆分   :   100%')
            print('（2/3）图片转换   :   100%')
            print("（3/3）视频生成进度："+str(x/len(item)*100)+' %')
            img = cv2.imread(item[x])
            video.write(img)
        video.release()
        cv2.destroyAllWindows()


# 测试

# vc = VideoMode(GetDesktopPath()+'/video')
# list1 = vc.unCodeVideo()
# PrintList(list1)
# vc.resizeImage(list1)
# vc.makeVideo(list1)

# 测试


# 视频处理







# 多线程
import threading
class Thread():
    def __init__(self):
        self.Keys = 2

    def start_a(self):
        return 0

# 多线程






# 主函数


def Main():
    longKey = int(input("视频长度>"))
    nameKey = str(input("文件夹名称>"))
    testUrl = 'https://www.soogif.com/shareSatin'
    driver = OpenUrlInChrome(testUrl)
    for x in range(longKey):
        print(x)
        time.sleep(1)
        UseJsInChrome(driver,'window.scrollTo(0,100000)')
    time.sleep(3)
    soup = GetSoupByChromeDriver(driver)
    # print(soup)
    videoList = soup.select('img.lazy')
    print(videoList)

    UrlList = []
    for x in videoList:
        UrlList.append(x.get('data-original'))
    PrintList(UrlList)
    downInDesktop(nameKey,UrlList)
    vc = VideoMode(GetDesktopPath()+'/'+nameKey)
    vc.start()

Main()




# #
# def try1():
#     url = "https://www.soogif.com/shareSatin"
#     re = requests.get(url)
#     soup = BeautifulSoup(re.text,'lxml')
#     print(soup.select('img'))
#
#
# try1()




#
















