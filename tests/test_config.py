"""config 모듈 테스트."""

from src.config import (
    PLATFORM, ENV, DATASET_NAMES, DOMAINS, DATASET_DOMAIN_MAP,
    TAGS, ML_MODELS, GLOSSARY_NODES, GLOSSARY_TERMS, setup_logging,
)


def test_platform_constants():
    assert PLATFORM == "mysql"
    assert ENV == "PROD"


def test_dataset_names_count():
    assert len(DATASET_NAMES) == 10


def test_all_datasets_have_domain():
    for ds in DATASET_NAMES:
        assert ds in DATASET_DOMAIN_MAP, f"{ds} has no domain mapping"


def test_all_domain_mappings_reference_valid_domains():
    for ds, domain in DATASET_DOMAIN_MAP.items():
        assert domain in DOMAINS, f"{ds} maps to unknown domain {domain}"


def test_domains_count():
    assert len(DOMAINS) == 4


def test_tags_count():
    assert len(TAGS) == 7


def test_ml_models_have_required_keys():
    required_keys = {"name", "description", "type", "algorithm", "model_id"}
    for model_key, model_info in ML_MODELS.items():
        assert required_keys.issubset(model_info.keys()), (
            f"Model {model_key} missing keys: {required_keys - model_info.keys()}"
        )


def test_ml_models_count():
    assert len(ML_MODELS) == 5


def test_glossary_terms_reference_valid_nodes():
    for term_name, info in GLOSSARY_TERMS.items():
        assert info["group"] in GLOSSARY_NODES, (
            f"Term '{term_name}' references unknown group '{info['group']}'"
        )


def test_glossary_terms_have_definitions():
    for term_name, info in GLOSSARY_TERMS.items():
        assert "definition" in info and len(info["definition"]) > 0, (
            f"Term '{term_name}' has no definition"
        )


def test_setup_logging():
    log = setup_logging()
    assert log.name == "datahub-marketing"
