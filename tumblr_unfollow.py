import random
import asyncio
import os
import logging
import nodriver as uc
import getpass

logging.basicConfig(level=logging.INFO)

async def random_sleep(min_seconds, max_seconds):
    wait_time = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(wait_time)

async def click_follow_or_login(tab, email, password):
    login_btn = await asyncio.wait_for(tab.find(text="Log in", best_match=True), timeout=10)
    
    if login_btn:
        await login_btn.scroll_into_view()
        await login_btn.mouse_click()

        await asyncio.sleep(2)
        await tab.get("https://www.tumblr.com/login")

        login_email = await asyncio.wait_for(tab.find("Email", best_match=True), timeout=10)
        await login_email.click()
        await login_email.send_keys(email)
        await asyncio.sleep(2)

        login_password = await asyncio.wait_for(tab.find("Password", best_match=True), timeout=10)
        await login_password.click()
        await login_password.send_keys(password)
        await asyncio.sleep(2)

        login_btn_final = await asyncio.wait_for(tab.find("Log in", best_match=True), timeout=10)
        await login_btn_final.click()
        await asyncio.sleep(8)

        await tab.get("https://www.tumblr.com/following")
        return login_btn
    else:
        return None

async def click_unfollow(tab):
    unfollow_btn = await asyncio.wait_for(tab.find(text="Unfollow", best_match=True), timeout=10)
    
    if unfollow_btn:
        await unfollow_btn.scroll_into_view()
        await unfollow_btn.mouse_click()
        return unfollow_btn
    else:
        return None

async def main(email, password):
    cookie_file_path = '.tumblrmain.dat'
    
    driver = await uc.start()

    if os.path.exists(cookie_file_path):
        await driver.cookies.load(cookie_file_path)
    
    tab = await driver.get("https://www.tumblr.com/following")
    await asyncio.sleep(10)

    await click_follow_or_login(tab, email, password)
    await asyncio.sleep(3)

    unfollow_count = 0
    max_unfollows = 1400
    # ^^ It's the number of people you want to unfollow

    while unfollow_count < max_unfollows:
        next_unfollow = await click_unfollow(tab)

        if next_unfollow is None:
            break

        unfollow_count += 1
        await random_sleep(0.5, 1.0)

    print(f"Unfollowed {unfollow_count} users.")

    await driver.cookies.save(cookie_file_path)
    await asyncio.sleep(2)
    await driver.close()

if __name__ == "__main__":
    email = input("Enter your Tumblr email: ")
    password = getpass.getpass("Enter your Tumblr password: ")
    asyncio.run(main(email, password))
