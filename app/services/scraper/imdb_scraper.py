import re
from playwright.async_api import async_playwright

searchUrl = "https://www.imdb.com/search/title/?title_type=feature&user_rating=9,10&num_votes=50,"
async def scrape_imdb():  
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True, args=[
    "--disable-blink-features=AutomationControlled",  # hide automation
    "--disable-dev-shm-usage",  # avoid /dev/shm issues
    "--no-sandbox",             # faster startup (if safe in your env)
    "--disable-gpu",            # not needed for scraping
    "--disable-extensions",
    "--disable-infobars",
])

    context = await browser.new_context(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        java_script_enabled=True,   # needed for IMDb rendering
        bypass_csp=True,            # bypass content security policy
        ignore_https_errors=True,   # ignore SSL errors
        locale="en-US",             # consistent content
    )

    page = await context.new_page()
    await page.goto(searchUrl, wait_until="domcontentloaded", timeout=30_000)
    pages_count = 0
    done = False
    count = 0
    while True:
      divs = page.locator("li.ipc-metadata-list-summary-item")
      newCount = await divs.count()
      while newCount == count:
        newCount = await divs.count()
      count = newCount
      newMoviesCount = 50
      if count % 50 != 0:
        newMoviesCount = count % 50
      for i in range(newMoviesCount):
        n = pages_count * 50 + i
        div = divs.nth(n)
        try:
          title = div.locator("h3.ipc-title__text.ipc-title__text--reduced")
          titleText = await title.inner_text(timeout=200)
          titleText = re.sub(r"^\d+\.\s*", "", titleText)
          href = await div.locator("div.ipc-title").first.locator("a").get_attribute("href")
          match = re.search(r"/title/(tt\d+)", href)
          imdb_id = match.group(1)
        except:
          done = True
          imdb_id = None
          break
        try:
          year = int(await div.locator("span.sc-15ac7568-7.cCsint.dli-title-metadata-item").first.inner_text())
        except:
          year = None
        try:
          synopsis = await div.locator("div.ipc-html-content-inner-div").inner_text(timeout=200)
        except:
          synopsis = ""
        try:
          detailsButton = div.locator("button.ipc-icon-button")
          if await detailsButton.count() != 1:
            raise Exception("Couldn't find details button.")
          await detailsButton.first.click()
          await page.wait_for_selector('[data-testid="btp_gl"]', timeout=200)
          genresList = page.get_by_test_id("btp_gl")
          genres = await genresList.locator("li").all_text_contents()
          await page.wait_for_selector('[data-testid="c_ct"]', timeout=200)
          starsList = page.get_by_test_id("c_ct")
          numCCTs = await starsList.count()
          stars = []
          for j in range(numCCTs):
            cct = starsList.nth(j)
            category = await cct.locator("span").first.text_content()
            if category.strip() == "Stars":
              stars = await cct.locator("a").all_text_contents()
              break
          closeButton = page.get_by_test_id("promptable__x").locator("button").first
          await closeButton.click()
        except:
          closeButton = page.get_by_test_id("promptable__x").locator("button").first
          await closeButton.click()
          genres = []
          stars = []
        print(imdb_id, titleText, year, synopsis[0:10], genres, stars, sep=", ")
      if done:
        break
      moreButton = page.locator("button.ipc-see-more__button")
      if await moreButton.count() == 0 or not await moreButton.is_visible():
        break
      pages_count += 1
      await moreButton.click()
    return {"movies_count": count}