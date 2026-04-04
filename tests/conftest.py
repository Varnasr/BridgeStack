import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.geography import District, State
from app.models.indicators import Indicator, IndicatorValue
from app.models.policies import Scheme, SchemeBudget, SchemeCoverage
from app.models.sectors import Sector
from app.models.tools import Tool

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def seed_data(db):
    """Populate the test database with representative sample data."""
    # Sectors
    health = Sector(sector_id="health", sector_name="Health")
    education = Sector(sector_id="education", sector_name="Education")
    nutrition = Sector(sector_id="health-nutrition", sector_name="Nutrition", parent_id="health")
    db.add_all([health, education, nutrition])

    # States
    karnataka = State(
        state_id="KA",
        state_name="Karnataka",
        region="South",
        state_type="State",
        capital="Bengaluru",
        area_sq_km=191791.0,
        census_2011_pop=61095297,
    )
    maharashtra = State(
        state_id="MH",
        state_name="Maharashtra",
        region="West",
        state_type="State",
        capital="Mumbai",
        area_sq_km=307713.0,
        census_2011_pop=112374333,
    )
    db.add_all([karnataka, maharashtra])

    # Districts
    bengaluru = District(
        district_id="KA-BLR",
        district_name="Bengaluru Urban",
        state_id="KA",
        tier="Tier-1",
        census_2011_pop=9621551,
        area_sq_km=2196.0,
        latitude=12.97,
        longitude=77.59,
    )
    mysuru = District(
        district_id="KA-MYS",
        district_name="Mysuru",
        state_id="KA",
        tier="Tier-2",
        census_2011_pop=3001127,
        area_sq_km=6854.0,
        latitude=12.30,
        longitude=76.64,
    )
    mumbai = District(
        district_id="MH-MUM",
        district_name="Mumbai",
        state_id="MH",
        tier="Tier-1",
        census_2011_pop=12442373,
        area_sq_km=603.0,
        latitude=19.08,
        longitude=72.88,
    )
    db.add_all([bengaluru, mysuru, mumbai])

    # Indicators
    imr = Indicator(
        indicator_id="IMR",
        indicator_name="Infant Mortality Rate",
        sector_id="health",
        unit="per 1000 live births",
        direction="lower_is_better",
        source="SRS",
        frequency="Annual",
        description="Deaths of infants under one year per 1000 live births",
    )
    literacy = Indicator(
        indicator_id="LIT",
        indicator_name="Literacy Rate",
        sector_id="education",
        unit="percentage",
        direction="higher_is_better",
        source="Census",
        frequency="Decennial",
        description="Percentage of population aged 7+ that is literate",
    )
    db.add_all([imr, literacy])

    # Indicator values
    db.add_all(
        [
            IndicatorValue(indicator_id="IMR", state_id="KA", year=2020, value=25.0),
            IndicatorValue(indicator_id="IMR", state_id="MH", year=2020, value=19.0),
            IndicatorValue(indicator_id="IMR", state_id="KA", year=2021, value=23.0),
            IndicatorValue(indicator_id="LIT", state_id="KA", year=2011, value=75.4),
            IndicatorValue(indicator_id="LIT", state_id="MH", year=2011, value=82.3),
        ]
    )

    # Schemes
    nrhm = Scheme(
        scheme_id="NRHM",
        scheme_name="National Rural Health Mission",
        ministry="Ministry of Health",
        sector_id="health",
        level="Central",
        launch_year=2005,
        status="Active",
        beneficiary_type="Rural population",
        website="https://nhm.gov.in",
    )
    mdm = Scheme(
        scheme_id="MDM",
        scheme_name="Mid-Day Meal Scheme",
        ministry="Ministry of Education",
        sector_id="education",
        level="Central",
        launch_year=1995,
        status="Active",
        beneficiary_type="School children",
    )
    db.add_all([nrhm, mdm])

    # Budgets
    db.add_all(
        [
            SchemeBudget(
                scheme_id="NRHM",
                fiscal_year="2022-23",
                allocated_crores=37800.0,
                revised_crores=35200.0,
                spent_crores=33100.0,
            ),
            SchemeBudget(
                scheme_id="NRHM",
                fiscal_year="2023-24",
                allocated_crores=40000.0,
                revised_crores=38500.0,
                spent_crores=36200.0,
            ),
            SchemeBudget(
                scheme_id="MDM",
                fiscal_year="2022-23",
                allocated_crores=10234.0,
                revised_crores=9800.0,
                spent_crores=9500.0,
            ),
        ]
    )

    # Coverage
    db.add_all(
        [
            SchemeCoverage(
                scheme_id="NRHM",
                state_id="KA",
                year=2022,
                beneficiaries=4500000,
                target=5000000,
                achievement_pct=90.0,
            ),
            SchemeCoverage(
                scheme_id="NRHM",
                state_id="MH",
                year=2022,
                beneficiaries=8200000,
                target=9000000,
                achievement_pct=91.1,
            ),
        ]
    )

    # Tools
    db.add_all(
        [
            Tool(
                tool_name="District Health Dashboard",
                stack="ViewStack",
                directory="dashboards/health",
                description="Interactive health indicator explorer",
                sector="health",
                language="JavaScript",
                tool_type="dashboard",
                difficulty="intermediate",
                tags="health,dashboard,d3",
                file_count=12,
            ),
            Tool(
                tool_name="Equity Analysis Notebook",
                stack="EquityStack",
                directory="notebooks/equity",
                description="Jupyter notebook for equity gap analysis",
                sector="education",
                language="Python",
                tool_type="notebook",
                difficulty="advanced",
                tags="equity,analysis,jupyter",
                file_count=5,
            ),
        ]
    )

    db.commit()

    return {
        "states": [karnataka, maharashtra],
        "districts": [bengaluru, mysuru, mumbai],
        "sectors": [health, education, nutrition],
        "indicators": [imr, literacy],
        "schemes": [nrhm, mdm],
    }
