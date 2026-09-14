# Asset Correlation as Hilbert Space Geometry

This project visualizes the relationship between two financial assets (**UPST** & **SOFI**) not just as time series, but as vectors in a mathematical space called $L^2(\Omega)$. 

---

## 1. The Mathematical Foundation

In quantitative finance, we treat a return series $X$ as a random variable. The space of these variables has a geometric structure where:
* **Length (Norm):** Represents the Volatility ($\sigma$).
* **Angle ($\theta$):** Represents the Correlation ($\rho$).

### The "Law of Cosines" for Finance
The fundamental link between statistics and geometry is the definition of the **Correlation**:
$$\rho_{XY} = \cos(\theta)$$

Where $\theta$ is the angle between the two asset vectors.

### Asset Vectors Construction
To visualize this in a 2D plane (as seen in the code), we define:
1.  **Vector 1 (Asset X):** Placed on the x-axis.
    $$\vec{v_1} = [\sigma_X, 0]$$
2.  **Vector 2 (Asset Y):** Placed at an angle $\theta$ relative to $v_1$.
    $$\vec{v_2} = [\sigma_Y \cos(\theta), \sigma_Y \sin(\theta)]$$



---

## 2. Statistical Moments (The Code Logic)

The script calculates the "Moments" of the distributions using the following formulas:

| Metric | Formula | Description |
| :--- | :--- | :--- |
| **Log Returns** | $r_t = \ln(P_t / P_{t-1})$ | Continuous compounding returns. |
| **Expected Return** | $E[X] = \frac{1}{n} \sum X_i$ | The average drift of the asset. |
| **Variance** | $\sigma^2 = E[(X - E[X])^2]$ | The "spread" or total risk. |
| **Covariance** | $\text{cov}(X,Y) = E[(X-E[X])(Y-E[Y])]$ | How the assets breathe together. |
| **Correlation** | $\rho = \frac{\text{cov}(X,Y)}{\sigma_X \sigma_Y}$ | The cosine of the angle between assets. |

---

## 3. Geometric Interpretation of the Dashboard

### A. The Scatter Plot (Linear Dependence)
The scatter plot of returns visualizes the **Covariance**. 
* If the dots form a diagonal line: High Correlation (Small angle $\theta$).
* If the dots form a circle: Zero Correlation (Right angle $\theta = 90^\circ$).



### B. The Vector Panel (The Hilbert Space)
This is the most advanced part of the script. It translates the abstract correlation into a physical angle:
* **Arrow Length:** The longer the arrow, the higher the volatility.
* **Proximity of Arrows:** The closer the arrows are to each other, the more the assets move in tandem.
* **Orthogonality:** If the arrows are at $90^\circ$, the assets are perfectly diversified (independent).

---

## 4. Why UPST & SOFI? (Analysis Insight)
By running this code on Fintech stocks like **UPST** and **SOFI**, you will likely observe:
1.  **High Volatility:** Long vectors.
2.  **High Correlation:** A very small angle $\theta$ between vectors. 
3.  **The Result:** Since they are "pointing" in the same direction, combining them offers very little diversification. You are essentially doubling down on the same "Risk Dimension."

---

## 5. How to use this for Markowitz?
Once you have the angle $\theta$ and the lengths $\sigma_X, \sigma_Y$, the distance between the tips of the arrows represents the **Risk of a Long-Short Portfolio**:
$$\text{Dist}^2 = \sigma_X^2 + \sigma_Y^2 - 2\sigma_X\sigma_Y\cos(\theta)$$
