import spider as s
import argparse
from selenium import webdriver
from os import getcwd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamical testing tool for web applications")
    parser.add_argument('URL', type=str, help="Target URL")
    parser.add_argument('rec_level', type=int, nargs=1, help="Level of recursion for the url scrawler")
    parser.add_argument('paralel', type=int, nargs=1, help="Number of browsers testing at the same time")
    parser.add_argument('--show', help="Show the web browsers", nargs="?", const=True, default=False)
    parser.add_argument('--XSS', help="Test only cross site scripting attacks", nargs="?", const=True, default=False)
    parser.add_argument('--XXE', help="Test only external XML attacks", nargs="?", const=True, default=False)
    args = parser.parse_args()

    print(args.URL)
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "".join([getcwd(), "\Downloads"])}
    chromeOptions.add_experimental_option("prefs",prefs)
    if not args.show:
        chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options = chromeOptions)

    goal = s.get_xpaths_inputs_recursiveley(driver , args.URL , args.rec_level[0])
    if args.XSS and not args.XXE:
        vectors = s.get_all_xss_attacks()
    elif not args.XSS and args.XXE:
        vectors = s.get_all_xxe_attacks()
    elif not args.XSS and not args.XXE:
        vectors = s.get_all_xss_attacks() + s.get_all_xxe_attacks()
    else:
        print("--XSS and --XXE can't be used at the same time")
        exit(0)
    driver.close()
    for i in goal:
        s.parallel_test_vector( i , vectors , args.paralel[0], args.show)