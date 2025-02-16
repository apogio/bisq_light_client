from bisq.common.protocol.network.network_envelope import NetworkEnvelope
from bisq.core.dao.monitoring.network.request_state_hashes_handler import (
    RequestStateHashesHandler,
)
from bisq.core.dao.monitoring.network.messages.get_dao_state_hashes_request import (
    GetDaoStateHashesRequest,
)
from bisq.core.dao.monitoring.network.messages.get_dao_state_hashes_response import (
    GetDaoStateHashesResponse,
)


class RequestDaoStateHashesHandler(
    RequestStateHashesHandler[GetDaoStateHashesRequest, GetDaoStateHashesResponse]
):

    def get_get_state_hashes_request(
        self, from_height: int
    ) -> GetDaoStateHashesRequest:
        return GetDaoStateHashesRequest(height=from_height, nonce=self.nonce)

    def cast_to_get_state_hashes_response(
        self, network_envelope: NetworkEnvelope
    ) -> "GetDaoStateHashesResponse":
        return network_envelope

    def is_get_state_hashes_response(self, network_envelope: NetworkEnvelope) -> bool:
        return isinstance(network_envelope, GetDaoStateHashesResponse)
