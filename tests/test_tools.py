from tools import search_listings

def test_search_returns_results():
    results = search_listings("vintage", None, 100)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings(
        "designer ballgown",
        "XXS",
        5
    )
    assert results == []

def test_price_filter():
    results = search_listings(
        "jacket",
        None,
        20
    )

    assert all(
        item["price"] <= 20
        for item in results
    )