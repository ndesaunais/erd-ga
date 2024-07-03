from click.testing import CliRunner
from mermaid.erdiagram import Entity, ERDiagram, Link
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine

from erd_ga.erd_dump import erd_dump, sql_to_mermaid


def create_mermaid_dump(url):
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("out.mmd", "w") as f:
            result = runner.invoke(erd_dump, ["--url", url, "--output", f])
            assert result.exit_code == 0
        with open("out.mmd", "r") as f:
            out = f.read().strip()
            assert out
            return out


def test_sql_to_mermaid(postgres_simple):
    engine: Engine = create_engine(postgres_simple)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    er_diag = sql_to_mermaid(metadata)

    expect = ERDiagram(
        "bli",
        [
            Entity(
                "names",
                {
                    "firstname": ["VARCHAR", "nullable"],
                    "lastname": ["VARCHAR", "nullable"],
                },
            )
        ],
    )
    expect == er_diag


def test_erd_dump_simple(postgres_simple):
    out = create_mermaid_dump(postgres_simple)

    in_data = """erDiagram
\tnames{
\tVARCHAR firstname "nullable"
\tVARCHAR lastname "nullable"
}
""".strip()
    assert out == in_data


def test_erd_dump_airbnb(postgres_airbnb):
    engine: Engine = create_engine(postgres_airbnb)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    er_diag = sql_to_mermaid(metadata)

    addresses = Entity(
        "addresses",
        {
            "id": ["INTEGER", "PK"],
            "street": ["TEXT", "nullable"],
            "suburb": ["TEXT", "nullable"],
            "government_area": ["TEXT", "nullable"],
            "market": ["TEXT", "nullable"],
            "country": ["TEXT", "nullable"],
            "country_code": ["TEXT", "nullable"],
            "location": ["JSON", "nullable"],
        },
    )
    hosts = Entity(
        "hosts",
        {
            "id": ["INTEGER", "PK"],
            "url": ["TEXT", "nullable"],
            "name": ["TEXT", "nullable"],
            "location": ["TEXT", "nullable"],
            "about": ["TEXT", "nullable"],
            "response_time": ["TEXT", "nullable"],
            "thumbnail_url": ["TEXT", "nullable"],
            "picture_url": ["TEXT", "nullable"],
            "neighbourhood": ["TEXT", "nullable"],
            "response_rate": ["INTEGER", "nullable"],
            "is_superhost": ["BOOLEAN", "nullable"],
            "has_profile_pic": ["BOOLEAN", "nullable"],
            "identity_verified": ["BOOLEAN", "nullable"],
            "listings_count": ["INTEGER", "nullable"],
            "total_listings_count": ["INTEGER", "nullable"],
            "verifications": ["JSON", "nullable"],
        },
    )
    listings = Entity(
        "listings",
        {
            "id": ["VARCHAR", "PK"],
            "listing_url": ["TEXT", "nullable"],
            "name": ["TEXT", "nullable"],
            "summary": ["TEXT", "nullable"],
            "space": ["TEXT", "nullable"],
            "description": ["TEXT", "nullable"],
            "neighborhood_overview": ["TEXT", "nullable"],
            "notes": ["TEXT", "nullable"],
            "transit": ["TEXT", "nullable"],
            "access": ["TEXT", "nullable"],
            "interaction": ["TEXT", "nullable"],
            "house_rules": ["TEXT", "nullable"],
            "property_type": ["TEXT", "nullable"],
            "room_type": ["TEXT", "nullable"],
            "bed_type": ["TEXT", "nullable"],
            "minimum_nights": ["TEXT", "nullable"],
            "maximum_nights": ["TEXT", "nullable"],
            "cancellation_policy": ["TEXT", "nullable"],
            "last_scraped": ["TIMESTAMP", "nullable"],
            "calendar_last_scraped": ["TIMESTAMP", "nullable"],
            "first_review": ["TIMESTAMP", "nullable"],
            "last_review": ["TIMESTAMP", "nullable"],
            "accommodates": ["INTEGER", "nullable"],
            "bedrooms": ["INTEGER", "nullable"],
            "beds": ["INTEGER", "nullable"],
            "number_of_reviews": ["INTEGER", "nullable"],
            "bathrooms": ["DOUBLE_PRECISION", "nullable"],
            "amenities": ["JSON", "nullable"],
            "price": ["DOUBLE_PRECISION", "nullable"],
            "security_deposit": ["DOUBLE_PRECISION", "nullable"],
            "cleaning_fee": ["DOUBLE_PRECISION", "nullable"],
            "extra_people": ["DOUBLE_PRECISION", "nullable"],
            "guests_included": ["DOUBLE_PRECISION", "nullable"],
            "images": ["JSON", "nullable"],
            "availability": ["JSON", "nullable"],
            "review_scores": ["JSON", "nullable"],
            "reviews_per_month": ["INTEGER", "nullable"],
            "address_id": ["INTEGER", "FK", "nullable"],
            "host_id": ["INTEGER", "FK", "nullable"],
            "weekly_price": ["DOUBLE_PRECISION", "nullable"],
            "monthly_price": ["DOUBLE_PRECISION", "nullable"],
        },
    )

    reviews = Entity(
        "reviews",
        {
            "id": ["VARCHAR", "PK"],
            "date": ["TIMESTAMP", "nullable"],
            "listing_id": ["VARCHAR", "FK", "nullable"],
            "reviewer_id": ["INTEGER", "nullable"],
            "reviewer_name": ["TEXT", "nullable"],
            "comments": ["TEXT", "nullable"],
        },
    )
    expect = ERDiagram(
        "bli",
        [addresses, hosts, listings, reviews],
        [
            Link(addresses, listings, "exactly-one", "zero-or-more", "address_id"),
            Link(hosts, listings, "exactly-one", "zero-or-more", "host_id"),
            Link(listings, reviews, "exactly-one", "zero-or-more", "listing_id"),
        ],
    )
    # TODO: comparison is order dependant...
    assert expect == er_diag


def test_erd_dump_analytics(postgres_analytics):
    engine: Engine = create_engine(postgres_analytics)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    er_diag = sql_to_mermaid(metadata)
    customer = Entity(
        "customer",
        {
            "id": ["VARCHAR", "PK"],
            "username": ["VARCHAR", "nullable"],
            "name": ["VARCHAR", "nullable"],
            "address": ["TEXT", "nullable"],
            "birthdate": ["TIMESTAMP", "nullable"],
            "email": ["VARCHAR", "nullable"],
            "active": ["BOOLEAN", "nullable"],
            "tier_and_details": ["JSON", "nullable"],
        },
    )
    customersxaccount = Entity(
        "customersxaccount",
        {
            "id": ["INTEGER", "PK"],
            "customer_id": ["VARCHAR", "FK", "nullable"],
            "account_id": ["VARCHAR", "FK", "nullable"],
        },
    )
    accounts = Entity(
        "accounts",
        {
            "id": ["VARCHAR", "PK"],
            "account_limit": ["INTEGER", "nullable"],
            "products": ["JSON", "nullable"],
        },
    )
    transactionsmetadata = Entity(
        "transactionsmetadata",
        {
            "id": ["VARCHAR", "PK"],
            "account_id": ["VARCHAR", "FK", "nullable"],
            "transaction_count": ["INTEGER", "nullable"],
            "bucket_start_date": ["TIMESTAMP", "nullable"],
            "bucket_end_date": ["TIMESTAMP", "nullable"],
        },
    )
    transactions = Entity(
        "transactions",
        {
            "id": ["INTEGER", "PK"],
            "account_id": ["VARCHAR", "FK", "nullable"],
            "date": ["TIMESTAMP", "nullable"],
            "amount": ["INTEGER", "nullable"],
            "transaction_code": ["VARCHAR", "nullable"],
            "symbol": ["VARCHAR", "nullable"],
            "price": ["DOUBLE_PRECISION", "nullable"],
            "total": ["DOUBLE_PRECISION", "nullable"],
        },
    )

    expect = ERDiagram(
        "bli",
        [customer, customersxaccount, accounts, transactionsmetadata, transactions],
        [
            Link(
                customer,
                customersxaccount,
                "exactly-one",
                "zero-or-more",
                "customer_id",
            ),
            Link(
                accounts, customersxaccount, "exactly-one", "zero-or-more", "account_id"
            ),
            Link(
                accounts,
                transactionsmetadata,
                "exactly-one",
                "zero-or-more",
                "account_id",
            ),
            Link(accounts, transactions, "exactly-one", "zero-or-more", "account_id"),
        ],
    )
    assert expect == er_diag


def test_erd_dump_mflix(postgres_mflix):
    engine: Engine = create_engine(postgres_mflix)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    er_diag = sql_to_mermaid(metadata)

    theaters = Entity(
        "theaters",
        {
            "id": ["VARCHAR", "PK"],
            "theaterid": ["INTEGER", "nullable"],
            "location": ["JSON", "nullable"],
        },
    )
    users = Entity(
        "users",
        {
            "id": ["VARCHAR", "PK"],
            "name": ["TEXT", "nullable"],
            "email": ["TEXT", "nullable"],
            "password": ["TEXT", "nullable"],
            "preferences": ["JSON", "nullable"],
        },
    )
    sessions = Entity(
        "sessions",
        {
            "id": ["VARCHAR", "PK"],
            "user_id": ["VARCHAR", "FK", "nullable"],
            "jwt": ["TEXT", "nullable"],
        },
    )
    movies = Entity(
        "movies",
        {
            "id": ["VARCHAR", "PK"],
            "title": ["TEXT", "nullable"],
            "year": ["INTEGER", "nullable"],
            "runtime": ["INTEGER", "nullable"],
            "released": ["TIMESTAMP", "nullable"],
            "poster": ["TEXT", "nullable"],
            "plot": ["TEXT", "nullable"],
            "fullplot": ["TEXT", "nullable"],
            "lastupdated": ["TIMESTAMP", "nullable"],
            "type": ["TEXT", "nullable"],
            "directors": ["JSON", "nullable"],
            "imdb": ["JSON", "nullable"],
            "casting": ["JSON", "nullable"],
            "countries": ["JSON", "nullable"],
            "genres": ["JSON", "nullable"],
            "tomatoes": ["JSON", "nullable"],
            "num_mflix_comments": ["INTEGER", "nullable"],
            "rated": ["TEXT", "nullable"],
            "awards": ["JSON", "nullable"],
            "languages": ["JSON", "nullable"],
            "writers": ["JSON", "nullable"],
            "metacritic": ["INTEGER", "nullable"],
        },
    )
    comments = Entity(
        "comments",
        {
            "id": ["VARCHAR", "PK"],
            "movie_id": ["VARCHAR", "FK", "nullable"],
            "name": ["TEXT", "nullable"],
            "email": ["TEXT", "nullable"],
            "text": ["TEXT", "nullable"],
            "date": ["TIMESTAMP", "nullable"],
        },
    )

    expect = ERDiagram(
        "bli",
        [theaters, users, sessions, movies, comments],
        [
            Link(users, sessions, "exactly-one", "zero-or-more", "user_id"),
            Link(movies, comments, "exactly-one", "zero-or-more", "movie_id"),
        ],
    )

    assert expect == er_diag
