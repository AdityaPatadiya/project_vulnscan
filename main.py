# http://testphp.vulnweb.com/

from core.crawler import crawl
from core.scanner import load_plugins, run_plugins


def main():
    target = input("Enter target URL: ").strip()
    links = crawl(target)

    print(f"\n[+] Crawled Links:")
    for link in links:
        print(link)

    plugins = load_plugins()
    run_plugins(plugins, links)

if __name__ == "__main__":
    main()
