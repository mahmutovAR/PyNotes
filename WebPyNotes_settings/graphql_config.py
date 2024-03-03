from urllib.parse import urljoin


class GraphqlConfig:
    """Class with GraphQL API settings."""
    __slots__ = ['ip_and_port', 'gql_endpoint']

    def __init__(self):
        self.ip_and_port = 'http://127.0.0.1:30000/'
        self.gql_endpoint = '/pynotes/graphql'

    def get_gql_endpoint(self):
        """Returns the GraphQL API endpoint."""
        return self.gql_endpoint

    def get_graphql_api(self):
        """Returns the GraphQL API absolut URL."""
        return urljoin(self.ip_and_port, self.gql_endpoint)


GraphqlAPI = GraphqlConfig()
