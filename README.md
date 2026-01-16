## POM Case study code
### This code is set in place to aid in solving the variious numerical and computation heavy processes in solving the POM workshop tasks
to run most of the files you will need 
### A working python installation 
### The following libraries
run: `pip install networkx matplotlib requests numpy osmnx geopy pandas` 

For most of the files you may just need to run them but some such as the shelf utilizatoin require some parameters inorder to run 

# Documentation for Case study 1 on shelf utilization

# Documentation: CaseStud1_No1_Shelf_Util.py

## Overview
This Python module simulates a production planning system for managing shelf allocation across three plants (A, B, and C) over a 5-year planning period (2026-2030). It calculates optimal shelf distribution based on production requirements, yields, and workforce needs.

## Purpose
The utility helps decision-makers understand:
- How many shelves each plant requires based on projected sales
- Profit/loss margins relative to production targets
- Workforce requirements (workers, technicians, and team leaders)

## Key Data Structures

### Production Yield Per Shelf
```python
data_yield = [
    ["A", 0.5],  # Plant A yields 0.5 tons per shelf
    ["B", 0.3],  # Plant B yields 0.3 tons per shelf
    ["C", 0.4],  # Plant C yields 0.4 tons per shelf
]
```

### Projected Sales Data
The module contains three arrays representing sales projections for each plant across 5 years:
- `plant_a`: [1.5, 1.1, 0.8, 0.5, 0.0] tons per year
- `plant_b`: [0.0, 0.1, 0.3, 0.5, 0.6] tons per year
- `plant_c`: [0.6, 1.2, 0.6, 1.2, 0.6] tons per year

## Main Functions

### `calcShelvesForAYear(pro_year, yield_p_shelf)`
Calculates the minimum number of shelves required to meet production for a single plant.
- **Input**: Production target (pro_year) and yield per shelf
- **Output**: Number of shelves needed (rounded up using `ceil`)
- **Formula**: shelves = ⌈production / yield_per_shelf⌉

### `calcProjectedShelvesSize(idx)`
Determines the ideal shelf allocation for all three plants for a given year.
- **Input**: Year index (0-4, where 0 = 2026)
- **Output**: List [shelves_A, shelves_B, shelves_C]
- **Purpose**: Shows what the optimal shelf distribution should be

### `calcYields(value)`
Calculates actual production yield based on shelf allocation.
- **Input**: List of shelves allocated [shelvesA, shelvesB, shelvesC]
- **Output**: Actual yields produced [yieldA, yieldB, yieldC]
- **Calculation**: yield = shelves × yield_per_shelf

### `calcProfitsAndLosses(value, idx)`
Compares actual production to projected targets, calculating profit/loss margins.
- **Input**: Shelf allocation and year index
- **Output**: Profit/loss for each plant [pl_A, pl_B, pl_C]
- **Calculation**: profit_loss = (actual_yield) - (projected_sales)

### `calcWorkers(value)`
Determines workforce requirements based on shelf allocation.
- **Input**: List of shelves allocated [shelvesA, shelvesB, shelvesC]
- **Output**: Workers breakdown per plant [[workers, technicians, leaders], ...]
- **Staffing Rules**:
  - Base: 3 technicians per plant
  - Team Leaders: 1 per shelf (+ oversight)
  - Production Workers: 1 worker per 0.1 tons of yield (⌈yield / 0.1⌉)
  - Additional Technician: 1 more per plant if shelves > 0

### `main(shelfA, shelfB, shelfC, year)`
Main execution function that orchestrates calculations and records results.
- **Input**: Shelf counts for each plant and year (command-line arguments)
- **Process**:
  1. Validates input shelf counts
  2. Calculates profits/losses for the given year
  3. Computes required workforce
  4. Writes results to `records.txt`
- **Output**: Records file with shelves, profit/loss, and workforce data

## Usage

Run from command line with four arguments:
```bash
python CaseStud1_No1_Shelf_Util.py <shelfA> <shelfB> <shelfC> <year>
```

**Example**:
```bash
python CaseStud1_No1_Shelf_Util.py 3 0 2 0
```
This allocates 3 shelves to Plant A, 0 to Plant B, 2 to Plant C for year 2026 (index 0).

## Output

Results are appended to `records.txt` in the following format:
- Shelf allocation for each plant
- Profit/loss margins relative to projected sales
- Workforce requirements (workers, technicians, leaders) per plant

## Key Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `years` | List | Year labels (2026-2030) |
| `plant_a/b/c` | List | Projected sales per year (tons) |
| `year_shelves` | List | Stores calculated shelf requirements (declared but unused) |
| `year_profits_losses` | List | Stores profit/loss data (declared but unused) |

## Notes

- The module uses functional programming with `reduce()` to sum shelf counts
- Ceiling function ensures adequate shelf allocation to meet all targets
- Worker calculations account for management overhead (team leaders) plus production workers
- Results are accumulated in `records.txt` (append mode), preserving historical calculations


# NPV.py - Net Present Value Analysis

## Overview
This module performs financial analysis comparing two investment strategies for facility acquisition: **building ownership** versus **renting**. It calculates Net Present Value (NPV) for a 5-year investment period (2026-2030) to determine which option is more financially viable.

## Purpose
The utility helps determine:
- Whether it's more cost-effective to buy and maintain a building or rent
- Expected cash flows based on projected sales
- Net profit/loss after discounting future cash flows
- Impact of residual asset values at the end of the investment period


## Key Financial Data

### Investment Costs

**Buying (One-time and recurring costs)**:
```python
buying = {
    "buildingCosts": 1.5,    # Building construction: $1.5M
    "land_costs": 0.5,       # Land acquisition: $0.5M
    "equipment": 3,          # Equipment: $3M
}
```
**Total Initial Investment for Buying**: $5M

**Renting**:
```python
renting = {
    "buildingLand": 40000    # Annual rent: $40,000
}
```

### Product Costs and Pricing

Three product lines (D, E, F) with associated costs and selling prices:

**Consumables Cost** (Manufacturing cost per unit):
- D: $5,000
- E: $6,000
- F: $4,500

**Sales Price**:
- D: $7,500
- E: $8,000
- F: $6,000

**Gross Profit Per Unit**:
- D: $2,500
- E: $2,000
- F: $1,500

### Sales Projections (2026-2030)

```python
projectedAnnualSales = {
    "2026": 0.1,   # 100,000 units
    "2027": 0.3,   # 300,000 units
    "2028": 0.8,   # 800,000 units
    "2029": 1.0,   # 1,000,000 units
    "2030": 1.3,   # 1,300,000 units
}
```

### Financial Parameters

- **Discount Rate**: 0.1 (10% annual compounded monthly)
- **Maintenance as % of Initial Investment**: 15% yearly
- **Residual Land Value**: 80% of original cost (recoverable at end of period)
- **Residual Building Value**: 0% (fully depreciated)

## Core Functions

### `calcSumBuilding()`
Calculates total initial investment for building purchase.
- **Output**: Sum of building costs, land costs, and equipment ($5.0M)
- **Purpose**: Baseline for NPV calculation in purchase scenario

### `calcSumRenting()`
Calculates total rent-related costs over 5 years.
- **Calculation**: (40000 / 10^6) × 5 + 3 = $3.0M
- **Purpose**: Baseline for NPV calculation in rental scenario

### `calcNetSalesPerYear()`
Calculates gross profit per product line (selling price minus cost).
- **Output**: Dictionary with net sales per product {D: 2500, E: 2000, F: 1500}
- **Purpose**: Used to determine per-unit profitability

### `calcTotalNetSales()`
Sums total gross profit across all three product lines.
- **Output**: 2500 + 2000 + 1500 = $6,000 per unit
- **Purpose**: Total revenue per unit sold

### `calcCashFlows()`
Calculates annual cash flows normalized to millions.
- **Process**: 
  1. Gets total net sales per unit
  2. Multiplies by annual sales projection
  3. Divides by 10^6 to normalize to millions
- **Output**: Dictionary with cash flows for each year (millions)
- **Example**: Year 2026: $6,000 × 0.1 / 10^6 = $0.0006M

### `calcNPVBuilding(maintainYearly=False)`
Calculates NPV for building purchase option.
- **Parameters**:
  - `maintainYearly`: If True, maintenance subtracted yearly; if False, deducted upfront
- **Process**:
  1. Subtracts initial investment ($5M)
  2. Applies maintenance costs (15% of initial investment = $0.75M/year)
  3. Discounts cash flows: CF / (1 + discount_rate)^year
  4. Adds back residual land value (80% of $0.5M = $0.4M)
- **Output**: NPV value in millions
- **Formula**: NPV = -Initial + Σ(CashFlow / (1.1)^year) - MaintenanceCosts + ResidualValue

### `calcNPVRenting()`
Calculates NPV for renting option.
- **Process**:
  1. Subtracts initial rental setup costs ($3M)
  2. Applies 15% maintenance yearly
  3. Discounts cash flows over 5 years
- **Output**: NPV value in millions
- **Key Difference**: No residual value recovery at end of period (rented asset)

## Usage

Run directly as a script:
```bash
python NPV.py
```

## Output

The script generates NPV calculations and appends them to `records.txt`:

```
Net Sales per Product: {D: 2500, E: 2000, F: 1500}
Annual Cash Flows (millions): [0.0006, 0.0018, 0.0048, 0.006, 0.0078]

Building NPV yearly maintenance: <value>
Building NPV initial: <value>
Building NPV renting: <value>
```

## Interpretation

**Decision Rule**:
- Compare the three NPV values
- **Positive NPV** = Value-creating investment
- **Highest NPV** = Most financially attractive option
- Typically: Buying with residual value recovery > Renting > Buying with upfront maintenance

## Key Variables Summary

| Variable | Type | Purpose |
|----------|------|---------|
| `buying` | Dict | One-time construction/equipment costs |
| `renting` | Dict | Annual rental expenses |
| `consumablesCost` | Dict | Manufacturing cost per product |
| `salesPrice` | Dict | Selling price per product |
| `projectedAnnualSales` | Dict | Sales volume by year (millions) |
| `COMPOUDED_MONTHLY_DISCOUNT_RATE` | Float | 10% annual discount rate |
| `RESIDUAL_VALUE_LAND` | Float | 80% of land cost recovered |
| `RESIDUAL_VALUE_BUILDING` | Float | 0% depreciation (fully used) |

## Financial Concepts Used

- **Net Present Value (NPV)**: Present value of all future cash flows minus initial investment
- **Discounting**: Adjusting future cash flows to present value using discount rate
- **Maintenance Costs**: Operating expenses estimated at 15% of initial investment annually
- **Residual Value**: Salvage value of assets at end of investment period

## Notes

- Discount rate (10%) is applied annually using the formula: CF / (1 + rate)^year
- Calculations assume all cash flows occur at year-end
- The module uses functional programming with `reduce()` for aggregations
- Results are appended to `records.txt` preserving all historical analyses
- The comparison helps decision-makers choose between capital-intensive (buying) vs. operational-intensive (renting) strategies

## Documentation for case study 3 No4
Below is the **mathematical formulation** of what your code is doing, followed by a **step-by-step explanation** that maps directly to each line of the function.

## 1. Mathematical Equation Used (Normal Distribution)

Your code is plotting the **probability density function (PDF)** of a normal (Gaussian) distribution:

$$f(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2\right)$$

### Correspondence to Your Code

| Mathematical Symbol | Code Variable |
|---|---|
| $\mu$ (mean) | `mean` |
| $\sigma$ (population standard deviation) | `std_dev` |
| $x$ | `x` |
| $f(x)$ | `y` |

---

## 2. How the Bell Curve Is Constructed (Step by Step)

### Step 1: Input Data

`shelf` is a **list of numerical observations**, for example monthly yields from a shelf:

$$\{x_1, x_2, \ldots, x_n\}$$

---

### Step 2: Compute the Mean

```python
mean = calcMean(values)
```

$$\mu = \frac{1}{n} \sum_{i=1}^{n} x_i$$

The mean determines the **center of the bell curve**.

---

### Step 3: Compute the Population Standard Deviation

```python
std_dev = calcPopStandardDeviation(values)
```

$$\sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \mu)^2}$$

The standard deviation controls the **spread (width)** of the curve.

---

### Step 4: Define the x-Range (±3σ Rule)

```python
x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
```

Mathematically:

$$x \in [\mu - 3\sigma,\ \mu + 3\sigma]$$

This interval is chosen because:

* ~68% of data lies within $\pm 1\sigma$
* ~95% within $\pm 2\sigma$
* ~99.7% within $\pm 3\sigma$

Thus, nearly the **entire distribution** is captured.

---

### Step 5: Compute the Bell Curve Values

```python
y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
```

This evaluates:

$$y = f(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2\right)$$

For each point $x$, the formula computes the **height of the bell curve**.

---

### Step 6: Plot the Curve

```python
plt.plot(x, y)
```

This produces the **smooth bell-shaped curve** centered at $\mu$, with width determined by $\sigma$.

---

## 3. Interpretation of the Bell Curve

* The curve is **not a histogram** of your data
* It is a **theoretical normal distribution** fitted using:
  * empirical mean
  * empirical population standard deviation

The area under the curve equals **1**, meaning it represents a probability density.

---

## 4. Intuition

* Higher $\sigma$ → wider, flatter curve
* Lower $\sigma$ → narrower, taller curve
* Shifting $\mu$ → moves the curve left or right

Your data determine only **two parameters** ($\mu, \sigma$), and the bell curve is then fully defined.

---

## 5. Important Note

You are using the **population standard deviation**, which assumes the shelf data represents the full population.
If the shelf values are a **sample**, the sample standard deviation should be used instead.

---

If you want, I can also:

* Overlay this curve on a histogram of the shelf data
* Explain when the normal assumption is justified
* Show how to test normality (Shapiro–Wilk, Q-Q plot)

Just tell me.
## 1. Mathematical Equation Used (Normal Distribution)

Your code is plotting the **probability density function (PDF)** of a normal (Gaussian) distribution:

$$
f(x) = \frac{1}{\sigma \sqrt{2\pi}}
\exp!\left(-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2\right)
$$

### Correspondence to Your Code

| Mathematical Symbol                        | Code Variable |
| ------------------------------------------ | ------------- |
| ( \mu ) (mean)                             | `mean`        |
| ( \sigma ) (population standard deviation) | `std_dev`     |
| ( x )                                      | `x`           |
| ( f(x) )                                   | `y`           |

---

## 2. How the Bell Curve Is Constructed (Step by Step)

### Step 1: Input Data

`shelf` is a **list of numerical observations**, for example monthly yields from a shelf.

$$
{x_1, x_2, \ldots, x_n}
$$

---

### Step 2: Compute the Mean

```python
mean = calcMean(values)
```

$$
\mu = \frac{1}{n} \sum_{i=1}^{n} x_i
$$

The mean determines the **center of the bell curve**.

---

### Step 3: Compute the Population Standard Deviation

```python
std_dev = calcPopStandardDeviation(values)
```

$$
\sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \mu)^2}
$$

The standard deviation controls the **spread (width)** of the curve.

---

### Step 4: Define the x-Range (±3σ Rule)

```python
x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
```

Mathematically:

$$
x \in [\mu - 3\sigma,\ \mu + 3\sigma]
$$

This interval is chosen because:

* ~68% of data lies within ( \pm 1\sigma )
* ~95% within ( \pm 2\sigma )
* ~99.7% within ( \pm 3\sigma )

Thus, nearly the **entire distribution** is captured.

---

### Step 5: Compute the Bell Curve Values

```python
y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
```

This evaluates:

$$
y = f(x) = \frac{1}{\sigma \sqrt{2\pi}}
\exp!\left(-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2\right)
$$

For each point ( x ), the formula computes the **height of the bell curve**.

---

### Step 6: Plot the Curve

```python
plt.plot(x, y)
```

This produces the **smooth bell-shaped curve** centered at ( \mu ), with width determined by ( \sigma ).

---

## 3. Interpretation of the Bell Curve

* The curve is **not a histogram** of your data
* It is a **theoretical normal distribution** fitted using:

  * empirical mean
  * empirical population standard deviation

The area under the curve equals **1**, meaning it represents a probability density.

---

## 4. Intuition

* Higher ( $\sigma$ ) → wider, flatter curve
* Lower ( $\sigma$) → narrower, taller curve
* Shifting ( $\mu$ ) → moves the curve left or right

Your data determine only **two parameters** (( $\mu, \sigma$ )), and the bell curve is then fully defined.

---

## 5. Important Note

You are using the **population standard deviation**, which assumes the shelf data represents the full population.
If the shelf values are a **sample**, the sample standard deviation should be used instead.

---