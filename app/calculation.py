import numpy as np
import numpy_financial as npf


def calculation(indexes: str, initialInvestment: int, discountRate: int, cashflows: int, cf1: int ):

    masCashFlows = [cf1]

    initialInvestment = initialInvestment * -1
    discountRate = discountRate / 100
    masCashFlowsUser = [initialInvestment]
    for i in range(cashflows):
        masCashFlowsUser.append(masCashFlows[i])

    npv = npf.npv(discountRate, masCashFlowsUser).round(2)

    sum = np.sum(masCashFlowsUser)
    pi = 1 + (npv / sum).round(2)

    if indexes == 'NPV':
        return npv

