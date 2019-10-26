import requests
import pandas as pd 
from bs4 import BeautifulSoup
import expanddouban

# Movie class
class Movie():
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

# 获取电影排行函数
# top函数
def getMovieRank(category_list):
    '''
    category_list(list): 存放电影类型的list
    return：
        True: 输出内容至两个文件
            movie.csv：用于存放各个类型电影评分9-10之间在所属地区的数量
            output.txt：用于存放各类型电影排名前三的地区及占比
        False: 输出内容至文件失败
    '''
    # 创建location_list空列表
    location_list = []
    # 获取网页链接
    url = getMovieUrl('爱情', '香港')
    # 从网页上获取所有的location
    html = expanddouban.getHtml(url)
    soup = BeautifulSoup(html)
    for element in soup.find_all('ul', class_='category')[2].children:
        if element.text == '全部地区':
            continue
        location_list.append(element.text)
    # 获取电影数据，存放至数据框df
    df = pd.DataFrame(data=None, columns=['name', 'rate', 'location', 'category', 'info_link', 'cover_link'])
    index = 0
    for category in category_list:
        for location in location_list:
            # 通过类别和位置获取
            movie_list = getMovie(category, location)
            for movie in movie_list:
                df.loc[index] = [movie.name, 
                            movie.rate, 
                            movie.location, 
                            movie.category,
                            movie.info_link, 
                            movie.cover_link]
                index += 1
    # 输出dataframe至csv文件
    try:
        df.to_csv('movie.csv', encoding='utf_8_sig')
    except Exception as err:
        print('output dataframe to csv file failed for: {}'.format(err))
        return False
    
    # 计算各类型电影在不同地区的数量，并存放至dataframe文件
    df_cat = pd.DataFrame(data=None, index=location_list, columns=category_list)
    for category in category_list:
            df_cat_series = df[df['category']==category].location.value_counts()
            df_cat[category] = df_cat_series.copy()
            df_cat[category+'_占比'] = df_cat[category] / df_cat[category].sum()
    df_cat.fillna(value=0, inplace=True)

    # 存放排序数据至output.txt
    try:
        catSortFile('output.txt', df_cat, category_list)
    except Exception as err:
        print('save data to txt file failed for: {}'.format(err))
        return False

    return True

# 获取电影类型和地区对应的链接
def getMovieUrl(category, location):
    """
    catrgory: 电影类型
    location：地区
    return: a string corresponding to the URL of douban movie lists
    """
    url_head = "https://movie.douban.com/tag/#/"
    sort_type = "sort=S" # S: sort by score
    score_range = "range=9,10"
    url = url_head+"?"+sort_type+"&"+score_range+"&"+"tags="+"电影,"+category+","+location
    return url

# 获取指定类型和地区的电影的名称、评分、评分、链接等构成的对象
def getMovie(category, location):
    """
    catrgory: 电影类型
    location：地区
    return: Movie类的实例化对象构成的list
    """
    # 获取电影列表链接
    url = getMovieUrl(category, location)
    # 由链接下载html文件
    html = expanddouban.getHtml(url, loadmore=True)
    # 解析html文件
    soup = BeautifulSoup(html)
    # 创建空movie列表
    movie_list = []
    # 查找html文件中的所有item类的'a'标签
    item_list = soup.find_all('a', class_='item')
    for item in item_list:
        info_link = item.get('href')
        cover_link = item.div.img.get('src')
        name = item.p.span.text
        rate_str = item.p.find('span', class_='rate').text
        try:
            rate = float(float(rate_str))
        except Exception as err:
            print('The rate of {} is {} which is not a number'.format(title, rate_str))
        # print(name, rate, info_link, cover_link)
        m = Movie(name, rate, location, category, info_link, cover_link)
        movie_list.append(m)
    return movie_list

# 将排序后的dataframe数据框的前三名存放至txt文件
def catSortFile(filename, df_cat, category_list):
    '''
    filename: 存放数量排名信息的文件
    df_cat: 不同类别下各地区电影数量的数据框
    return：Bool，True表示存放文件成功，False：表示存放文件失败，并打印出失败原因
    '''
    with open(filename, 'w') as outfile:
        for category in category_list:
            try:
                outfile.write('{}类型电影排名前三的地区：\n'.format(category))
            except Exception as err:
                print('save file failed for {}'.format(err))
                return 0
            df_cat.sort_values(by=category, ascending=False, inplace=True)
            for i in range(len(category_list)):
                try:
                    outfile.write('{:<10s}: 数量{:<10.0f} 占比{:<10.2f}\n'\
                                  .format(df_cat.index[i], 
                                          df_cat[category][i], 
                                          df_cat[category+'_占比'][i]))
                except Exception as err:
                    print('save file failed for {}'.format(err))
                    return 0   
    return 1

def testDoubanCrawler():
    category_list = ['爱情', '科幻', '战争']
    getMovieRank(category_list)

if __name__=='__main__':
    testDoubanCrawler()