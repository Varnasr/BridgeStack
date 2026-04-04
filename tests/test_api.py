class TestHealthEndpoints:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "BridgeStack API"
        assert "stacks" in data

    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "healthy"
        assert body["database"] == "connected"
        assert "version" in body

    def test_docs_available(self, client):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema(self, client):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert response.json()["info"]["title"] == "BridgeStack API"


class TestGeography:
    def test_list_states_empty(self, client):
        response = client.get("/api/v1/geography/states")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_states(self, client, seed_data):
        response = client.get("/api/v1/geography/states")
        assert response.status_code == 200
        states = response.json()
        assert len(states) == 2
        assert states[0]["state_name"] == "Karnataka"

    def test_filter_states_by_region(self, client, seed_data):
        response = client.get("/api/v1/geography/states?region=South")
        states = response.json()
        assert len(states) == 1
        assert states[0]["state_id"] == "KA"

    def test_get_state_detail(self, client, seed_data):
        response = client.get("/api/v1/geography/states/KA")
        assert response.status_code == 200
        state = response.json()
        assert state["state_name"] == "Karnataka"
        assert len(state["districts"]) == 2

    def test_state_not_found(self, client):
        response = client.get("/api/v1/geography/states/NONEXISTENT")
        assert response.status_code == 404

    def test_list_districts(self, client, seed_data):
        response = client.get("/api/v1/geography/districts")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_filter_districts_by_state(self, client, seed_data):
        response = client.get("/api/v1/geography/districts?state_id=KA")
        districts = response.json()
        assert len(districts) == 2
        assert all(d["state_id"] == "KA" for d in districts)

    def test_filter_districts_by_tier(self, client, seed_data):
        response = client.get("/api/v1/geography/districts?tier=Tier-1")
        districts = response.json()
        assert len(districts) == 2

    def test_district_not_found(self, client):
        response = client.get("/api/v1/geography/districts/NONEXISTENT")
        assert response.status_code == 404


class TestSectors:
    def test_list_sectors_empty(self, client):
        response = client.get("/api/v1/sectors/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_sectors(self, client, seed_data):
        response = client.get("/api/v1/sectors/")
        sectors = response.json()
        assert len(sectors) == 3

    def test_get_sector(self, client, seed_data):
        response = client.get("/api/v1/sectors/health")
        assert response.status_code == 200
        assert response.json()["sector_name"] == "Health"

    def test_sector_not_found(self, client):
        response = client.get("/api/v1/sectors/nonexistent")
        assert response.status_code == 404


class TestIndicators:
    def test_list_indicators_empty(self, client):
        response = client.get("/api/v1/indicators/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_indicators(self, client, seed_data):
        response = client.get("/api/v1/indicators/")
        assert len(response.json()) == 2

    def test_filter_indicators_by_sector(self, client, seed_data):
        response = client.get("/api/v1/indicators/?sector_id=health")
        indicators = response.json()
        assert len(indicators) == 1
        assert indicators[0]["indicator_id"] == "IMR"

    def test_filter_indicators_by_source(self, client, seed_data):
        response = client.get("/api/v1/indicators/?source=SRS")
        indicators = response.json()
        assert len(indicators) == 1

    def test_get_indicator_detail(self, client, seed_data):
        response = client.get("/api/v1/indicators/IMR")
        assert response.status_code == 200
        indicator = response.json()
        assert indicator["indicator_name"] == "Infant Mortality Rate"
        assert len(indicator["values"]) == 3

    def test_indicator_not_found(self, client):
        response = client.get("/api/v1/indicators/NONEXISTENT")
        assert response.status_code == 404

    def test_list_indicator_values(self, client, seed_data):
        response = client.get("/api/v1/indicators/values/")
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_filter_values_by_indicator(self, client, seed_data):
        response = client.get("/api/v1/indicators/values/?indicator_id=IMR")
        values = response.json()
        assert len(values) == 3
        assert all(v["indicator_id"] == "IMR" for v in values)

    def test_filter_values_by_state(self, client, seed_data):
        response = client.get("/api/v1/indicators/values/?state_id=KA")
        values = response.json()
        assert len(values) == 3

    def test_filter_values_by_year(self, client, seed_data):
        response = client.get("/api/v1/indicators/values/?year=2020")
        values = response.json()
        assert len(values) == 2


class TestPolicies:
    def test_list_schemes_empty(self, client):
        response = client.get("/api/v1/policies/schemes")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_schemes(self, client, seed_data):
        response = client.get("/api/v1/policies/schemes")
        assert len(response.json()) == 2

    def test_filter_schemes_by_sector(self, client, seed_data):
        response = client.get("/api/v1/policies/schemes?sector_id=health")
        schemes = response.json()
        assert len(schemes) == 1
        assert schemes[0]["scheme_id"] == "NRHM"

    def test_filter_schemes_by_status(self, client, seed_data):
        response = client.get("/api/v1/policies/schemes?status=Active")
        assert len(response.json()) == 2

    def test_filter_schemes_by_level(self, client, seed_data):
        response = client.get("/api/v1/policies/schemes?level=Central")
        assert len(response.json()) == 2

    def test_get_scheme_detail(self, client, seed_data):
        response = client.get("/api/v1/policies/schemes/NRHM")
        assert response.status_code == 200
        scheme = response.json()
        assert scheme["scheme_name"] == "National Rural Health Mission"
        assert len(scheme["budgets"]) == 2
        assert len(scheme["coverage"]) == 2

    def test_scheme_not_found(self, client):
        response = client.get("/api/v1/policies/schemes/NONEXISTENT")
        assert response.status_code == 404

    def test_list_budgets(self, client, seed_data):
        response = client.get("/api/v1/policies/budgets")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_filter_budgets_by_scheme(self, client, seed_data):
        response = client.get("/api/v1/policies/budgets?scheme_id=NRHM")
        budgets = response.json()
        assert len(budgets) == 2

    def test_filter_budgets_by_fiscal_year(self, client, seed_data):
        response = client.get("/api/v1/policies/budgets?fiscal_year=2022-23")
        assert len(response.json()) == 2

    def test_list_coverage(self, client, seed_data):
        response = client.get("/api/v1/policies/coverage")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_filter_coverage_by_state(self, client, seed_data):
        response = client.get("/api/v1/policies/coverage?state_id=KA")
        coverage = response.json()
        assert len(coverage) == 1
        assert coverage[0]["achievement_pct"] == 90.0


class TestTools:
    def test_list_tools_empty(self, client):
        response = client.get("/api/v1/tools/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tools(self, client, seed_data):
        response = client.get("/api/v1/tools/")
        assert len(response.json()) == 2

    def test_filter_tools_by_stack(self, client, seed_data):
        response = client.get("/api/v1/tools/?stack=ViewStack")
        tools = response.json()
        assert len(tools) == 1
        assert tools[0]["tool_name"] == "District Health Dashboard"

    def test_filter_tools_by_language(self, client, seed_data):
        response = client.get("/api/v1/tools/?language=Python")
        assert len(response.json()) == 1

    def test_filter_tools_by_difficulty(self, client, seed_data):
        response = client.get("/api/v1/tools/?difficulty=intermediate")
        assert len(response.json()) == 1

    def test_tool_not_found(self, client):
        response = client.get("/api/v1/tools/999")
        assert response.status_code == 404
