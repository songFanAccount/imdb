import re
# import asyncio
# from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter
from playwright.async_api import async_playwright

router = APIRouter(prefix="/scrape", tags=["scrape"])

@router.get("/")
async def scrape_IMDB():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
      user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    await page.goto("https://www.imdb.com/search/title/?title_type=feature&user_rating=9,9.1&genres=action", wait_until="domcontentloaded")
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
          title = await div.locator("h3.ipc-title__text.ipc-title__text--reduced").inner_text(timeout=200)
          title = re.sub(r"^\d+\.\s*", "", title)
        except:
          done = True
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
          await page.wait_for_selector('[data-testid="btp_gl"]')
          genresList = page.get_by_test_id("btp_gl")
          genres = await genresList.locator("li").all_text_contents()
          await page.wait_for_selector('[data-testid="c_ct"]')
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
          print("More details failed")
          genres = []
          stars = []
        print(title, year, synopsis[0:10], genres, stars)
      if done:
        break
      moreButton = page.locator("button.ipc-see-more__button")
      if await moreButton.count() == 0 or not await moreButton.is_visible():
        break
      pages_count += 1
      await moreButton.click()
    return {"movies_count": count}