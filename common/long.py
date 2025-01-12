import graphene
from graphql.language.ast import IntValue  # Correct import for GraphQL AST

class Long(graphene.Scalar):
    """Custom scalar to represent Long integers."""

    @staticmethod
    def serialize(value):
        """Serialize the Long value to an integer."""
        if value is None:
            return None
        return int(value)

    @staticmethod
    def parse_value(value):
        """Parse the value passed into GraphQL (ensure it's an integer)."""
        return int(value)

    @staticmethod
    def parse_literal(ast_node):
        """Parse a literal in the query."""
        if isinstance(ast_node, IntValue):
            return int(ast_node.value)
        return None