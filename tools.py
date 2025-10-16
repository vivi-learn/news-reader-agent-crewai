import time
from crewai.tools import tool  # 크루에이아이의 툴 데코레이터
from crewai_tools import SerperDevTool  # 구글 검색을 위한 라이브러리
from playwright.sync_api import sync_playwright  # 웹 스크래핑을 위한 라이브러리
from bs4 import BeautifulSoup  # html 파싱을 위한 라이브러리


# 구글 검색 툴 설정
search_tool = SerperDevTool(
    n_results=5, # 검색 결과 수
)


@tool
def scrape_tool(url: str):
    """
    Use this when you need to read the content of a website.
    Returns the content of a website, in case the website is not available, it returns 'No content'.
    Input should be a `url` string. for example (https://www.reuters.com/world/asia-pacific/cambodia-thailand-begin-talks-malaysia-amid-fragile-ceasefire-2025-08-04/)
    """

    print(f"Scrapping URL: {url}")

    # Using Playwright to fetch the page content
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        # Open a new page
        page = browser.new_page()
        # Navigate to the URL
        page.goto(url)
        # Wait for the page to load completely
        time.sleep(5)
        # Get the page content
        html = page.content()
        # Close the browser
        browser.close()
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # Remove unwanted tags and their content
        unwanted_tags = [
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
            "iframe",
            "form",
            "button",
            "input",
            "select",
            "textarea",
            "img",
            "svg",
            "canvas",
            "audio",
            "video",
            "embed",
            "object",
        ]
        # Decompose unwanted tags
        for tag in soup.find_all(unwanted_tags):
            tag.decompose()
        # Extract and return the text content
        content = soup.get_text(separator=" ")
        # Clean up the content by removing extra whitespace
        return content if content != "" else "No content"