import pytest
from credit_card_rewards import reward_points, late_payment_fee, card_status

# --- Tests for reward_points ---
def test_classic_grocery():
    assert reward_points("classic", 1000, "grocery", False) == 10

def test_reward_points_invalid_tier():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 1000, "grocery", False)

def test_reward_points_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("gold", 0, "grocery", False)

def test_reward_points_fuel():
    assert reward_points("gold", 1000, "fuel", False) == 0

def test_reward_points_dining():
    # Covers 'category == "dining"'
    assert reward_points("gold", 1000, "dining", False) == 40

def test_reward_points_travel():
    # Covers 'category == "travel"' (the second branch of the 'or' condition)
    assert reward_points("platinum", 1000, "travel", False) == 80

def test_reward_points_weekend_platinum():
    # Covers is_weekend=True and card_tier != "classic"
    assert reward_points("platinum", 100, "grocery", True) == 54

def test_reward_points_weekend_classic():
    # Covers is_weekend=True when card_tier == "classic" (False branch)
    assert reward_points("classic", 100, "grocery", True) == 1

# --- Tests for late_payment_fee ---
def test_paid_on_time():
    assert late_payment_fee(5000, 0) == 0

def test_no_outstanding():
    # Covers 'outstanding <= 0' (the second branch of the 'or' condition)
    assert late_payment_fee(0, 10) == 0

def test_late_fee_tier_1():
    assert late_payment_fee(1000, 15) == 100

def test_late_fee_tier_2():
    assert late_payment_fee(5000, 15) == 500

def test_late_fee_tier_3():
    assert late_payment_fee(15000, 15) == 1000

def test_late_fee_over_30_days():
    assert late_payment_fee(500, 35) == 850

# --- Tests for card_status ---
def test_card_status_frozen():
    assert card_status(50, 0, True) == "frozen"

def test_card_status_blocked():
    assert card_status(50, 3, False) == "blocked"

def test_card_status_over_limit():
    assert card_status(95, 0, False) == "over limit risk"

def test_card_status_watch_utilisation():
    assert card_status(50, 0, False) == "watch"

def test_card_status_watch_missed_payments():
    # Covers 'missed_payments > 0' when utilisation <= 30
    assert card_status(20, 1, False) == "watch"

def test_card_status_good():
    assert card_status(20, 0, False) == "good"