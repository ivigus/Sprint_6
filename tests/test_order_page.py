import pytest
from Sprint_6.pages.order_page import OrderPage
from Sprint_6.test_data import ORDER_TEST_DATA
from Sprint_6.conftest import browser
from Sprint_6.locators import OrderPageLocators


class TestOrderForm:
    @pytest.mark.parametrize("data", ORDER_TEST_DATA)
    @pytest.mark.parametrize("button_action", [
        ("click_order_button", "верхнюю"),
        ("click_order_button_2", "нижнюю")
    ], ids=["top_button", "bottom_button"])
    def test_order_form(self, browser, data, button_action):
        """Тест оформления заказа через разные кнопки"""
        button_method, button_name = button_action
        
        order_page = OrderPage(browser)
        order_page.open(OrderPageLocators.URL)
        
        # Нажимаем cuci только для нижней кнопки
        if button_method == "click_order_button_2":
            order_page.cuci()
        
        # Нажимаем соответствующую кнопку заказа
        getattr(order_page, button_method)()
        
        order_page.fill_name(data["name"])
        order_page.fill_lastname(data["lastname"])
        order_page.fill_address(data["address"])
        order_page.select_metro_station()
        order_page.fill_phone(data["phone"])
        order_page.click_next()

        # Выбор даты
        order_page.open_date_picker_and_select_24()
        # Выбор срока аренды
        order_page.select_rent_term_4_days()
        # Выбор цвета
        order_page.select_color_black_pearl()
        # Нажать кнопку "Заказать" внизу
        order_page.click_order_button_bottom()
        # Подтвердить заказ нажатием "Да"
        order_page.confirm_order()

        modal_header = order_page.wait_for_order_modal()
        assert modal_header.is_displayed(), f"'Заказ оформлен' не отображается при использовании {button_name} кнопки"


class TestLogoNavigation:
    def test_logo_scooter(self, browser):
        """Тест перехода по логотипу Самоката"""
        main_page = OrderPage(browser)
        main_page.open(OrderPageLocators.URL)
        main_page.click_logo_scooter()
        assert main_page.get_current_url() == OrderPageLocators.URL, "Ожидался переход на главную страницу"

    def test_logo_yandex(self, browser):
        """Тест перехода по логотипу Яндекса"""
        other_page = OrderPage(browser)
        other_page.open(OrderPageLocators.URL)
        original_window = browser.current_window_handle
        other_page.click_logo_yandex()
        assert other_page.get_current_url() == OrderPageLocators.URL_Yandex, "Ожидался переход на главную страницу Дзена"