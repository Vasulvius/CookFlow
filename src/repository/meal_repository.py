from framefox.core.orm.abstract_repository import AbstractRepository
from src.entity.meal import Meal

""" Available Methods:
find(id)                                                     # Retrieve entity by ID
find_all()                                                   # Retrieve all entities
find_by(criteria, order_by=None, limit=None, offset=None)    # Retrieve entities by criteria
get_query_builder()                                          # Get QueryBuilder instance for complex queries

Example:
user = user_repo.find(1)
users = user_repo.find_all()
active_users = user_repo.find_by({"active": True})
"""


class MealRepository(AbstractRepository):
    def __init__(self):
        super().__init__(Meal)

    ###########
    # build your own query by using the QueryBuilder
    ###########
    # def get_user_by_email(self, email: str):
    #     query_builder = self.get_query_builder()
    #     return (
    #         query_builder
    #         .select()
    #         .where(self.model.email == email)
    #         .first()
    #     )
 