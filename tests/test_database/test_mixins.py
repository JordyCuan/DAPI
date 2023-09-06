from sqlalchemy.orm import Mapped, Session, mapped_column

from utils.database.mixins import TimestampMixin
from utils.database.models import APIBaseModel


class SampleModel(APIBaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]


class TestTimestampMixin:
    def test_default_timestamps(self, session: Session):
        instance = SampleModel(name="Test")
        session.add(instance)
        session.commit()
        assert instance.created_at is not None
        assert instance.updated_at is not None

    def test_updated_at_changes(self, session: Session):
        instance = SampleModel(name="Original")
        session.add(instance)
        session.commit()

        original_updated_at = instance.updated_at
        instance.name = "Updated"  # type: ignore
        session.commit()
        assert instance.updated_at != original_updated_at
