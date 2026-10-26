"""Módulo de cálculo de métricas de negócio e simulação de rentabilidade.

Este módulo concentra toda a lógica matemática da aplicação de forma pura,
permitindo execução e validação por testes unitários sem acoplamento com UI.
"""

from typing import Any

import pandas as pd

# --- Exceções customizadas ---


class EmptyDataFrameError(ValueError):
    """O DataFrame fornecido está vazio."""

    def __init__(self) -> None:
        super().__init__("O DataFrame está vazio.")


class InvalidDiscountCapError(ValueError):
    """O teto de desconto deve situar-se entre 0.0 e 1.0."""

    def __init__(self) -> None:
        super().__init__("O teto de desconto deve estar entre 0.0 e 1.0.")


# --- Funções ---


def calcular_kpis(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        raise EmptyDataFrameError()

    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())

    net_margin_pct = (total_profit / total_sales * 100.00) if total_sales > 0 else 0.0

    unique_orders = int(df["Order ID"].nunique())
    mean_ticket = (total_sales / unique_orders) if unique_orders > 0 else 0.0

    deficit_mask = df["Profit"] < 0
    loss_orders_count = int(deficit_mask.sum())
    loss_sales = float(df.loc[deficit_mask, "Sales"].sum())
    loss_profit_accumulated = float(df.loc[deficit_mask, "Profit"].sum())

    loss_sales_pct = (loss_sales / total_sales * 100) if total_sales > 0 else 0.0

    return {
        "faturamento_total": total_sales,
        "lucro_consolidado": total_profit,
        "margem_liquida_pct": net_margin_pct,
        "total_pedidos_unicos": unique_orders,
        "ticket_medio": mean_ticket,
        "total_transacoes": len(df),
        "pedidos_deficitarios": loss_orders_count,
        "prejuizo_acumulado": loss_profit_accumulated,
        "faturamento_drenado": loss_sales,
        "percentual_faturamento_drenado": loss_sales_pct,
    }


def obter_piores_categorias(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise EmptyDataFrameError()

    worst = (
        df.groupby("Sub-Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Negative_Orders=("Profit", lambda s: (s < 0).sum()),
            Total_Orders=("Order ID", "count"),
        )
        .reset_index()
    )

    worst["Profit_Margin_%"] = (
        worst["Total_Profit"] / worst["Total_Sales"].replace(0, float("nan")) * 100
    ).fillna(0.0)

    return worst.sort_values(by="Total_Profit", ascending=True).reset_index(drop=True)


def simular_teto_desconto(df: pd.DataFrame, teto_desconto: float) -> dict[str, Any]:
    if df.empty:
        raise EmptyDataFrameError()
    if not (0.0 <= teto_desconto <= 1.0):
        raise InvalidDiscountCapError()

    df_sim = df.copy()

    preco_bruto = df_sim["Sales"] / (1.0 - df_sim["Discount"])
    custo = df_sim["Sales"] - df_sim["Profit"]

    novo_desconto = df_sim["Discount"].clip(upper=teto_desconto)

    df_sim["Sales_simulated"] = preco_bruto * (1.0 - novo_desconto)
    df_sim["Profit_simulated"] = df_sim["Sales_simulated"] - custo

    original_deficit = int((df_sim["Profit"] < 0).sum())
    simulated_deficit = int((df_sim["Profit_simulated"] < 0).sum())

    reducao_pct = (
        ((original_deficit - simulated_deficit) / original_deficit * 100)
        if original_deficit > 0
        else 0.0
    )

    faturamento_simulado = float(df_sim["Sales_simulated"].sum())
    lucro_simulado = float(df_sim["Profit_simulated"].sum())
    lucro_original = float(df_sim["Profit"].sum())

    margem_simulada_pct = (
        (lucro_simulado / faturamento_simulado * 100)
        if faturamento_simulado > 0
        else 0.0
    )

    return {
        "teto_desconto": teto_desconto,
        "faturamento_simulado": faturamento_simulado,
        "lucro_simulado": lucro_simulado,
        "recuperacao_financeira": lucro_simulado - lucro_original,
        "margem_liquida_simulada_pct": margem_simulada_pct,
        "reducao_pedidos_deficitarios_pct": reducao_pct,
        "pedidos_deficitarios_restantes": simulated_deficit,
    }


def analisar_desconto_vs_margem(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise EmptyDataFrameError()

    df_work = df.copy()
    df_work["Discount_Category"] = pd.cut(
        df_work["Discount"],
        bins=[-0.01, 0.1, 0.2, 0.3, 1.0],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True,
    )

    grup = (
        df_work.groupby(["Category", "Discount_Category"], observed=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Deficit_Orders=("Profit", lambda s: (s < 0).sum()),
            Total_Orders=("Order ID", "count"),
        )
        .reset_index()
    )

    grup["Liquid_Margin_%"] = (
        grup["Profit"] / grup["Sales"].replace(0, float("nan")) * 100.0
    ).fillna(0.0)

    grup["Deficit_Order_Rate_%"] = (
        grup["Deficit_Orders"] / grup["Total_Orders"].replace(0, float("nan")) * 100.0
    ).fillna(0.0)

    return grup
