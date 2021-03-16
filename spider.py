from selenium import webdriver
import matplotlib.pyplot as plt
from time import sleep
from progress.bar import Bar
from bs4 import BeautifulSoup
import networkx as nx





def get_all_xpath_inputs(driver , url):
    if(driver.current_url != url):
        driver.get(url)
        sleep(1)
    content = driver.find_element_by_xpath("/html").get_attribute("innerHTML")
    soup = BeautifulSoup(content , "lxml")
    inputs = soup.find_all("input" , {"type":"text"})
    xpaths = []
    for i in inputs:
        xpath = xpath_soup(i)
        xpaths.append(xpath)
    return(xpaths)

#get spath of a soup element
def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def get_hrefs( driver , main_url):
    try:
        driver.get(main_url)
        #sleep depends on internet velocity, if internet is faster sleep can be slower
        sleep(1)
        webpage_content = driver.find_element_by_xpath("/html")
        content = webpage_content.get_attribute("innerHTML")
        soup = BeautifulSoup(content , "lxml")
        elements_with_hrefs = soup.find_all("a")
        hrefs = []
        for i in elements_with_hrefs:
            link = i['href']
            try:
                if(link[0]== "/"):
                    link = main_url+link
            except:
                pass
            try:
                if((link[0]!= "h")and(link[1]!="t")and(link[2]!="t")and(link[3]!="p")):
                    link = main_url+"/"+link
            except:
                pass
            hrefs.append(link)
        return(hrefs)
    except:
        return([])

def check_list(elem , lista):
    for i in lista:
        if(elem == i["son"]):
            return(False)
    return(True)

def recursively_scrawl(driver , main_url , deph):
    start = get_hrefs(driver , main_url)
    first = []
    for i in start:
        father = main_url
        son = i
        couple = {
            "father":father,
            "son":son
        }
        first.append(couple)

    for i in range(deph-1):
        print("\n {} recursion".format(i+1))
        bar = Bar("progress..." , max=len(first))
        for num in range ( len(first)):
            bar.next()
            j = first[num]
            hrefs = get_hrefs(driver, j["son"])
            for k in hrefs:
                if(check_list(k , first)):
                    father = j
                    son = k
                    couple = {
                        "father":father,
                        "son":son
                    }
                    first.append(couple)
            #print(len(first) , i+1 )
    return(first)

def generate_graph(son_father_list):
    touples = []
    G = nx.Graph()
    for i in son_father_list:
        left = i["father"]
        right = i["son"]
        try:
            G.add_edge(left, right)
        except:
            pass
        touple = (left,right)
        touples.append(touple)

    #print(touples)
    nx.draw(G)
    plt.show()



def get_xpaths_inputs_recursiveley(driver , root_url):

    cont = recursively_scrawl(driver , root_url , 2 )
    all_xpaths = []
    for i in cont:
        try:
            xpaths = get_all_xpath_inputs(driver , i["son"])
            for j in xpaths:
                info = {
                    "url":i["son"],
                    "xpath":j
                }
                all_xpaths.append(info)
        except Exception as e:
            pass
    return(all_xpaths)


driver = webdriver.Chrome()
goal = get_xpaths_inputs_recursiveley(driver , "https://tmedweb.tulane.edu/content_open")
print(goal)

driver.close()

