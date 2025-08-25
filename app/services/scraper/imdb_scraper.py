from contextlib import suppress
import logging
import re
import sys
from playwright.async_api import async_playwright

from app.schemas.movie import MovieIn
from app.services.repo.movies_repo import add_movies
logger = logging.getLogger(__name__)
searchUrl = "https://www.imdb.com/search/title/?title_type=feature&user_rating=9,10&num_votes=50,"
class ParseError(Exception):
  """Failed to parse a text section block"""

async def parse_title_block(div):
  try:
    title = div.locator("h3.ipc-title__text.ipc-title__text--reduced")
    title_text = await title.inner_text(timeout=200)
    title_text = re.sub(r"^\d+\.\s*", "", title_text)
    href = await div.locator("div.ipc-title").first.locator("a").get_attribute("href")
    match = re.search(r"/title/(tt\d+)", href)
    imdb_id = match.group(1)
    return imdb_id, title_text
  except Exception as e:
    raise ParseError("Could not parse title block") from e
async def close_modal(page, timeout=500):
  modal = page.get_by_test_id("promptable__pc")

  # If no modal is present, nothing to do
  if await modal.count() == 0:
      return

  # Try the visible "X" button first
  with suppress(Exception):
      btn = page.get_by_test_id("promptable__x").locator("button").first
      if await btn.is_visible():
          await btn.click()

  # Fallback: press Escape if still open
  if await modal.count() > 0:
      with suppress(Exception):
          await page.keyboard.press("Escape")

  # Wait for it to go away; don't crash if timing is tight
  with suppress(Exception):
      await modal.wait_for(state="detached", timeout=timeout)
  if await modal.count() > 0:
      with suppress(Exception):
          await modal.first.wait_for(state="hidden", timeout=timeout)
async def parse_year_synopsis_rating(div):
  try:
    year = int(await div.locator("span.sc-15ac7568-7.cCsint.dli-title-metadata-item").first.inner_text())
  except:
    year = None
  try:
    synopsis = await div.locator("div.ipc-html-content-inner-div").inner_text(timeout=200)
  except:
    synopsis = None
  try:
    rating = await div.locator("span.ipc-rating-star--rating").inner_text(timeout=200)
  except:
    rating = 9
  return year, synopsis, rating
async def parse_genres_stars_from_details(div, page):
  try:
    detailsButton = div.locator("button.ipc-icon-button")
    if await detailsButton.count() == 0:
      raise Exception("Couldn't find details button.")
    await detailsButton.first.click()
    try:
      await page.wait_for_selector('[data-testid="btp_gl"]', timeout=200)
      genresList = page.get_by_test_id("btp_gl")
      genres = await genresList.locator("li").all_text_contents()
    except Exception as e:
      # logger.warning(f"Could not find genres list: {e}")
      genres = []
    try:
      await page.wait_for_selector('[data-testid="c_ct"]', timeout=500)
      starsList = page.get_by_test_id("c_ct")
      numCCTs = await starsList.count()
      stars = []
      for j in range(numCCTs):
        cct = starsList.nth(j)
        category = await cct.locator("span").first.text_content()
        if category.strip() == "Stars":
          stars = await cct.locator("a").all_text_contents()
          break
    except Exception as e:
      # logger.warning(f"Could not find stars list: {e}")
      stars = []
  except Exception as e:
    logger.warning(f"Could not find details button: {e}")
    genres = []
    stars = []
  finally:
    await close_modal(page)
    return genres, stars
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
    logging.info(f"Arrived at {searchUrl}")
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
        logging.info(f"Final page: {newMoviesCount} movies")
      movies_batch = []

      for i in range(newMoviesCount):
        n = pages_count * 50 + i
        div = divs.nth(n)
        try:
          imdb_id, title_text = await parse_title_block(div)
        except ParseError as e:
          logger.warning(f"Could not parse title for {e}, skipping...")
          continue
        year, synopsis, rating = await parse_year_synopsis_rating(div)
        genres, stars = await parse_genres_stars_from_details(div, page)
          # logger.info("Details closed successfully")
        movie_obj = MovieIn(
          imdb_id=imdb_id,
          title=title_text,
          year=year,
          rating=rating,
          synopsis=synopsis,
          genres=genres,
          cast=stars
        )
        movies_batch.append(movie_obj)
        sys.stdout.write(".")
        sys.stdout.flush()
      print()
      await add_movies(movies_batch)
      if done:
        break
      moreButton = page.locator("button.ipc-see-more__button")
      if await moreButton.count() == 0 or not await moreButton.is_visible():
        break
      pages_count += 1
      await moreButton.click()
    return {"movies_count": count}