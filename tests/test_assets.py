def test_create_asset(client):
    response = client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["symbol"] == "AAPL"
    assert data["name"] == "Apple Inc."


def test_get_assets(client):
    client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    response = client.get("/assets")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["symbol"] == "AAPL"
    assert data[0]["name"] == "Apple Inc."

def test_get_asset(client):
    create_response = client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    asset_id = create_response.json()["id"]

    response = client.get(f"/assets/{asset_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == asset_id
    assert data["symbol"] == "AAPL"
    assert data["name"] == "Apple Inc."


def test_get_asset_not_found(client):
    response = client.get("/assets/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Asset not found",
    }

def test_update_asset(client):
    create_response = client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    asset_id = create_response.json()["id"]

    response = client.put(
        f"/assets/{asset_id}",
        json={
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == asset_id
    assert data["symbol"] == "GOOGL"
    assert data["name"] == "Alphabet Inc."

def test_update_asset_not_found(client):
    response = client.put(
        "/assets/999",
        json={
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Asset not found",
    }

def test_update_asset_duplicate_symbol(client):
    first_response = client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    first_asset_id = first_response.json()["id"]

    client.post(
        "/assets",
        json={
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
        },
    )

    response = client.put(
        f"/assets/{first_asset_id}",
        json={
            "symbol": "MSFT",
            "name": "Another Company",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Asset with this symbol already exists",
    }

def test_delete_asset(client):
    create_response = client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    asset_id = create_response.json()["id"]

    response = client.delete(f"/assets/{asset_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/assets/{asset_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Asset not found",
    }


def test_delete_asset_not_found(client):
    response = client.delete("/assets/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Asset not found",
    }

def test_create_asset_invalid_data(client):
    response = client.post(
        "/assets",
        json={
            "symbol": "",
            "name": "",
        },
    )

    assert response.status_code == 422

def test_create_asset_whitespace_data(client):
    response = client.post(
        "/assets",
        json={
            "symbol": "   ",
            "name": "   ",
        },
    )

    assert response.status_code == 422

def test_get_assets_pagination(client):
    assets = [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
        },
    ]

    for asset in assets:
        response = client.post("/assets", json=asset)
        assert response.status_code == 200

    response = client.get(
        "/assets?skip=1&limit=1",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["symbol"] == "MSFT"

def test_get_assets_default_pagination(client):
    for index in range(25):
        response = client.post(
            "/assets",
            json={
                "symbol": f"STK{index}",
                "name": f"Stock {index}",
            },
        )

        assert response.status_code == 200

    response = client.get("/assets")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 20

def test_get_assets_by_symbol(client):
    client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    client.post(
        "/assets",
        json={
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
        },
    )

    response = client.get("/assets?symbol=AAPL")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["symbol"] == "AAPL"


def test_get_assets_by_symbol_case_insensitive(client):
    client.post(
        "/assets",
        json={
            "symbol": "AAPL",
            "name": "Apple Inc.",
        },
    )

    response = client.get("/assets?symbol=aapl")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["symbol"] == "AAPL"

def test_get_assets_invalid_skip(client):
    response = client.get("/assets?skip=-1")

    assert response.status_code == 422


def test_get_assets_invalid_limit_zero(client):
    response = client.get("/assets?limit=0")

    assert response.status_code == 422


def test_get_assets_invalid_limit_too_large(client):
    response = client.get("/assets?limit=101")

    assert response.status_code == 422