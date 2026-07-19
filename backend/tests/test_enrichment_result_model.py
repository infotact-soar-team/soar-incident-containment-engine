import uuid
from app.models.enrichment_result import EnrichmentResultModel
from app.models.ioc import IOC


def test_enrichment_result_model_fields():
    result = EnrichmentResultModel(
        ioc_id=uuid.uuid4(),
        abuse_confidence_score=92,
        vt_malicious_count=58,
        geo_country="Germany",
        risk_score=95,
    )
    assert result.abuse_confidence_score == 92
    assert result.geo_country == "Germany"


def test_ioc_model_has_enrichment_fk():
    ioc = IOC(alert_id=uuid.uuid4(), ioc_type="ip", value="185.220.101.1")
    assert hasattr(ioc, "enrichment_id")