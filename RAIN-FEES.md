# Rain Protocol Fee Structure

**Source**: Rain team documentation (2026-02-10)

---

## Fee Breakdown by Market Type

### Prediction Markets (5.00% total)

**Three scenarios:**
1. **Marketing Budget** (5.00%)
2. **Organic** (5.00%)  
3. **Organic With Referral** (5.00%)

| Component | Marketing Budget | Organic | Organic w/ Referral |
|-----------|------------------|---------|---------------------|
| Protocol Fee (BBB) | 2.50% | 2.50% | 2.50% |
| Affiliate Fee | 0.00% | - | 0.00% |
| LP | 1.20% | 1.10% | 1.10% |
| LP Affiliate fee | 0.00% | 0.10% | 0.10% |
| Builder | 0.00% | 0.00% | - |
| Market Creator | 1.00% | 1.00% | 1.00% |
| Market Resolver | 0.20% | 0.20% | 0.20% |
| Market Resolution proposer | 0.10% | 0.10% | 0.10% |
| **Total** | **5.00%** | **5.00%** | **5.00%** |

---

### Shared Liquidity Markets (4.00% total)

**Three scenarios:**
1. **Pred Build** (4.00%)
2. **Organic With Referral LM Build** (4.00%)
3. **LM Build** (4.00%)

| Component | Pred Build | Organic w/ Referral | LM Build |
|-----------|------------|---------------------|----------|
| Protocol Fee (BBB) | 2.50% | 2.50% | 2.50% |
| Affiliate Fee | 0.00% | - | 0.00% |
| LP | 1.50% | 1.40% | 1.40% |
| LP Affiliate fee | 0.00% | 0.10% | 0.10% |
| Builder | 0.00% | 0.00% | - |
| Market Creator | 0.00% | 0.00% | 0.00% |
| Market Resolver | 0.00% | 0.00% | 0.00% |
| Market Resolution proposer | 0.00% | 0.00% | 0.00% |
| **Total** | **4.00%** | **4.00%** | **4.00%** |

---

## Key Differences

### Prediction Markets (5.00%)
- **Higher total fees** (5.00%)
- **Lower LP fees** (1.10%-1.20%)
- Includes **market creator** (1.00%)
- Includes **resolver** (0.20%)
- Includes **resolution proposer** (0.10%)
- **Use case**: Individual market creation with manual resolution

### Shared Liquidity Markets (4.00%)
- **Lower total fees** (4.00%)
- **Higher LP fees** (1.40%-1.50%)
- **No creator/resolver fees** (0.00%)
- **Use case**: Automated markets sharing liquidity pools

---

## Components Explained

### Protocol Fee (BBB) - 2.50%
- Base protocol fee
- Goes to Rain protocol
- **Same across all market types**

### LP (Liquidity Provider) - 1.10%-1.50%
- Rewards for providing liquidity
- Higher in shared liquidity markets (1.40%-1.50%)
- Lower in prediction markets (1.10%-1.20%)

### LP Affiliate Fee - 0.00%-0.10%
- Additional LP rewards for referred users
- 0.10% when referral program active
- 0.00% for organic/marketing budget

### Market Creator - 0.00%-1.00%
- Rewards for creating markets
- 1.00% in prediction markets
- 0.00% in shared liquidity markets

### Market Resolver - 0.00%-0.20%
- Rewards for resolving market outcomes
- 0.20% in prediction markets
- 0.00% in shared liquidity markets (automated)

### Market Resolution Proposer - 0.00%-0.10%
- Rewards for proposing resolution
- 0.10% in prediction markets
- 0.00% in shared liquidity markets

---

## MKT Token Allocation

**From MKT token allocation** (limited):
- **0.50% bonus** until Rain protocol reaches $1B accumulated volume
- Incentivizes early adoption
- Applies to specific market types (see table)

---

## Referral Program

### 2nd Tier Referral (Superaffiliate)
- **0.50% additional** for super affiliates
- Examples mentioned: Tipico, MaRe, KJ
- Creates multi-level referral incentives

---

## Examples from Document

### Example 1: MaRe, KJ
- Likely: Organic with referral flow
- 5.00% or 4.00% depending on market type
- Includes LP affiliate fee (0.10%)

### Example 2: KJ
- Likely: Direct referral scenario
- Similar structure with referral bonuses

---

## Strategic Implications for Currents

### Fee Transparency
- **Display total fees** to users (5% or 4%)
- Break down where fees go (protocol, LP, creator, resolver)
- Compare to Polymarket (2% fee)

### Market Type Selection
- **Prediction Markets** (5%):
  - Better for custom markets
  - Manual resolution
  - Higher creator rewards
  
- **Shared Liquidity** (4%):
  - Lower fees for users
  - Automated resolution
  - Better for standardized markets

### Revenue Opportunities
- **Market creation** (1.00% on prediction markets)
- **LP provision** (1.10%-1.50%)
- **Referral program** (0.10% + 0.50% superaffiliate)

---

## UX Recommendations

### 1. Fee Display
Show clear fee breakdown:
```
Trading Fee: 5.00%
├─ Protocol: 2.50%
├─ Liquidity: 1.10%
├─ Creator: 1.00%
├─ Resolver: 0.20%
└─ Resolution Proposer: 0.10%
```

### 2. Market Type Badge
```
[Prediction Market] 5.00% fee
[Shared Liquidity] 4.00% fee
```

### 3. Comparison Tooltip
```
💡 Rain fees: 4-5%
   Polymarket: 2%
   
   Why higher? You earn:
   • Creator rewards (1.00%)
   • LP incentives (1.10%-1.50%)
   • MKT token bonus (0.50%)
```

---

## Questions for Product

1. **Which market types will Currents support?**
   - Prediction markets only?
   - Shared liquidity only?
   - Both?

2. **Will Currents participate in revenue sharing?**
   - Become a market creator (earn 1.00%)?
   - Provide liquidity (earn 1.10%-1.50%)?
   - Run referral program (earn 0.10%)?

3. **How to communicate fees?**
   - Transparent breakdown?
   - Compare to competitors?
   - Emphasize value (creator rewards, MKT tokens)?

4. **Fee calculator?**
   - Show exact fees before trade
   - Break down fee allocation
   - Show potential earnings (LP, referrals)

---

## Technical Integration

### API Response Enhancement
```json
{
  "market_id": "517311",
  "title": "Will Trump deport 250,000-500,000 people?",
  "market_type": "prediction",  // or "shared_liquidity"
  "fees": {
    "total": 0.05,
    "protocol": 0.025,
    "lp": 0.011,
    "creator": 0.01,
    "resolver": 0.002,
    "resolution_proposer": 0.001
  },
  "mkt_bonus": 0.005  // if < $1B volume
}
```

### Fee Calculator Function
```python
def calculate_trade_fees(amount, market_type='prediction'):
    fees = {
        'prediction': {
            'protocol': 0.025,
            'lp': 0.011,
            'creator': 0.01,
            'resolver': 0.002,
            'resolution_proposer': 0.001,
            'total': 0.05
        },
        'shared_liquidity': {
            'protocol': 0.025,
            'lp': 0.015,
            'creator': 0.00,
            'resolver': 0.00,
            'resolution_proposer': 0.00,
            'total': 0.04
        }
    }
    
    fee_breakdown = fees[market_type]
    return {
        'amount': amount,
        'fee_total': amount * fee_breakdown['total'],
        'net_amount': amount * (1 - fee_breakdown['total']),
        'breakdown': {k: amount * v for k, v in fee_breakdown.items()}
    }
```

---

**Saved**: 2026-02-10  
**Source**: Rain team fee structure documentation
