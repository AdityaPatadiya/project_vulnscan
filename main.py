from core.crawler import crawl

def main():
    target = input("Enter target URL: ").strip()
    links = crawl(target)
    print(f"\n[+] Found Links:")
    for link in links:
        print(link)

if __name__ == "__main__":
    main()

