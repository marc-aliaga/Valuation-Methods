import numpy as np

def calculate_siprifi_valuation(params):

    # 1. Parameters
    g = params['g']
    r_A = params['r_A']
    r_B = params['r_B']
    tau = params['tau']
    delta = params['delta']
    f = params['f']
    omega = params['omega']
    alpha_K = params['alpha_K']
    alpha_L = params['alpha_L']

    c = params['c']
    rho = params['rho']
    sigma = params['sigma']
    z_0 = params['z_0']

    horizon = params.get('horizon', 50)

    # Safety checks
    assert alpha_K + alpha_L < 1, "Returns to scale must be < 1"
    assert r_A > g, "Discount rate must exceed growth rate"

    # 2. Optimal scale (φ*)
    
    denom = (r_A / (1 - tau)) + f + delta
    power = 1 / (1 - (alpha_K + alpha_L))

    phi_1 = (
        (alpha_K / denom) ** (1 - alpha_L)
        * (alpha_L / omega) ** alpha_L
    ) ** power

    phi_2 = (
        (alpha_K / denom) ** alpha_K
        * (alpha_L / omega) ** (1 - alpha_K)
    ) ** power

    # 3. Expected profit shock path 

    M_z = 0.0

    adj_factor = np.exp(
        -0.5 * sigma**2 * (alpha_K + alpha_L) / (1 - (alpha_K + alpha_L))**2
    )

    for n in range(1, horizon + 1):
        Ez = (
            c ** ((1 - rho**n) / (1 - rho))
            * z_0 ** (rho**n)
            * np.exp(0.5 * sigma**2 * (1 - rho**(2*n)) / (1 - rho**2))
        )

        M_z += ((1 + g) / (1 + r_A))**n * Ez**power

    M_z *= adj_factor

    # 4. P* (economic surplus)
    operating_surplus = (
        phi_1**alpha_K * phi_2**alpha_L
        - f * phi_1
        - delta * phi_1
        - omega * phi_2
    )

    p_star = operating_surplus * (1 - tau) - r_A * phi_1

    # 5. Going-concern value
    G_z = M_z * p_star

    # 6. Book value (early-stage safe)
    K_0 = params.get('K_0', 1.0)
    L_0 = params.get('L_0', 1.0)
    B_0 = params.get('B_0', 0.0)

    Q_0 = z_0 * (K_0**alpha_K) * (L_0**alpha_L)

    book_equity = (
        (Q_0 - f*K_0 - delta*K_0 - omega*L_0 - r_B*B_0)
        * (1 - tau)
        + K_0 - B_0
    )

    total_value = max(0.0, book_equity + G_z)

    return {
        "Total Valuation": total_value,
        "Going-Concern Value": G_z,
        "Optimal Capital (K*)": phi_1,
        "Optimal Labor (L*)": phi_2
    }
siprifi_data = {

    'g': 0.02,        # growth rate
    'r_A': 0.25,      # risk adjusted rate
    'r_B': 0.08,      # debt cost
    
    # FIRM COSTS 
    'tau': 0.21,      # tax rate
    'delta': 0.15,    # depreciation 
    'f': 0.15,        # fixed costs
    'omega': 0.8,     # labor costs
    
    # ELACTICITY
    'alpha_K': 0.10,  # relation between asstes and profit
    'alpha_L': 0.60,  # relation between workforce and profit
    
    # STOCHASTIC PROFITS 
    'c': 1.1,         # expected efficency
    'rho': 0.6,       # Mean reversion (not permanent shocks)
    'sigma': 0.40,    # HIGH volatility = startup risk profile ⚡
    'z_0': 1.0,       # Current productivity
    
    # BALANCE SHEET 
    'K_0': 1.0, 'L_0': 1.0, 'B_0': 0.0,  # minimum needed
    'horizon': 50     # horizon to growth
   }

result = calculate_siprifi_valuation(siprifi_data)

print(f"Siprifi Valuation: ${result['Total Valuation']:,.2f}")
print(f"Going-Concern Value: ${result['Going-Concern Value']:,.2f}")
