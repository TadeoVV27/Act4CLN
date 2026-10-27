from decimal import Decimal
import pytest

from app.domain import (
    Money,
    InvalidOrderData,
    InvalidOrderTransition,
    OrderItem,
    OrderItemLimitExceeded,
)
from cargar_csv import load_fixture


def test_money_negativo():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("-1"))


def test_pedido_o001_inicia_draft_con_total_esperado():
    orders = load_fixture()
    order = orders["O001"]
    assert order.status.value == "DRAFT"
    assert order.units == 4
    assert order.total.amount == Decimal("2100.00")


def test_confirmacion_doble_no_es_permitida():
    orders = load_fixture()
    order = orders["O013"]
    order.confirm()
    assert order.status.value == "CONFIRMED"
    assert [event.name for event in order.events] == ["OrderConfirmed"]

    with pytest.raises(InvalidOrderTransition):
        order.confirm()

    # La operación fallida no cambia el estado ni agrega otro evento.
    assert order.status.value == "CONFIRMED"
    assert [event.name for event in order.events] == ["OrderConfirmed"]


def test_cliente_inactivo_no_puede_confirmar():
    orders = load_fixture()
    order = orders["O003"]
    with pytest.raises(InvalidOrderData):
        order.confirm()
    assert order.status.value == "DRAFT"
    assert order.events == []


def test_no_se_puede_superar_limite_de_20_unidades():
    orders = load_fixture()
    order = orders["O009"]  # Inicia con 19 unidades.
    item = OrderItem("SKU_TEST", 2, Money(Decimal("1.00")))
    with pytest.raises(OrderItemLimitExceeded):
        order.add_item(item)
    assert order.units == 19
