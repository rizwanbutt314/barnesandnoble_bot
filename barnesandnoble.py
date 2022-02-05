import time
from utils import (
    BASE_URL,
    EMAIL,
    Elements,
    Driver,
    NoSuchElementException
)


def main():
    """
        Driver without proxy:
            driver = Driver()
        
        Driver with proxy:
            driver = Driver(use_tor_sock_proxy=True)
    """

    driver = Driver()
    driver.get(BASE_URL)

    driver.move_to_element(Elements.MY_ACCOUNT_BTN)

    # click on sign in button
    driver.click(Elements.SINGIN_BTN)
    time.sleep(5)

    # switch to sign in iframe
    driver.switch_to_iframe(Elements.SINGIN_IFRAME)

    # click on forgot password button
    driver.click(Elements.FORGOT_PASSWORD_BTN)
    time.sleep(5)

    # Back to default content
    driver.switch_to_default_content()

    # switch to forgot password iframe
    driver.switch_to_iframe(Elements.FORGOT_PASSWORD_IFRAME)

    # Enter data to email input
    driver.enter_text(Elements.EMAIL_INPUT, EMAIL)

    # Click on continue Button
    driver.click(Elements.RESET_PASSWORD_BTN)

    # wait for alert message to show
    try:
        alert_text = driver.get_text(Elements.ALERT_MSG)
        print(f"Alert: {alert_text}")
    except NoSuchElementException:
        print("Alert Message not found")


if __name__ == "__main__":
    main()