from typing import Any, Dict, List, Optional, Type

from flask_appbuilder.models.filters import BaseFilter
from flask_appbuilder.models.sqla import Model
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from dao.exceptions import (
    DAOConfigError,
    DAOCreateFailedError,
    DAODeleteFailedError,
    DAOUpdateFailedError,
)


class BaseDAO:
    """
    Base DAO, implement base CRUD sqlalchemy operations
    """

    model_cls: Optional[Type[Model]] = None
    """
    Child classes need to state the Model class so they don't need to implement basic
    create, update and delete methods
    """
    base_filter: Optional[BaseFilter] = None
    """
    Child classes can register base filtering to be aplied to all filter methods
    """

    @classmethod
    def find_by_id(cls, model_id: int, session: Session = None) -> Model:
        from api import db
        """
        Find a model by id, if defined applies `base_filter`
        """
        session = session or db.session
        query = session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, session)
            query = cls.base_filter(  # pylint: disable=not-callable
                "id", data_model
            ).apply(query, None)
        return query.filter_by(id=model_id).one_or_none()

    @classmethod
    def find_by_ids(cls, model_ids: List[int]) -> List[Model]:
        """
        Find a List of models by a list of ids, if defined applies `base_filter`
        """
        id_col = getattr(cls.model_cls, "id", None)
        if id_col is None:
            return []
        from api import db
        query = db.session.query(cls.model_cls).filter(id_col.in_(model_ids))
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter(  # pylint: disable=not-callable
                "id", data_model
            ).apply(query, None)
        return query.all()

    @classmethod
    def find_all(cls) -> List[Model]:
        """
        Get all that fit the `base_filter`
        """
        from api import db
        query = db.session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter(  # pylint: disable=not-callable
                "id", data_model
            ).apply(query, None)
        return query.all()

    @classmethod
    def find_one_or_none(cls, **filter_by: Any) -> Optional[Model]:
        """
        Get the first that fit the `base_filter`
        """
        from api import db
        query = db.session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)

            query = cls.base_filter( #pylint: disable=not-callable
                "id", data_model
            ).apply(query, None)
        return query.filter_by(**filter_by).one_or_none()

    @classmethod
    def create(cls, properties: Dict[str, Any], commit: bool = True) -> Model:
        """
        Generic for creating models
        :raises: DAOCreateFailedError
        """
        if cls.model_cls is None:
            raise DAOConfigError()
        model = cls.model_cls()  # pylint: disable=not-callable
        for key, value in properties.items():
            setattr(model, key, value)
        try:
            from api import db
            db.session.add(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAOCreateFailedError(exception=ex) from ex
        return model

    @classmethod
    def save(cls, instance_model: Model, commit: bool = True) -> Model:
        """
        Generic for saving models
        :raises: DAOCreateFailedError
        """
        if cls.model_cls is None:
            raise DAOConfigError()
        if not isinstance(instance_model, cls.model_cls):
            raise DAOCreateFailedError(
                "the instance model is not a type of the model class"
            )
        try:
            from api import db
            db.session.add(instance_model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAOCreateFailedError(exception=ex) from ex
        return instance_model

    @classmethod
    def update(
        cls, model: Model, properties: Dict[str, Any], commit: bool = True
    ) -> Model:
        """
        Generic update a model
        :raises: DAOCreateFailedError
        """
        for key, value in properties.items():
            setattr(model, key, value)
        try:
            from api import db
            db.session.merge(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAOUpdateFailedError(exception=ex) from ex
        return model

    @classmethod
    def delete(cls, model: Model, commit: bool = True) -> Model:
        """
        Generic delete a model
        :raises: DAOCreateFailedError
        """
        try:
            from api import db
            db.session.delete(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAODeleteFailedError(exception=ex) from ex
        return model